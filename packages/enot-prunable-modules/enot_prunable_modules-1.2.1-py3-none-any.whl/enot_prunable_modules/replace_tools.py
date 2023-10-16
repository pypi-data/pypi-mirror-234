from typing import List
from typing import Union

from torch import nn

from enot_prunable_modules.replace_factory import ReplaceFactory
from enot_prunable_modules.replace_factory import get_replacer
from enot_prunable_modules.utils import replace_named_value

__all__ = [
    "replace_implementations",
    "revert_implementations",
]


def replace_implementations(
    model: nn.Module,
    factory: Union[List[ReplaceFactory], ReplaceFactory],
) -> None:
    """
    Replace non-prunable modules with it's prunable variants.

    Note that the function works in-place.

    Parameters
    ----------
    model : nn.Module
        Pytorch model that we check for factory.original_type
        modules and replace them with factory.replaced_type.

    factory : Union[List[ReplaceFactory], ReplaceFactory]
        Module replace strategies.

    """
    for specific_factory in factory if isinstance(factory, List) else [factory]:
        for name, module in model.named_modules():
            if replacer := get_replacer(specific_factory, module, replace_type=False):
                if new_module := replacer.replace(module):
                    replace_named_value(model=model, attr_name=name, attr=new_module)


def revert_implementations(
    model: nn.Module,
    factory: Union[List[ReplaceFactory], ReplaceFactory],
) -> None:
    """
    Replace modules implementations with its origin.

    Note that the function works in-place.

    Parameters
    ----------
    model : nn.Module
        Pytorch model that we check for replaced ENOT modules and replace them with original ones.

    factory : Union[List[ReplaceFactory], ReplaceFactory]
        Module replace strategies.

    """
    for specific_factory in factory if isinstance(factory, List) else [factory]:
        for name, module in model.named_modules():
            if replacer := get_replacer(specific_factory, module, replace_type=True):
                if new_module := replacer.revert(module):
                    replace_named_value(model=model, attr_name=name, attr=new_module)
