from prefect.flows import Flow
from prefect.orion.schemas.schedules import CronSchedule

from .abstract_schedule import AbstractSchedule


class Cron(AbstractSchedule):
    def __init__(
        self,
        flow: Flow,
        cron: str,
        timezone: str,
    ):
        super().__init__(flow)

        self._cron = cron
        self._timezone = timezone

    def digest(self) -> CronSchedule:
        return CronSchedule(cron=self._cron, timezone=self._timezone)
