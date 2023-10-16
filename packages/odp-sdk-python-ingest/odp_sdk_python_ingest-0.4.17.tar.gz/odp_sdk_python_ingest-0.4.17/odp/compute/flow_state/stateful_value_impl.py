"""Stateful flow and task values"""
import re
from dataclasses import dataclass, field
from typing import Any, Optional

from prefect.context import FlowRunContext, TaskRunContext, get_run_context
from prefect_kv import KVStore

__all__ = ["StatefulValue", "stateful_value"]
_VALID_BLOCK_NAME_PATTERN = "^[a-z0-9-]+$"


@dataclass
class StatefulValue:
    """Stateful value - persist values across task/flow runs"""

    name: str
    store_name: Optional[str] = None

    _value: Any = field(init=False, default=None)
    _store: Optional[KVStore] = field(init=False, repr=False, default=None)

    def __post_init__(self):
        self._store = KVStore(self.store_name or self._get_qualified_prefix())
        self.update()

    def _get_qualified_prefix(self) -> str:
        context = get_run_context()
        if isinstance(context, TaskRunContext):
            ret = "task-{}".format(context.task.name)
        elif isinstance(context, FlowRunContext):
            ret = "flow-{}".format(context.flow.name)
        else:
            raise ValueError("Invalid run context: %s", type(context).__name__)

        return ret.replace("_", "-").lower()

    @property
    def value(self) -> Any:
        """Retrieve the stateful value

        Returns:
            Value within `StatefulValue` instance
        """
        return self._value

    @value.setter
    def value(self, value: Any):
        """Set the stateful value. Value will be persisted.

        In order to not persist the value, use the `set_value`-method instead

        Args:
            value: Value to be set.
        """
        self.set_value(value, persist=True)

    def set_value(self, value: Any, persist: bool = True):
        """Set the stateful value. Optionally disable persistence. Value can be
        manually persisted later using the `persist`-method.

        Args:
            value: Value to be set
            persist: Set to `False` to not persist the value.
        """

        self._value = value
        if persist:
            self.persist()

    def get_value(self, default=None) -> Any:
        """Retrieve the stateful value, optionally return a default value

        Returns:
            Value within `StatefulValue` instance or the supplied `default`
        """
        if self._value is None:
            return default
        return self._value

    def persist(self):
        """Persist the value to the backend `KVStore`."""
        self._store.set(self.name, self._value)

    def update(self):
        """Updated the value by reading it from the backend `KVStore`"""
        self._value = self._store.get(self.name)


def stateful_value(name: str, instance_ref: Optional[str] = None, store_name: Optional[str] = None) -> StatefulValue:
    """Create a stateful value instance

    Args:
        name: Name of stateful value
        instance_ref: Optional reference to instance of stateful value
        store_name: Optional store name when stateful values are required to be referred across different tasks.

    Returns:
        Stateful value instance

    Example:

        Example task implementation using stateful values::

        ```python
        @task()
        def process_file(fname: str, f_last_updated: datetime):

            last_processed: datetime = stateful_value("last_updated", fname)

            if last_processed.value and f_last_updated > last_processed:
                ... # process file

                # Remember to update task state with new timestamp
                last_processed.value = f_last_updated
        ```

        Example tasks implementation using explicit store name when stateful values are required to be read/written
        across different tasks::

        ```python
        @task()
        def identify_file(fname: str):

            last_processed: datetime = stateful_value("last_updated", fname, "example_store")

            if last_processed.value and f_last_updated > last_processed:
                ... # Identify eligible file.

            return f_last_updated

        @task()
        def process_file(fname: str, f_last_updated: datetime):

            last_processed: datetime = stateful_value("last_updated", fname, "example_store")
            ... # process file

            # Update task state with new timestamp
            last_processed.value = f_last_updated
        ```
    """
    if instance_ref:
        name = f"{name}__{instance_ref[:64]}"

    if store_name and not re.match(_VALID_BLOCK_NAME_PATTERN, store_name):
        raise ValueError("Invalid store name. Store name must contain lowercase letters, numbers and dashes only.")

    return StatefulValue(name, store_name=store_name)
