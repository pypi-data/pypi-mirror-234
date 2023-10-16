from enum import Enum
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Type

from diffusers.models.attention_processor import Attention
from diffusers.models.resnet import Downsample2D
from diffusers.models.resnet import ResnetBlock2D
from diffusers.models.resnet import Upsample2D
from timm.models.vision_transformer import Attention as TimmAttention
from torch import nn

from enot_prunable_modules.replace_modules import AttentionReplacer
from enot_prunable_modules.replace_modules import DownsampleReplacer
from enot_prunable_modules.replace_modules import GroupConvReplacer
from enot_prunable_modules.replace_modules import GroupNormReplacer
from enot_prunable_modules.replace_modules import PrunableAttention
from enot_prunable_modules.replace_modules import PrunableDownsample2D
from enot_prunable_modules.replace_modules import PrunableGroupConv
from enot_prunable_modules.replace_modules import PrunableGroupNorm
from enot_prunable_modules.replace_modules import PrunableResnetBlock2D
from enot_prunable_modules.replace_modules import PrunableTimmAttention
from enot_prunable_modules.replace_modules import PrunableTorchAttention
from enot_prunable_modules.replace_modules import PrunableUpsample2D
from enot_prunable_modules.replace_modules import ResnetBlock2DReplacer
from enot_prunable_modules.replace_modules import TimmAttentionReplacer
from enot_prunable_modules.replace_modules import TorchAttentionReplacer
from enot_prunable_modules.replace_modules import UpsampleReplacer
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


class ReplaceFactory(Enum):
    """
    Replace modules strategy.

    * KANDINSKY_PRUNING - diffusers kandinsky2-2 pruning
    * GROUP_OPS - group norm and group conv pruning
    * ATTENTIONS - attention modules from timm, diffusers and torch pruning

    """

    KANDINSKY_PRUNING = {
        TypesTuple(original_type=Attention, replaced_type=PrunableAttention): AttentionReplacer(),
        TypesTuple(original_type=ResnetBlock2D, replaced_type=PrunableResnetBlock2D): ResnetBlock2DReplacer(),
        TypesTuple(original_type=Upsample2D, replaced_type=PrunableUpsample2D): UpsampleReplacer(),
        TypesTuple(original_type=Downsample2D, replaced_type=PrunableDownsample2D): DownsampleReplacer(),
    }

    GROUP_OPS = {
        TypesTuple(original_type=nn.GroupNorm, replaced_type=PrunableGroupNorm): GroupNormReplacer(),
        TypesTuple(original_type=nn.Conv2d, replaced_type=PrunableGroupConv): GroupConvReplacer(),
    }

    ATTENTIONS = {
        TypesTuple(original_type=nn.MultiheadAttention, replaced_type=PrunableTorchAttention): TorchAttentionReplacer(),
        TypesTuple(original_type=TimmAttention, replaced_type=PrunableTimmAttention): TimmAttentionReplacer(),
    }


def get_replacer(
    factory: ReplaceFactory,
    module: nn.Module,
    replace_type: bool,
) -> Optional[Replacer]:
    """Get value by tuple attribute (module_type) and key (module)."""
    module_type = "replaced_type" if replace_type else "original_type"
    new_factory = dict(zip(_get_keys(factory, module_type), factory.value.values()))
    return new_factory[type(module)] if type(module) in new_factory else None


def _get_keys(
    factory: ReplaceFactory,
    module_type: str,
) -> List[Type]:
    """Get keys by tuple attribute."""
    return [getattr(module_tuple, module_type) for module_tuple in factory.value]
