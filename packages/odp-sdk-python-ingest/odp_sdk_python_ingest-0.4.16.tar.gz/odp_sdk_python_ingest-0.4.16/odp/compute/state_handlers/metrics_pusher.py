import logging
import threading
import time
from typing import Dict, Optional

from prefect import Task
from prefect.engine.state import State

from odp.compute.metrics import Metrics

LOG = logging.getLogger(__name__)


class MetricsPusher:
    def __init__(self, push_interval: int = 1, thread_kwargs: Optional[Dict] = None):
        self.push_interval = push_interval
        self.thread_kwargs = thread_kwargs or {}
        self.thread: Optional[MetricsPusherThread] = None

    def state_handler_cb(self, task: Task, old_state: State, new_state: State) -> None:
        if new_state.is_finished():
            self.thread.stop(timeout=2 * self.push_interval)
        elif old_state.is_pending() and new_state.is_running():
            self.thread = MetricsPusherThread(push_interval=self.push_interval, **self.thread_kwargs)
            self.thread.start()

    def __call__(self, task: Task, old_state: State, new_state: State) -> None:
        self.state_handler_cb(task, old_state, new_state)


class MetricsPusherThread(threading.Thread):
    def __init__(self, push_interval: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_interval = push_interval
        self.keep_alive = False

    def start(self) -> None:
        self.keep_alive = True
        super().start()

    def stop(self, wait: bool = True, timeout: Optional[float] = None):
        self.keep_alive = False

        if wait:
            self.join(timeout=timeout)

    def run(self) -> None:
        last_cycle = 0

        while self.keep_alive:
            t = time.time()
            dt = t - last_cycle
            if dt < self.push_interval:
                time.sleep(self.push_interval - dt)
            elif dt >= (1.1 * self.push_interval) and last_cycle > 0:
                LOG.warning(
                    f"{self.__class__.__name__} cycle time exceeded expected interval: {dt} > {self.push_interval}"
                )

            Metrics.push(False)
            last_cycle = t
