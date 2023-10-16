from typing import List, Optional, Sequence, Tuple, Union

from prometheus_client import REGISTRY, CollectorRegistry

from odp.metrics.abstract_metrics import CounterABC
from odp.metrics.metric_client import MetricClient
from odp.metrics.mock.metrics import DEFAULT_BUCKETS, MockCounter, MockGauge, MockHistogram


class MockMetricClient(MetricClient):
    def __init__(self, job_name: Optional[str] = None):
        self.metrics = []
        self._job_name = job_name

    def create_counter(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
    ) -> CounterABC:
        counter = MockCounter(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
        )
        self.metrics.append(counter)
        return counter

    def create_gauge(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
    ):
        gauge = MockGauge(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
            _labelvalues=_labelvalues,
        )
        self.metrics.append(gauge)
        return gauge

    def create_histogram(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
        buckets: Sequence[Union[float, str]] = DEFAULT_BUCKETS,
    ):
        histogram = MockHistogram(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
            _labelvalues=_labelvalues,
            buckets=buckets,
        )
        self.metrics.append(histogram)
        return histogram

    def push_metrics(self):
        print(f"MOCK -- Job: {self._job_name}")
        for metric in self.metrics:
            print(metric.__dict__())
