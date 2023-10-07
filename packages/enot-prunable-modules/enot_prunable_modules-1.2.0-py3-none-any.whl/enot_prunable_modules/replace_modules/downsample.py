import types

from diffusers.models.lora import LoRACompatibleConv
from diffusers.models.resnet import Downsample2D
from torch.nn import functional as F

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableDownsample2D",
    "DownsampleReplacer",
]


class PrunableDownsample2D(Downsample2D):
    """
    Prunable version of forward.

    See diffusers.models.resnet.Downsample2D.

    Problem was that self.channels didn't trace and prune
    so assert always raised assertion error.

    """

    def forward(self, hidden_states, scale: float = 1.0):
        """Remove assert."""
        if self.use_conv and self.padding == 0:
            pad = (0, 1, 0, 1)
            hidden_states = F.pad(hidden_states, pad, mode="constant", value=0)

        if isinstance(self.conv, LoRACompatibleConv):
            hidden_states = self.conv(hidden_states, scale)
        else:
            hidden_states = self.conv(hidden_states)

        return hidden_states


class DownsampleReplacer(Replacer):
    """
    Downsample2D module replacer.

    Replacing module forever. Revert method does nothing.
    Otherwise inference will fall with assertion error.

    """

    def replace(self, module: Downsample2D) -> None:
        """Replace Downsample2D module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableDownsample2D.forward, module)
        module.__class__ = PrunableDownsample2D

    def revert(self, module: PrunableDownsample2D) -> None:
        """Do nothing."""
