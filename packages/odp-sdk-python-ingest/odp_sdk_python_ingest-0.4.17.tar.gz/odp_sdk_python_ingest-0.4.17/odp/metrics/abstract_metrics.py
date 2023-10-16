from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from prometheus_client import REGISTRY, CollectorRegistry
from prometheus_client.metrics import _build_full_name, _validate_labelnames


class MetricABC(ABC):
    """Base class for all metrics"""

    _type: str = None
    _reserved_labelnames = []

    def _is_parent(self):
        """Return a boolean indicating if the metric has children metrics."""
        return self._labelnames and not self._labelvalues

    def __init__(
        self,
        name: str,
        documentation: str,
        labelnames: Union[List[str], Tuple[str]] = (),
        namespace: str = "",
        subsystem: str = "",
        unit: str = "",
        registry: Optional[CollectorRegistry] = REGISTRY,
        _labelvalues: Optional[Sequence[str]] = None,
    ):
        self._name = _build_full_name(self._type, name, namespace, subsystem, unit)
        self._labelnames = _validate_labelnames(self, labelnames)
        self._labelvalues = tuple(_labelvalues or ())
        self._documentation = documentation
        self._unit = unit
        if self._is_parent():
            self._metrics: Dict[Sequence[str], "MetricABC"] = {}

    def labels(self, *labelvalues: Any, **labelkwargs: Any) -> "MetricABC":
        """Inspired from the prometheus metrics. Return the child for the given labelset.
        All metrics can have labels, allowing grouping of related time series.

        See the best practices on [naming](http://prometheus.io/docs/practices/naming/)
        and [labels](http://prometheus.io/docs/practices/instrumentation/#use-labels).

        Args:
            *labelvalues: Label values
            **labelkwargs: Label kwargs

        Returns:
            A object from the same metric class.
        """
        if not self._labelnames:
            raise ValueError("No label names were set when constructing %s" % self)
        if self._labelvalues:
            raise ValueError(
                "{} already has labels set ({}); can not chain calls to .labels()".format(
                    self, dict(zip(self._labelnames, self._labelvalues))
                )
            )
        if labelvalues and labelkwargs:
            raise ValueError("Can't pass both *args and **kwargs")
        if labelkwargs:
            if sorted(labelkwargs) != sorted(self._labelnames):
                raise ValueError("Incorrect label names")
            labelvalues = tuple(str(labelkwargs[label]) for label in self._labelnames)
        else:
            if len(labelvalues) != len(self._labelnames):
                raise ValueError("Incorrect label count")
            labelvalues = tuple(str(label) for label in labelvalues)
        if labelvalues not in self._metrics:
            self._metrics[labelvalues] = self.__class__(
                self._name,
                documentation=self._documentation,
                labelnames=self._labelnames,
                unit=self._unit,
                _labelvalues=labelvalues,
            )
        return self._metrics[labelvalues]


class CounterABC(MetricABC):
    """Base class for all counters.

    A counter is a cumulative metric that represents a single numerical value that only ever goes up. A counter is
    typically used to count requests served, tasks completed, errors occurred, etc. Counters should not be used to
    expose current counts of items whose number can also go down, e.g. the number of currently running coroutines.
    """

    @abstractmethod
    def inc(self, value: float = 1, labels: Dict[str, str] = None):
        """Increment the counter by the given value.

        Args:
            value: Value to increment the counter by.
            labels: dict with label name as key, label value as value
        """


class GaugeABC(MetricABC):
    """Base class for all gauges.

    A gauge is a metric that represents a single numerical value that can arbitrarily go up and down. Gauges are
    typically used to represent current counts of items, e.g. the number of currently running coroutines.
    """

    @abstractmethod
    def set(self, value: float, labels: Dict[str, str] = None):
        ...

    @abstractmethod
    def inc(self, value: float = 1, labels: Dict[str, str] = None):
        ...

    def dec(self, value: float = 1, labels: Dict[str, str] = None):
        self.inc(value=-value, labels=labels)


class HistogramABC(MetricABC):
    """Base class for all histograms.

    A histogram is a metric that represents the distribution of a set of values over time. Histograms are typically
    used to track request latencies, response sizes, etc.
    """

    @abstractmethod
    def observe(self, value: float, labels: Dict[str, str] = {}):
        ...
