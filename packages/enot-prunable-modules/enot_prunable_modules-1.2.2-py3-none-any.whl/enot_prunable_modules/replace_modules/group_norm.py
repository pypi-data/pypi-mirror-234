import typing

import torch
from torch import nn
from torch.nn import functional as F

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGroupNorm",
    "GroupNormReplacer",
]


class PrunableGroupNorm(nn.Module):
    """
    Prunable version of GroupNorm from torch package.

    Native GroupNorm replaced with slice and LayerNorm.
    Be careful, diff is about 1e-7.

    """

    def __init__(
        self,
        num_groups: int,
        num_channels: int,
        affine: bool = True,
        eps: float = 1e-5,
    ):
        """Initialize almost like in nn.GroupNorm."""
        super().__init__()
        self.num_channels = num_channels
        self.num_groups = num_groups
        self.weight = torch.empty(num_channels)
        self.bias = torch.empty(num_channels)
        self.affine = affine
        self.eps = eps

        if self.affine:
            self.weight = nn.Parameter(torch.ones(num_channels))
            self.bias = nn.Parameter(torch.zeros(num_channels))

        self.group_slice = num_channels // num_groups

    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """Equivalent forward implementation for group norm."""
        spatial = [*input_tensor.shape[2:]]

        groups = []
        for _ in range(self.num_groups):
            layer_norm = F.layer_norm(
                input=input_tensor[:, : self.group_slice, ...],
                normalized_shape=(typing.cast(int, self.group_slice), *spatial),
                eps=self.eps,
            )
            groups.append(layer_norm)
            input_tensor = input_tensor[:, self.group_slice :, ...]  # iterator

        input_tensor = torch.cat(groups, dim=1)

        if self.affine:
            view_shape = [1, self.num_channels] + [1] * (input_tensor.ndim - 2)
            input_tensor.mul_(self.weight.view(view_shape))
            input_tensor.add_(self.bias.view(view_shape))
            return input_tensor

        return input_tensor

    def __repr__(self) -> str:
        """Representation with respect to pruning attribute."""
        channels = self.num_groups * typing.cast(int, self.group_slice)
        return f"PrunableGroupNorm({self.num_groups}, {channels}, eps={self.eps}, affine={self.affine})"


class GroupNormReplacer(Replacer):
    """nn.GroupNorm module replacer."""

    def replace(self, module: nn.GroupNorm) -> PrunableGroupNorm:
        """Replace nn.GroupNorm module with its prunable version."""
        prunable_group_norm = PrunableGroupNorm(
            num_groups=module.num_groups,
            num_channels=module.num_channels,
            affine=module.affine,
            eps=module.eps,
        )
        if module.affine:
            prunable_group_norm.weight = nn.Parameter(module.weight)
            prunable_group_norm.bias = nn.Parameter(module.bias)

        return prunable_group_norm

    def revert(self, module: PrunableGroupNorm) -> nn.GroupNorm:
        """Revert nn.GroupNorm module replacing."""
        original_group_norm = nn.GroupNorm(
            num_groups=module.num_groups,
            num_channels=module.num_channels,
            eps=module.eps,
            affine=module.affine,
        )
        if module.affine:
            original_group_norm.weight = nn.Parameter(module.weight)
            original_group_norm.bias = nn.Parameter(module.bias)

        return original_group_norm
