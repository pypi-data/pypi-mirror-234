"""
CLI tool for running prefect flows
"""

import asyncio
import importlib
import importlib.util
import inspect
import logging
import os
import sys
from ast import literal_eval
from typing import Dict

import click
from prefect import Flow
from prefect.settings import temporary_settings

from odp.auth.prefect.prefect_b2c_client import PrefectB2cClient

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--verbose", is_flag=True, help="Enable verbose output. Is overloaded by --debug")
@click.option("--debug", is_flag=True, help="Enable debug-output. Overloads --verbose")
@click.option(
    "-p",
    "--param",
    multiple=True,
    callback=lambda ctx, param, value: dict(map(lambda x: x.split("="), value)),
    help="Parameter to be forwarded to flow. Basic types will be evaluated",
)
@click.option("-n", "--fn", default="main", help="Flow function name")
@click.option("--api-server", type=str, required=False, help="Prefect API url")
@click.argument("pipeline_path")
def run(
    pipeline_path: str,
    fn: str,
    param: Dict[str, str],
    api_server: str,
    verbose: bool,
    debug: bool,
) -> None:
    run_pipeline(pipeline_path, fn, param, api_server, verbose, debug)


def run_pipeline(
    pipeline_path: str,
    fn: str,
    parameters: Dict[str, str],
    api_server: str,
    verbose: bool,
    debug: bool,
) -> None:
    """Run a prefect pipeline

    Args:
        pipeline_path: Path to pipeline. Directory must contain `flow.py` and `deploy.yml`
        parameters: Parameter values
        verbose: Verbose output
        debug: Debug-output
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    click.echo(f"Running pipeline: {pipeline_path}")

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

    # Parse input parameters

    flow_parameters = set(inspect.signature(flow.fn).parameters)

    for param, value in parameters.items():
        if param not in flow_parameters:
            raise ValueError(f"The parameter '{param}' is not defined in the flow '{flow.name}'")

        try:
            parameters[param] = literal_eval(value)
        except ValueError:
            parameters[param] = value

    client = PrefectB2cClient(api_server=api_server)

    click.echo(f"Running flow '{flow.name}'")
    with temporary_settings(client.get_prefect_config(api_server)):
        if flow.isasync:
            asyncio.run(flow(**parameters))
        else:
            flow(**parameters)
