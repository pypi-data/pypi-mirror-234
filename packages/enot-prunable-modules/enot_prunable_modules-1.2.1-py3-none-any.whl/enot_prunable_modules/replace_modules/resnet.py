import types

from diffusers.models.resnet import Downsample2D
from diffusers.models.resnet import ResnetBlock2D
from diffusers.models.resnet import Upsample2D

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableResnetBlock2D",
    "ResnetBlock2DReplacer",
]


class PrunableResnetBlock2D(ResnetBlock2D):
    """diffusers.models.resnet.ResnetBlock2D."""

    def forward(self, input_tensor, temb, scale: float = 1.0):
        """Replace chunk with slice."""
        hidden_states = input_tensor

        if self.time_embedding_norm in ["ada_group", "spatial"]:
            hidden_states = self.norm1(hidden_states, temb)
        else:
            hidden_states = self.norm1(hidden_states)

        hidden_states = self.nonlinearity(hidden_states)

        if self.upsample is not None:
            # upsample_nearest_nhwc fails with large batch sizes.
            if hidden_states.shape[0] >= 64:
                input_tensor = input_tensor.contiguous()
                hidden_states = hidden_states.contiguous()
            input_tensor = (
                self.upsample(input_tensor, scale=scale)
                if isinstance(self.upsample, Upsample2D)
                else self.upsample(input_tensor)
            )
            hidden_states = (
                self.upsample(hidden_states, scale=scale)
                if isinstance(self.upsample, Upsample2D)
                else self.upsample(hidden_states)
            )
        elif self.downsample is not None:
            input_tensor = (
                self.downsample(input_tensor, scale=scale)
                if isinstance(self.downsample, Downsample2D)
                else self.downsample(input_tensor)
            )
            hidden_states = (
                self.downsample(hidden_states, scale=scale)
                if isinstance(self.downsample, Downsample2D)
                else self.downsample(hidden_states)
            )

        hidden_states = self.conv1(hidden_states, scale)

        if self.time_emb_proj is not None:
            if not self.skip_time_act:
                temb = self.nonlinearity(temb)
            temb = self.time_emb_proj(temb, scale)[:, :, None, None]

        if temb is not None and self.time_embedding_norm == "default":
            hidden_states = hidden_states + temb

        if self.time_embedding_norm in ["ada_group", "spatial"]:
            hidden_states = self.norm2(hidden_states, temb)
        else:
            hidden_states = self.norm2(hidden_states)

        if temb is not None and self.time_embedding_norm == "scale_shift":
            scale_shift, shift = temb[:, : self.out_channels, ...], temb[:, self.out_channels :, ...]
            hidden_states = hidden_states * (1 + scale_shift) + shift

        hidden_states = self.nonlinearity(hidden_states)

        hidden_states = self.dropout(hidden_states)
        hidden_states = self.conv2(hidden_states, scale)

        if self.conv_shortcut is not None:
            input_tensor = self.conv_shortcut(input_tensor, scale)

        output_tensor = (input_tensor + hidden_states) / self.output_scale_factor

        return output_tensor


class ResnetBlock2DReplacer(Replacer):
    """ResnetBlock2D module replacer."""

    def replace(self, module: ResnetBlock2D) -> None:
        """Replace ResnetBlock2D module inplace with its prunable version."""
        module.forward = types.MethodType(PrunableResnetBlock2D.forward, module)
        module.__class__ = PrunableResnetBlock2D

    def revert(self, module: PrunableResnetBlock2D) -> None:
        """Revert ResnetBlock2D module replacing."""
        module.__class__ = ResnetBlock2D
        module.forward = types.MethodType(ResnetBlock2D.forward, module)
