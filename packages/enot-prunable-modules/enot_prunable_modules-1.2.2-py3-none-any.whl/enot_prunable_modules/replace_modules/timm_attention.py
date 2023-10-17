import torch
from timm.models.vision_transformer import Attention as TimmAttention
from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableTimmAttention",
    "TimmAttentionReplacer",
]


class PrunableTimmAttention(nn.Module):
    """timm.models.vision_transformer.Attention."""

    def __init__(
        self,
        dim: int,
        num_heads: int = 8,
        qkv_bias: bool = False,
        attn_drop: float = 0.0,
        proj_drop: float = 0.0,
    ):
        """No significant changes."""
        super().__init__()
        if dim % num_heads != 0:
            raise ValueError(f'"dim"={dim} should be divisible by "num_heads"={num_heads}')
        self.num_heads = num_heads
        head_dim = dim // num_heads
        self.scale = head_dim**-0.5

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(self, input_tensor) -> torch.Tensor:
        """
        Rewrite forward.

        `batch_size, seq_len, channels = input_tensor.shape` -> `batch_size, seq_len, _ = input_tensor.shape`
        Replace C in reshapes with -1
        Replace unbind with indexing.

        """
        batch_size, seq_len, _ = input_tensor.shape
        # Modification: replaced .
        qkv = self.qkv(input_tensor).reshape(batch_size, seq_len, 3, self.num_heads, -1).permute(2, 0, 3, 1, 4)
        query, key, value = qkv[0], qkv[1], qkv[2]

        attn = (query @ key.transpose(-2, -1)) * self.scale
        attn = attn.softmax(dim=-1)
        attn = self.attn_drop(attn)

        input_tensor = (attn @ value).transpose(1, 2).reshape(batch_size, seq_len, -1)
        input_tensor = self.proj(input_tensor)
        input_tensor = self.proj_drop(input_tensor)
        return input_tensor


class TimmAttentionReplacer(Replacer):
    """
    TimmAttention module replacer.

    Replacing module forever. Revert method does nothing.
    Otherwise inference will fall with assertion error and shape mismatch.

    """

    def replace(self, module: TimmAttention) -> PrunableTimmAttention:
        """Replace TimmAttention module with its prunable version."""
        attn = PrunableTimmAttention(
            dim=module.qkv.in_features,
            num_heads=module.num_heads,
            qkv_bias=module.qkv.bias is not None,
            attn_drop=module.attn_drop.p,
            proj_drop=module.proj_drop.p,
        )

        attn.qkv.weight = module.qkv.weight
        attn.proj.weight = module.proj.weight

        attn.qkv.bias = module.qkv.bias
        attn.proj.bias = module.proj.bias

        return attn

    def revert(self, module: PrunableTimmAttention) -> None:
        """Do nothing."""
