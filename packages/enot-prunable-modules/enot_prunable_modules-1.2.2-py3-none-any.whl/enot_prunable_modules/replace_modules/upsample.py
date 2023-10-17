import types

import torch
from diffusers.models.lora import LoRACompatibleConv
from diffusers.models.resnet import Upsample2D
from torch import nn
from torch.nn import functional as F

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableUpsample2D",
    "UpsampleReplacer",
]


class PrunableUpsample2D(Upsample2D):
    """
    Prunable version of forward.

    See diffusers.models.resnet.Upsample2D.

    Problem was that self.channels didn't trace and prune
    so assert always raised assertion error.

    """

    def forward(self, hidden_states, output_size=None, scale: float = 1.0):
        """Remove assert."""
        if self.use_conv_transpose:
            assert isinstance(self.conv, nn.Conv2d)
            return self.conv(hidden_states)

        # Cast to float32 to as 'upsample_nearest2d_out_frame' op does not support bfloat16
        # TODO(Suraj): Remove this cast once the issue is fixed in PyTorch
        # https://github.com/pytorch/pytorch/issues/86679
        dtype = hidden_states.dtype
        if dtype == torch.bfloat16:
            hidden_states = hidden_states.to(torch.float32)

        # upsample_nearest_nhwc fails with large batch sizes. see https://github.com/huggingface/diffusers/issues/984
        if hidden_states.shape[0] >= 64:
            hidden_states = hidden_states.contiguous()

        # if `output_size` is passed we force the interpolation output
        # size and do not make use of `scale_factor=2`
        if output_size is None:
            hidden_states = F.interpolate(hidden_states, scale_factor=2.0, mode="nearest")
        else:
            hidden_states = F.interpolate(hidden_states, size=output_size, mode="nearest")

        # If the input is bfloat16, we cast back to bfloat16
        if dtype == torch.bfloat16:
            hidden_states = hidden_states.to(dtype)

        # TODO(Suraj, Patrick) - clean up after weight dicts are correctly renamed
        if self.use_conv:
            if self.name == "conv":
                if isinstance(self.conv, LoRACompatibleConv):
                    hidden_states = self.conv(hidden_states, scale)
                else:
                    assert isinstance(self.conv, nn.Conv2d)
                    hidden_states = self.conv(hidden_states)
            else:
                if isinstance(self.Conv2d_0, LoRACompatibleConv):
                    hidden_states = self.Conv2d_0(hidden_states, scale)
                else:
                    assert isinstance(self.Conv2d_0, nn.Conv2d)
                    hidden_states = self.Conv2d_0(hidden_states)

        return hidden_states


class UpsampleReplacer(Replacer):
    """
    Upsample2D module replacer.

    Replacing module forever. Revert method does nothing.
    Otherwise inference will fall with assertion error.

    """

    def replace(self, module: Upsample2D) -> None:
        """Replace Upsample2D module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableUpsample2D.forward, module)
        module.__class__ = PrunableUpsample2D

    def revert(self, module: PrunableUpsample2D) -> None:
        """Do nothing."""
