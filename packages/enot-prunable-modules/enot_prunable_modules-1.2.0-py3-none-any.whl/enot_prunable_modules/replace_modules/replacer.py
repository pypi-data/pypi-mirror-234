from abc import ABC
from abc import abstractmethod
from typing import Optional

from torch import nn


class Replacer(ABC):
    """
    Module replacer interface.

    Replace and revert can either replace methods
    inplace or return replaced module.

    """

    @abstractmethod
    def replace(self, module: nn.Module) -> Optional[nn.Module]:
        """Replace module with its other implementation."""

    @abstractmethod
    def revert(self, module: nn.Module) -> Optional[nn.Module]:
        """Revert replacing."""
