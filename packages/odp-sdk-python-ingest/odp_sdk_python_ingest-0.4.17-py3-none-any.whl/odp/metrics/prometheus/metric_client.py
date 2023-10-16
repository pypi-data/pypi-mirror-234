from os import getenv
from typing import List, Optional, Sequence, Tuple, Union

from prometheus_client import CollectorRegistry
from prometheus_client import Histogram as BasePrometheusHistogram
from prometheus_client import push_to_gateway

from odp.metrics.abstract_metrics import CounterABC, GaugeABC, HistogramABC
from odp.metrics.metric_client import MetricClient
from odp.metrics.prometheus.metrics import PrometheusCounter, PrometheusGauge, PrometheusHistogram


class PrometheusMetricClient(MetricClient):
    def __init__(self, pushgateway_url: Optional[str] = None, job_name: Optional[str] = None):
        self._pushgateway_url = pushgateway_url or getenv("ODP__METRIC_CLIENT_ARGS")
        self._job_name = job_name
        self._registry = CollectorRegistry()
        self._run = getenv("PREFECT__CONTEXT__FLOW_RUN_ID", "UNKNOWN_RUN")

    def create_counter(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
    ) -> CounterABC:
        return PrometheusCounter(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=self._registry,
        )

    def create_gauge(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
    ) -> GaugeABC:
        return PrometheusGauge(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=self._registry,
        )

    def create_histogram(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
        buckets: Sequence[Union[float, str]] = BasePrometheusHistogram.DEFAULT_BUCKETS,
    ) -> HistogramABC:
        return PrometheusHistogram(
            name=name,
            documentation=documentation,
            labelnames=labelnames,
            namespace=namespace,
            subsystem=subsystem,
            unit=unit,
            registry=self._registry,
            buckets=buckets,
        )

    def push_metrics(self):
        push_to_gateway(self._pushgateway_url, self._job_name, self._registry)
