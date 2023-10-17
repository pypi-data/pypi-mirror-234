# pylint: disable=ungrouped-imports
from enum import Enum
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Type

from torch import nn

from enot_prunable_modules.replace_modules.replacer import Replacer


class TypesTuple(NamedTuple):
    """
    Named tuple for factories.

    Attributes
    ----------
    original_type : Type
        A type to be replaced.
    replaced_type : Type
        A type to which will be replaced.

    """

    original_type: Type
    replaced_type: Type


class FactoryError(NamedTuple):
    """
    Factory errors encapsulation; designed for using as enum value in ``ReplaceFactory``.

    Attributes
    ----------
    error : str
        A string representation of the error encountered during factory initialization.
    proposal : str
        Suggestion for solving the error.

    """

    error: str
    proposal: str


# Torch Attention:
try:
    from enot_prunable_modules.replace_modules.torchvision_attention import PrunableTorchAttention
    from enot_prunable_modules.replace_modules.torchvision_attention import TorchAttentionReplacer

    _TORCH_ATTENTION_FACTORY = {
        TypesTuple(original_type=nn.MultiheadAttention, replaced_type=PrunableTorchAttention): TorchAttentionReplacer(),
    }
except ImportError as exc:
    _TORCH_ATTENTION_FACTORY = FactoryError(error=str(exc), proposal="check PyTorch installation")


# Group Convolution and Normalization:
try:
    from enot_prunable_modules.replace_modules.group_conv import GroupConvReplacer
    from enot_prunable_modules.replace_modules.group_conv import PrunableGroupConv
    from enot_prunable_modules.replace_modules.group_norm import GroupNormReplacer
    from enot_prunable_modules.replace_modules.group_norm import PrunableGroupNorm

    _GROUP_OPS_FACTORY = {
        TypesTuple(original_type=nn.GroupNorm, replaced_type=PrunableGroupNorm): GroupNormReplacer(),
        TypesTuple(original_type=nn.Conv2d, replaced_type=PrunableGroupConv): GroupConvReplacer(),
    }
except ImportError as exc:
    _GROUP_OPS_FACTORY = FactoryError(error=str(exc), proposal="check PyTorch installation")


# Kandinsky blocks:
try:
    from diffusers.models.attention_processor import Attention
    from diffusers.models.resnet import Downsample2D
    from diffusers.models.resnet import ResnetBlock2D
    from diffusers.models.resnet import Upsample2D

    from enot_prunable_modules.replace_modules.attention import AttentionReplacer
    from enot_prunable_modules.replace_modules.attention import PrunableAttention
    from enot_prunable_modules.replace_modules.downsample import DownsampleReplacer
    from enot_prunable_modules.replace_modules.downsample import PrunableDownsample2D
    from enot_prunable_modules.replace_modules.resnet import PrunableResnetBlock2D
    from enot_prunable_modules.replace_modules.resnet import ResnetBlock2DReplacer
    from enot_prunable_modules.replace_modules.upsample import PrunableUpsample2D
    from enot_prunable_modules.replace_modules.upsample import UpsampleReplacer

    _KANDINSKY_FACTORY = {
        TypesTuple(original_type=Attention, replaced_type=PrunableAttention): AttentionReplacer(),
        TypesTuple(original_type=ResnetBlock2D, replaced_type=PrunableResnetBlock2D): ResnetBlock2DReplacer(),
        TypesTuple(original_type=Upsample2D, replaced_type=PrunableUpsample2D): UpsampleReplacer(),
        TypesTuple(original_type=Downsample2D, replaced_type=PrunableDownsample2D): DownsampleReplacer(),
    }
except ImportError as exc:
    _KANDINSKY_FACTORY = FactoryError(
        error=str(exc),
        proposal="pip install enot-prunable-modules[diffusers]",
    )


# Timm Attention:
try:
    from timm.models.vision_transformer import Attention

    from enot_prunable_modules.replace_modules.timm_attention import PrunableTimmAttention
    from enot_prunable_modules.replace_modules.timm_attention import TimmAttentionReplacer

    _TIMM_ATTENTION_FACTORY = {
        TypesTuple(original_type=Attention, replaced_type=PrunableTimmAttention): TimmAttentionReplacer(),
    }
except ImportError as exc:
    _TIMM_ATTENTION_FACTORY = FactoryError(
        error=str(exc),
        proposal="pip install enot-prunable-modules[timm]",
    )


class ReplaceFactory(Enum):
    """
    Replace modules strategy.

    * KANDINSKY - diffusers kandinsky2-2 pruning
    * GROUP_OPS - group norm and group conv pruning
    * TORCH_ATTENTION - torch.nn.MultiheadAttention pruning
    * TIMM_ATTENTION - Timm ViT attention pruning

    """

    TORCH_ATTENTION = _TORCH_ATTENTION_FACTORY
    GROUP_OPS = _GROUP_OPS_FACTORY
    KANDINSKY = _KANDINSKY_FACTORY
    TIMM_ATTENTION = _TIMM_ATTENTION_FACTORY


def get_replacer(
    factory: ReplaceFactory,
    module: nn.Module,
    replace_type: bool,
) -> Optional[Replacer]:
    """Get value by tuple attribute (module_type) and key (module)."""
    if isinstance(factory.value, FactoryError):
        raise RuntimeError(
            f"{factory.name} factory is not available, error: {factory.value.error}, proposal: {factory.value.proposal}"
        )

    module_type = "replaced_type" if replace_type else "original_type"
    new_factory = dict(zip(_get_keys(factory, module_type), factory.value.values()))
    return new_factory[type(module)] if type(module) in new_factory else None


def _get_keys(
    factory: ReplaceFactory,
    module_type: str,
) -> List[Type]:
    """Get keys by tuple attribute."""
    return [getattr(module_tuple, module_type) for module_tuple in factory.value]
