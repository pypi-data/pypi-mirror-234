from typing import Type

from prefect.blocks.core import Block
from prefect.utilities.importtools import import_object

from ..abstract_deployment_block import AbstractDeploymentBlock


class GenericBlock(AbstractDeploymentBlock):
    def __init__(self, cls: str, name: str):
        cls: Type[Block] = import_object(cls)

        assert issubclass(cls, Block)
        self._cls = cls
        self._name = name

    def digest(self) -> Block:
        return self._cls.load(self._name)  # type: ignore
