import warnings
from operator import attrgetter
from typing import Any

import torch


def getattr_complex(obj: object, attr: str) -> Any:
    """
    Return the value of attribute given by ``complex_name`` if it exists, otherwise throws an error.

    Parameters
    ----------
    obj : object
        Top level object.
    attr : str
        Path to attribute, where next level attribute separates by '.'.

    Returns
    -------
    Any
        The value of attribute referenced by ``complex_name``.

    Raises
    ------
    AttributeError
        If attribute not found.

    """
    return attrgetter(attr)(obj) if attr != "" else obj


def is_property(instance: object, attribute: str) -> bool:
    """Has attribute property decorator or not."""
    return isinstance(getattr(type(instance), attribute, False), property)


def replace_named_value(model: torch.nn.Module, attr_name: str, attr: Any) -> None:
    """
    Replace value in model by it's full name.

    Parameters
    ----------
    model : torch.nn.Module
        Model where value should be replaced.
    attr_name : str
        Full name of an attribute to be replaced.
    attr : any
        Replace value for attribute.

    """
    if "." in attr_name:
        module_name, attribute_name = attr_name.rsplit(".", 1)
        parent_module = getattr_complex(model, module_name)
    else:
        attribute_name = attr_name
        parent_module = model

    if is_property(parent_module, attribute_name):
        warnings.warn(f'Attribute "{attribute_name}" has property decorator, it will be ignored')
    else:
        setattr(parent_module, attribute_name, attr)
