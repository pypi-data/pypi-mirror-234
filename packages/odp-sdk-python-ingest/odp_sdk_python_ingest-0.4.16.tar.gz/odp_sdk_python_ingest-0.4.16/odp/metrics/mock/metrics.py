import time
from typing import Dict, Iterable, Optional, Sequence, Union

from prometheus_client import REGISTRY, CollectorRegistry

from ..abstract_metrics import CounterABC, GaugeABC, HistogramABC

DEFAULT_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))


class MockCounter(CounterABC):
    def __init__(
        self,
        name: str,
        documentation: str,
        labelnames: Iterable[str] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
    ):
        super().__init__(name, documentation, labelnames, namespace, subsystem, unit, registry, _labelvalues)
        self._value = 0
        self._created = time.time()

    def inc(self, value: float = 1, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self.labels(**labels).inc(value=value)
        else:
            self._value += value


class MockGauge(GaugeABC):
    def __init__(
        self,
        name: str,
        documentation: str,
        labelnames: Iterable[str] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
    ):
        super().__init__(name, documentation, labelnames, namespace, subsystem, unit, registry, _labelvalues)
        self._value = 0

    def set(self, value: float, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self.labels(**labels).set(value=value)
        else:
            self._value = value

    def inc(self, value: float = 1, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self.labels(**labels).inc(value=value)
        else:
            self._value += value


class MockHistogram(HistogramABC):
    def __init__(
        self,
        name: str,
        documentation: str,
        labelnames: Iterable[str] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
        buckets: Sequence[Union[float, str]] = DEFAULT_BUCKETS,
    ):
        super().__init__(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
            _labelvalues=_labelvalues,
        )
        self.upper_bounds = buckets
        self.buckets = []
        self.sum = 0
        for b in self.upper_bounds:
            self.buckets.append({"upper_bound": b, "value": 0})

    def observe(self, value: float, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self.labels(**labels).observe(value=value)
        else:
            self.sum += 1
            for i, bound in enumerate(self.upper_bounds):
                if value <= bound:
                    self.buckets[i]["value"] += 1
                    break
