from abc import abstractmethod

from prefect.flows import Flow
from prefect.orion.schemas.schedules import SCHEDULE_TYPES

from ..abstract_deployment_block import AbstractDeploymentBlock


class AbstractSchedule(AbstractDeploymentBlock):
    """Deployment config schedule block"""

    def __init__(self, flow: Flow):
        self._flow = flow

    @abstractmethod
    def digest(self) -> SCHEDULE_TYPES:
        ...
