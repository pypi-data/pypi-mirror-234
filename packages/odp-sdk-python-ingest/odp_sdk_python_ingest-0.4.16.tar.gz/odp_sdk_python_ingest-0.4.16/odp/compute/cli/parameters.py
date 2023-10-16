"""
CLI tool for reading prefect flow parameter list
"""
import importlib
import importlib.util
import inspect
import logging
import os
import sys
from typing import cast

import click
from prefect import Flow

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--verbose", is_flag=True, help="Enable verbose output. Is overloaded by --debug")
@click.option("--debug", is_flag=True, help="Enable debug-output. Overloads --verbose")
@click.option("-n", "--fn", default="main", help="Flow function name")
@click.argument("pipeline_path")
def parameters(
    pipeline_path: str,
    fn: str,
    verbose: bool,
    debug: bool,
) -> None:
    get_parameters(pipeline_path, fn, verbose, debug)


def get_parameters(
    pipeline_path: str,
    fn: str,
    verbose: bool,
    debug: bool,
) -> None:
    """Print list of parameters

    Args:
        pipeline_path: Path to pipeline. Directory must contain `flow.py` and `deploy.yml`
        verbose: Verbose output
        debug: Debug-output
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    click.echo(f"Extracting parameters from pipeline: {pipeline_path}")

    # Import flow

    # Import flow

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

    flow: Flow = getattr(flow_module, fn)

    for pname, param in dict(inspect.signature(flow.fn).parameters).items():
        param = cast(inspect.Parameter, param)
        has_default = param.default is not inspect._empty

        cols = [f"name='{pname}'", f"required={not has_default}"]

        if has_default:
            cols.append(
                "default={delim}{value}{delim}".format(
                    delim="'" if isinstance(param.default, str) else "",
                    value=param.default,
                )
            )
        click.echo("  Parameter: {}".format(", ".join(cols)))
