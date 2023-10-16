from datetime import datetime, timedelta
from typing import Union

import isodate
from prefect.flows import Flow
from prefect.orion.schemas.schedules import IntervalSchedule

from .abstract_schedule import AbstractSchedule


class Interval(AbstractSchedule):
    def __init__(
        self,
        flow: Flow,
        interval: Union[str, timedelta],
        anchor: Union[str, datetime],
    ):
        super().__init__(flow)

        self._interval = self._parse_timedelta(interval)
        self._anchor = self._parse_datetime(anchor)

    def digest(self) -> IntervalSchedule:
        return IntervalSchedule(interval=self._interval, anchor_date=self._anchor)

    @staticmethod
    def _parse_timedelta(dt: Union[str, timedelta]) -> timedelta:
        if isinstance(dt, timedelta):
            return dt
        return isodate.parse_duration(dt)

    @staticmethod
    def _parse_datetime(t: Union[str, datetime]) -> datetime:
        if isinstance(t, datetime):
            return t
        return isodate.parse_datetime(t)
