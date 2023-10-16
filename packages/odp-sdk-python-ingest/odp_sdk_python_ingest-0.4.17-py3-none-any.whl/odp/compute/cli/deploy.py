"""
CLI tool for deploying prefect deployments
"""
import logging
import os
from io import StringIO
from typing import Any, Callable, Dict, List, Optional, Union, cast
from uuid import uuid4

import click
from jinja2 import StrictUndefined, Template
from prefect import Flow
from yaml import safe_load

from ...auth.prefect import PrefectB2cClient
from ...utils import import_prefect_flow_from_file
from ..deploy import create_deployment_block
from ..deploy.runtime import AbstractRuntime
from ..deploy.schedule import AbstractSchedule
from ..deploy.storage import AbstractStorage
from .context import CliContext

LOG = logging.getLogger(__name__)

DEFAULT_VALUES = {
    "storage.registry": "oceandata.azurecr.io",
    "storage.image_name": lambda flow, context: f"prefect-{flow.name}",
    "storage.image_tag": lambda flow, context: uuid4().hex,
    "storage.env_vars": {"PYTHONPATH": "$PYTHONPATH:./"},
}


def join_field(
    old_value: Optional[Union[str, Dict, List]], new_value: Union[str, Dict, List]
) -> Union[str, Dict, List]:
    """Join two values

    Args:
        old_value: Old value or `None`
        new_value: New value

    Returns:
        `new_value` if `old_value` is `None` or a simple type. Concatenate
        `old_value` and `new_value` otherwise
    """
    if old_value:
        assert type(old_value) == type(new_value)
        assert new_value is not None

        if isinstance(old_value, str):
            # Replace string
            return new_value
        elif isinstance(old_value, dict):
            # Concatenate dicts
            return dict(**old_value, **new_value)  # type: ignore
        elif isinstance(old_value, list):
            # Concatenate lists, remove duplicates
            ret = sorted(old_value + new_value)  # type: ignore
            return list(set(ret))
        else:
            raise ValueError("Invalid type: " + type(old_value).__name__)
    else:
        # Old value not set, simply return new value
        return new_value


def auto_populate(
    dct: Dict[str, Any],
    field: Union[List[str], str],
    value: Union[str, Callable[[Flow, CliContext], str]],
    flow: Flow,
    context: CliContext,
) -> None:
    """Set a field value for a nested dict, either by value or callback

    Can set field value in nested dict by using dot-syntax:

    ```python
    >>> dct["my.key.value"]
    # Translates to
    >>> dct["my"]["key"]["value"]
    ```

    Args:
        dct: Dict to be set
        field: Field to be set
        value: Value or callable to be set field
        flow: Flow used by value callback
        context: Client context
    """

    if isinstance(field, str):
        field = field.split(".")

    if len(field) == 0:
        return
    elif len(field) > 1:
        try:
            return auto_populate(dct[field[0]], field[1:], value, flow, context)
        except KeyError:
            LOG.info(f"The field '{field[0]}' is not set")
            return

    field = field[0]

    if isinstance(value, Callable):
        value = value(flow, context)

    dct[field] = join_field(dct.get(field), value)


@click.command()
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Build docker image, but don't deploy to prefect server",
)
@click.option("--api-server", type=str, required=False, help="Prefect API url")
@click.option(
    "--ensure-project",
    is_flag=True,
    help="Set this flag to ensure that the project exists before deploying the flow",
)
@click.option("--verbose", is_flag=True, help="Enable verbose output. Is overloaded by --debug")
@click.option("--debug", is_flag=True, help="Enable debug-output. Overloads --verbose")
@click.argument("pipeline_paths", nargs=-1)
def deploy(
    pipeline_paths: List[str],
    api_server: str,
    dry_run: bool,
    ensure_project: bool,
    verbose: bool,
    debug: bool,
):
    for pipeline_path in pipeline_paths:
        deploy_pipeline(
            pipeline_path.rstrip("/"),
            api_server,
            dry_run,
            verbose,
            debug,
        )


def deploy_pipeline(
    pipeline_path: str,
    api_server: str,
    dry_run: bool,
    verbose: bool,
    debug: bool,
):
    """Deploy a prefect pipeline

    Args:
        pipeline_path: Path to pipeline. Directory must contain `flow.py` and `deploy.yml`
        api_server: Prefect API hostname
        dry_run: Build, but do not deploy pipeline to prefect
        api_server: URL of Prefect apollo API to deploy to
        ensure_project: Ensure project exists before attempting to deploy the flow
        verbose: Verbose output
        debug: Debug-output
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    click.echo(f"Deploying pipeline: {pipeline_path}")

    pipeline_abspath = os.path.abspath(pipeline_path)

    # Import flow

    flow_module, flow = import_prefect_flow_from_file(pipeline_path, flow_cb="main")

    context = CliContext(
        {
            "flow_dir": pipeline_abspath,
            "flow_file": os.path.join(pipeline_abspath, "flow.py"),
            "flow_name": flow.name,
            "flow": flow,
            "flow_module": flow_module,
            "deploy_config": os.path.join(pipeline_abspath, "deploy.yml"),
        }
    )

    with open(context["deploy_config"], "r") as f:  # type: ignore
        template = Template(f.read(), undefined=StrictUndefined)
        rendered_config = template.render(context.to_dict())
    with StringIO(rendered_config) as stream:
        data = safe_load(stream)

    ignore_default_values = set(data.pop("ignore_default_values", []))

    # Load metadata-field

    metadata = data.pop("metadata")

    for field, value in DEFAULT_VALUES.items():
        if field in ignore_default_values:
            LOG.info(f"Ignoring default value for field '{field}'")
            continue
        auto_populate(data, field, value, flow, context)

    client = PrefectB2cClient(api_server)

    runtime = cast(
        Optional[AbstractRuntime],
        create_deployment_block(flow, data.pop("runtime", {})),
    )
    storage = cast(
        Optional[AbstractStorage],
        create_deployment_block(flow, data.pop("storage", {}), fail_if_empty=False),
    )
    schedule = cast(
        Optional[AbstractSchedule],
        create_deployment_block(flow, data.pop("schedule", {}), fail_if_empty=False),
    )

    if not runtime:
        raise ValueError("Missing mandatory config field 'runtime' is not set")

    flow_qualified_name = storage.flow_qualified_name(flow)

    registered_deployment = client.register(
        flow=flow,
        work_queue=metadata.get("workQueue", "default"),
        runtime=runtime,
        name=metadata["name"],
        description=metadata.get("description"),
        entrypoint="/opt/prefect/flows/{}.py:{}".format(flow_qualified_name, flow_qualified_name),  # type: ignore
        storage=storage,
        schedule=schedule,
        build=True,
        dry_run=dry_run,
    )

    if dry_run:
        click.echo("Prefect deployment: ")
        click.echo(registered_deployment)
    else:
        click.echo(f"New deployment with UUID '{registered_deployment}' uplaoded to {api_server}")
