import logging
import os
from typing import Any, Dict, List, Optional, Union

import inflection
import toml

LOG = logging.getLogger(__name__)


class CliContext:
    """Semi-global context used by cli for common values such as flow dir, etc

    Instances will hold an internal context, and will fallback to a global context if attribute is not found.
    The global context is set by environment variables, prefixed by `CliContext.ENVIRONMENT_VAR_NAME_PREFIX`
    """

    ENVIRONMENT_VAR_NAME_PREFIX = "ODP__"
    PYPROJECT_PACKAGE_PREFIX = "pyproject."

    class Undefined:
        pass

    def __init__(
        self,
        internal_context: Optional[Dict[str, Any]] = None,
        load_pyproject: bool = True,
    ):
        self._internal_context = internal_context or {}

        if load_pyproject:
            self._load_pyproject()

    @staticmethod
    def _get_package_version(version: List[Dict]) -> Optional[str]:
        """Parse the package version type

        Args:
            version: Version object, typically a `str` or `List[Dict]`

        Returns:
            Package version
        """
        if isinstance(version, str):
            return version.lstrip("^")
        if isinstance(version, list):
            for e in version:
                if e["platform"] == "linux":  # Docker build will always be a linux-platform
                    return e["version"].lstrip("^")

        return None

    def _load_pyproject(self) -> None:
        """Load python packages from pyproject-file"""

        dct = toml.load(open("pyproject.toml", "r"))
        packages = dct["tool"]["poetry"]["dependencies"]

        context = {
            inflection.underscore(key): f"{key}=={self._get_package_version(value)}" for key, value in packages.items()
        }

        self._internal_context["pyproject"] = {key: val for key, val in context.items() if val is not None}

    def __getitem__(self, attribute: str) -> Optional[str]:
        """Wraps `Context.get_attribute`

        Will raise an `AttributeError` if `attribute` is not found

        Args:
            attribute: Attribute name

        Returns:
            Attribute value
        """
        return self.get_attribute(attribute)

    def __setitem__(self, attribute: str, value: Any):
        """Set context attribute

        Args:
            attribute: Attribute name
            value: Attribute value
        """

        if attribute in self._internal_context:
            raise ValueError(f"Attribute '{attribute}' already exist in this context")

        self._internal_context[attribute] = value

    def set_internal_attribute(self, attribute: str, value: Any) -> None:
        """Set an attribute in the internal context

        Args:
            attribute: Attribute name
            value: Attribute value
        """
        assert attribute not in self._internal_context
        self._internal_context[attribute] = value

    def _attempt_internal(self, attribute: str) -> Any:
        return self._internal_context.get(attribute, CliContext.Undefined)

    def _attempt_global(self, attribute: str) -> Any:
        key = inflection.underscore(attribute).upper()
        LOG.debug(
            "Attempting to retrieve environment variable '%s' for attribute '%s",
            key,
            attribute,
        )

        return os.getenv(key, CliContext.Undefined)

    def get_attribute(self, attribute: str, raise_if_not_exists: bool = True) -> Union[None, Any]:
        """Get context attribute

        Args:
            attribute: Attribute name
            raise_if_not_exists: Will raise an `AttributeError` if `attribute` does not exist when set to true,
                                 will return `None` otherwise

        Returns:
            Attribute value or `None` if `attribute` is not found and `raise_if_not_exists` is `True`
        """
        ret = self._attempt_internal(attribute)
        if ret != CliContext.Undefined:
            return ret

        LOG.debug(
            "Failed to retrieve attribute '%s' from internal context attempting global context instead",
            attribute,
        )

        ret = self._attempt_global(attribute)
        if ret != CliContext.Undefined:
            return ret

        LOG.warning(
            "Failed to retrieve attribute '%s' from internal and global contexts attempting global context instead",
            attribute,
        )

        if raise_if_not_exists:
            raise AttributeError(f"Failed to retrieve attribute '{attribute}' from internal and glob contexts")
        else:
            return None

    def to_dict(self):
        """Collect context into dict

        Returns:
            Dict representing context snapshot
        """
        environment_variables = {
            key.lstrip(self.ENVIRONMENT_VAR_NAME_PREFIX).lower(): value
            for key, value in os.environ.items()
            if key.startswith(self.ENVIRONMENT_VAR_NAME_PREFIX)
        }

        return dict(**environment_variables, **self._internal_context)
