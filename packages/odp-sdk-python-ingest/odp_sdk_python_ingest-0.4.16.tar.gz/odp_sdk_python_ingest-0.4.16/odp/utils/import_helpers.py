import importlib
import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Tuple

from prefect.flows import Flow


def import_prefect_flow_from_file(pipeline_path: str, flow_cb: str = "main") -> Tuple[str, Flow]:
    """Import a prefect flow from a file path.

    Args:
        pipeline_path: Path to `.py`-file containing flow, or a directory. If a directory is specified,
            then the flow is assumed to be in `flow.py` within the specified directory
        flow_cb: Name of function with the `@flow`-decorator

    Returns:
        Imported flow

    Raises:
        ImportError: Failed to import flow for some reason
    """

    _, ext = os.path.splitext(pipeline_path)
    if ext != ".py":
        module_path = os.path.join(pipeline_path, "flow.py")
    else:
        module_path = pipeline_path

    if not os.path.exists(module_path):
        raise ImportError(f"The module '{module_path}' does not exist")

    module_name, _ = os.path.splitext(os.path.split(module_path)[-1])

    spec = importlib.util.spec_from_file_location(f"flows.{module_name}", module_path)
    if not spec or not spec.loader:
        raise ImportError(f"Failed to import flow from file '{module_path}'")

    sys.path.append(os.path.abspath(pipeline_path))
    flow_module = importlib.util.module_from_spec(spec)
    if not flow_module:
        raise ImportError(f"Failed to import flow from module spec '{spec.name}'")

    spec.loader.exec_module(flow_module)

    flow_module_name = ".".join(flow_module.__name__.split(".")[:-1])
    return flow_module_name, getattr(flow_module, flow_cb)


def load_script_as_module(path: str) -> ModuleType:
    """
    Execute a script at the given path.
    Sets the module name to `__odp_loader__`.
    If an exception occurs during execution of the script, an
    `ImportError` is created to wrap the exception and raised.
    During the duration of this function call, `sys` is modified to support loading.
    These changes are reverted after completion, but this function is not thread safe
    and use of it in threaded contexts may result in undesirable behavior.
    See https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

    Yanked from Prefect:
    https://github.com/PrefectHQ/prefect/blob/dd72aed27b44dd6ba6cc05d9e8c5744030e24bbf/src/prefect/utilities/importtools.py#L120
    """
    # We will add the parent directory to search locations to support relative imports
    # during execution of the script
    parent_path = str(Path(path).resolve().parent)
    working_directory = os.getcwd()

    spec = importlib.util.spec_from_file_location(
        "__odp_loader__",
        path,
        # Support explicit relative imports i.e. `from .foo import bar`
        submodule_search_locations=[parent_path, working_directory],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["__odp_loader__"] = module

    # Support implicit relative imports i.e. `from foo import bar`
    sys.path.insert(0, working_directory)
    sys.path.insert(0, parent_path)

    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop("__odp_loader__")
        sys.path.remove(parent_path)
        sys.path.remove(working_directory)

    return module


def load_module(module_name: str) -> ModuleType:
    """
    Import a module with support for relative imports within the module.

    Yanked from Prefect:
    https://github.com/PrefectHQ/prefect/blob/dd72aed27b44dd6ba6cc05d9e8c5744030e24bbf/src/prefect/utilities/importtools.py#L165
    """
    # Ensure relative imports within the imported module work if the user is in the
    # correct working directory
    working_directory = os.getcwd()
    sys.path.insert(0, working_directory)

    try:
        return importlib.import_module(module_name)
    finally:
        sys.path.remove(working_directory)


def import_object(import_path: str):
    """
    Load an object from an import path.
    Import paths can be formatted as one of:
    - module.object
    - module:object
    - /path/to/script.py:object
    This function is not thread safe as it modifies the 'sys' module during execution.

    Yanked from Prefect:
    https://github.com/PrefectHQ/prefect/blob/dd72aed27b44dd6ba6cc05d9e8c5744030e24bbf/src/prefect/utilities/importtools.py#L180
    """
    if ".py:" in import_path:
        script_path, object_name = import_path.rsplit(":", 1)
        module = load_script_as_module(script_path)
    else:
        if ":" in import_path:
            module_name, object_name = import_path.rsplit(":", 1)
        elif "." in import_path:
            module_name, object_name = import_path.rsplit(".", 1)
        else:
            raise ValueError(f"Invalid format for object import. Received {import_path!r}.")

        module = load_module(module_name)

    return getattr(module, object_name)
