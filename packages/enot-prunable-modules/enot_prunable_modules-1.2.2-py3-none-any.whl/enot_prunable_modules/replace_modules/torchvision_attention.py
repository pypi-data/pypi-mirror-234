import warnings
from typing import Optional
from typing import Tuple

import torch
from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer

__all__ = [
    "PrunableTorchAttention",
    "TorchAttentionReplacer",
]


class PrunableTorchAttention(nn.Module):
    """torch.nn.MultiheadAttention."""

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

        self.batch_first = True

        self.qkv = nn.Linear(dim, dim * 3, bias=qkv_bias)
        self.attn_drop = nn.Dropout(attn_drop)
        self.proj = nn.Linear(dim, dim)
        self.proj_drop = nn.Dropout(proj_drop)

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_padding_mask: Optional[torch.Tensor] = None,
        need_weights: bool = True,
        attn_mask: Optional[torch.Tensor] = None,
        average_attn_weights: bool = True,
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Rewrite forward.

        `batch_size, seq_len, channels = x.shape` -> `batch_size, seq_len, _ = x.shape`
        Replace using of channels with -1 in reshapes.
        Replace unbind with indexing.

        """
        del average_attn_weights

        if key_padding_mask is not None or need_weights or attn_mask is not None:
            raise NotImplementedError(
                'Forward for prunable "nn.MultiheadAttention" is not implemented '
                f'for "key_padding_mask"={key_padding_mask}, "need_weights"={need_weights}, and "attn_mask"={attn_mask}'
            )

        is_batched = query.dim() == 3

        if not is_batched:
            raise NotImplementedError(
                'Forward for prunable "nn.MultiheadAttention" is not implemented '
                f"for query dim != 3, got query dim={query.dim()}"
            )

        if not (query is key and key is value):
            raise NotImplementedError(
                'Forward for prunable "nn.MultiheadAttention" is implemented '
                'only for self-attention, got "query" != "key"'
            )

        input_tensor = query

        batch_size, seq_len, _ = input_tensor.shape
        qkv = self.qkv(input_tensor).reshape(batch_size, seq_len, 3, self.num_heads, -1).permute(2, 0, 3, 1, 4)
        query, key, value = qkv[0], qkv[1], qkv[2]

        attn = (query @ key.transpose(-2, -1)) * self.scale
        attn = self.attn_drop(attn.softmax(dim=-1))

        input_tensor = (attn @ value).transpose(1, 2).reshape(batch_size, seq_len, -1)
        input_tensor = self.proj(input_tensor)
        input_tensor = self.proj_drop(input_tensor)

        return input_tensor, None  # we need two outputs for nn.MultiheadAttention


class TorchAttentionReplacer(Replacer):
    """
    TorchAttention module replacer.

    Replacing module forever. Revert method does nothing.
    Otherwise inference will fall with shape mismatch.

    """

    def replace(self, module: nn.MultiheadAttention) -> PrunableTorchAttention:
        """Replace TorchAttention module with its prunable version."""
        # works only for self-attention
        warnings.warn(
            'Prunable version of "nn.MultiheadAttention" is implemented only for self-attention',
            UserWarning,
        )

        if not module.batch_first:
            raise NotImplementedError(
                'Prunable version of "nn.MultiheadAttention" is implemented '
                f'only for "batch_first"=True, got "batch_first"={module.batch_first}'
            )

        attn = PrunableTorchAttention(
            dim=module.embed_dim,
            num_heads=module.num_heads,
            qkv_bias=module.in_proj_bias is not None,
            attn_drop=module.dropout,
            proj_drop=module.dropout,
        )

        attn.qkv.weight = module.in_proj_weight
        attn.proj.weight = module.out_proj.weight

        attn.qkv.bias = module.in_proj_bias
        attn.proj.bias = module.out_proj.bias

        attn.batch_first = module.batch_first

        return attn

    def revert(self, module: PrunableTorchAttention) -> None:
        """Do nothing."""
