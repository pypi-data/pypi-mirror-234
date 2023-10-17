import typing
from typing import Optional
from typing import Tuple
from typing import Union

import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.common_types import _size_2_t
from torch.nn.modules.utils import _pair

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableGroupConv",
    "GroupConvReplacer",
]


class PrunableGroupConv(nn.Module):
    """
    Prunable version of group Conv from torch package.

    Native group Conv replaced with slice and convolutions.
    Be careful, diff is about 1e-7.

    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: Tuple[int, ...],
        groups: int = 1,
        stride: Tuple[int, ...] = (1, 1),
        padding: Union[str, Tuple[int, ...]] = (0, 0),
        dilation: Tuple[int, ...] = (1, 1),
        bias: bool = True,
        padding_mode: str = "zeros",
    ):
        """Initialize almost like in nn.Conv2d."""
        super().__init__()
        self.kernel_size = _pair(kernel_size)
        self.stride = _pair(stride)
        self.padding = padding if isinstance(padding, str) else _pair(padding)
        self.dilation = _pair(dilation)
        self.padding_mode = padding_mode

        self.groups = groups
        self.in_channels = in_channels
        self.out_channels = out_channels

        self.group_slice = in_channels // groups

        self.weight = nn.Parameter(
            torch.rand(
                groups,
                out_channels // groups,
                in_channels // groups,
                *kernel_size,
            )
        )

        self.bias = nn.Parameter(torch.rand(groups, out_channels // groups)) if bias else None

    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """Equivalent forward implementation for group conv."""
        groups = []
        for group_idx in range(self.groups):
            res = F.conv2d(
                input=input_tensor[:, : self.group_slice, :, :],
                weight=self.weight[group_idx],  # this indexing might cause a warnings
                bias=None if self.bias is None else self.bias[group_idx],  # and this
                stride=self.stride,
                padding=self.padding,
                dilation=self.dilation,
                groups=1,
            )
            groups.append(res)
            input_tensor = input_tensor[:, self.group_slice :, :, :]

        return torch.cat(groups, dim=1)

    def __repr__(self) -> str:
        """Representation with respect to pruning attribute."""
        out_channels, in_channels = self.weight.shape[1:3]
        in_channels *= self.groups
        out_channels *= self.groups

        return f"PrunableGroupConv({in_channels}, {out_channels}, groups={self.groups})"


class GroupConvReplacer(Replacer):
    """nn.Conv2d module with `1 < groups < in_channels` replacer."""

    def replace(self, module: nn.Conv2d) -> Optional[PrunableGroupConv]:
        """Replace nn.Conv2d module with its prunable version."""
        if module.groups in [1, module.in_channels]:
            return None

        prunable_conv = PrunableGroupConv(
            in_channels=module.in_channels,
            out_channels=module.out_channels,
            kernel_size=module.kernel_size,
            groups=module.groups,
            stride=module.stride,
            padding=module.padding,
            dilation=module.dilation,
            bias=module.bias is not None,
            padding_mode=module.padding_mode,
        )

        out_channels, in_channels, *kernel_size = module.weight.shape

        prunable_conv.weight = nn.Parameter(
            module.weight.reshape(module.groups, out_channels // module.groups, in_channels, *kernel_size),
        )

        if module.bias is not None:
            prunable_conv.bias = nn.Parameter(
                module.bias.reshape(module.groups, out_channels // module.groups),
            )

        return prunable_conv

    def revert(self, module: PrunableGroupConv) -> nn.Conv2d:
        """Revert nn.Conv2d module replacing."""
        groups, out_channels, in_channels, *kernel_size = module.weight.shape

        original_conv = nn.Conv2d(
            in_channels=in_channels * groups,
            out_channels=out_channels * groups,
            kernel_size=typing.cast(_size_2_t, tuple(kernel_size)),
            stride=typing.cast(_size_2_t, module.stride),
            padding=module.padding if isinstance(module.padding, str) else typing.cast(_size_2_t, module.padding),
            dilation=typing.cast(_size_2_t, module.dilation),
            groups=groups,
            bias=module.bias is not None,
            padding_mode=module.padding_mode,
        )

        original_conv.weight = nn.Parameter(
            module.weight.reshape(out_channels * groups, in_channels, *kernel_size),
        )

        if module.bias is not None:
            original_conv.bias = nn.Parameter(
                module.bias.reshape(out_channels * groups),
            )

        return original_conv
