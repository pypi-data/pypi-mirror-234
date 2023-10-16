from abc import abstractmethod

from prefect.flows import Flow
from prefect.infrastructure import Infrastructure

from ..abstract_deployment_block import AbstractDeploymentBlock


class AbstractRuntime(AbstractDeploymentBlock):
    """Deployment config runtime block"""

    def __init__(self, flow: Flow):
        self._flow = flow

    @abstractmethod
    def digest(self) -> Infrastructure:
        ...

    def apply_flow_options(self, flow: Flow) -> Flow:
        return flow
