from typing import Dict, Iterable, Optional, Sequence, Union

from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client import Counter as BasePrometheusCounter
from prometheus_client import Gauge as BasePrometheusGauge
from prometheus_client import Histogram as BasePrometheusHistogram

from odp.metrics.abstract_metrics import CounterABC, GaugeABC, HistogramABC


class PrometheusCounter(CounterABC):
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
        self._counter = BasePrometheusCounter(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
        )

    def inc(self, value: float = 1, labels: Optional[Dict[str, Union[str, int, float]]] = None):
        if labels:
            self._counter.labels(**labels).inc(value)
        else:
            self._counter.inc(value)


class PrometheusGauge(GaugeABC):
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
        self._gauge = BasePrometheusGauge(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
        )

    def set(self, value: float, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self._gauge.labels(**labels).set(value=value)
        else:
            self._gauge.set(value=value)

    def inc(self, value: float = 1, labels: Optional[Dict[str, Union[str, int, float]]] = None) -> None:
        if labels:
            self._gauge.labels(**labels).inc(amount=value)
        else:
            self._gauge.inc(amount=value)


class PrometheusHistogram(HistogramABC):
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
        buckets: Sequence[Union[float, str]] = BasePrometheusHistogram.DEFAULT_BUCKETS,
    ):
        super().__init__(name, documentation, labelnames, namespace, subsystem, unit, registry, _labelvalues)
        self._histogram = BasePrometheusHistogram(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=registry,
            buckets=buckets,
        )

    def observe(self, value: float = 1, labels: Optional[Dict[str, Union[str, int, float]]] = None):
        if labels:
            self._histogram.labels(**labels).observe(amount=value)
        else:
            self._histogram.observe(amount=value)
