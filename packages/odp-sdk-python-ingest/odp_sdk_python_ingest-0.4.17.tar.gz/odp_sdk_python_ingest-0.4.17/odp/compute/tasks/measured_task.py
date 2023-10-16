from functools import partial
from typing import Callable

from prefect import Task

from odp.compute.metrics import Metrics

__all__ = ["MeasuredTask"]


class MeasuredTask(Task):
    DEFAULT_METRIC_NAMESPACE = "prefect"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.run = partial(self._run_wrapper, self.run)
        self._run_time_metric = Metrics.distribution(
            MeasuredTask.DEFAULT_METRIC_NAMESPACE,
            "run_time",
            ["flow", "flow_id", "task", "task_id", "flow_run_id", "task_run_id"],
        )

    @staticmethod
    def _run_wrapper(fn: Callable, **kwargs):
        ret = fn(**kwargs)
        Metrics.push()

        return ret
