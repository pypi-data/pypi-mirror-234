from abc import abstractmethod
from typing import Dict, Optional

from prefect.blocks.core import Block
from prefect.flows import Flow
from slugify import slugify

from ..abstract_deployment_block import AbstractDeploymentBlock


class AbstractStorage(AbstractDeploymentBlock):
    def __init__(self, flow: Optional[Flow] = None):
        self._flows: Dict[str, Flow] = {}

        if flow:
            self.add_flow(flow)

    def add_flow(self, flow: Flow) -> str:
        if flow.name in self._flows:
            raise ValueError(f"Name conflict: Flow with name '{flow.name}' is already present")

        self._flows[flow.name] = flow
        return flow.name

    @abstractmethod
    def build(self, push: bool = False) -> str:
        ...

    @abstractmethod
    def digest(self) -> Optional[Block]:
        ...

    @staticmethod
    def flow_qualified_name(flow: Flow) -> str:
        return slugify(flow.name).replace("-", "_")
