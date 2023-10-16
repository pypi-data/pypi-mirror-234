import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from odp.metrics.abstract_metrics import CounterABC, GaugeABC, HistogramABC
from odp.utils.import_helpers import import_object


class MetricClient(ABC):
    """Base class for metric clients"""

    @abstractmethod
    def create_counter(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
    ) -> CounterABC:
        """Base method to create a counter from the metric client"""

    @abstractmethod
    def create_gauge(
        self, name: str, documentation: str, labels: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> GaugeABC:
        """Base method to create a gauge from the metric client"""

    @abstractmethod
    def create_histogram(
        self, name: str, description: str, labels: Optional[Dict[str, Union[str, int, float]]] = None
    ) -> HistogramABC:
        """Base method to create a gauge from the metric client"""

    @abstractmethod
    def push_metrics(self):
        """Base method to push metrics"""


def metric_client_factory(client_cls: Optional[str] = None, **kwargs: Any) -> MetricClient:
    """Instantiate a metrics object based on a given class name.
    The function will attempt to instantiate the metrics object from the environment variable `ODP_METRICS_CLASS` if no
    class name is given. If the environment variable is not set, the function will fall back to the default class name
    `odp.metrics.mock.metric_client.MockMetricClient`.
    Caller can pass keyword arguments to the metrics object constructor, which will override any environment variables.
    If no keyword arguments are passed, the metrics object will be instantiated from environment variables.
    Args:
        client_cls: The class name of the metrics object to instantiate.
        **kwargs: Keyword arguments to pass to the metrics object constructor.
    Returns:
        A metrics object.
    """
    client_cls_path = client_cls or os.getenv(
        "ODP__METRIC_CLIENT_CLS", "odp.metrics.mock.metric_client.MockMetricClient"
    )
    cls: MetricClient = import_object(client_cls_path)
    return cls(**kwargs)
