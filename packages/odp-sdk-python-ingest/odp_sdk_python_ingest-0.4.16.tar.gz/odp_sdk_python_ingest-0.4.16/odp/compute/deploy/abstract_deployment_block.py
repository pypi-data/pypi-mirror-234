from abc import ABC, abstractmethod
from typing import Any


class AbstractDeploymentBlock(ABC):
    """Simple superclass for deployment config-blocks"""

    @abstractmethod
    def digest(self) -> Any:
        ...
