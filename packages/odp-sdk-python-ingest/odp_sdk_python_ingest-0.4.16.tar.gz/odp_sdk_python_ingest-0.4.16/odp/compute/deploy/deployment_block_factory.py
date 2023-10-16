import importlib
from typing import Any, Dict, Optional

from prefect.flows import Flow

from .abstract_deployment_block import AbstractDeploymentBlock


def create_deployment_block(
    flow: Flow, config: Dict[str, Any], fail_if_empty: bool = True
) -> Optional[AbstractDeploymentBlock]:
    """Create a deployment block from a config-dict. Must include the field `cls`

    Args:
        flow: Flow used to initialze the returned deployment block
        config: Config used to initialize the deployment block. The field `cls` must be set,
            and is used to load the class-reference which is initialized.

    Returns:
        New deployment block corresponding to the referenced `cls`-key in `config`.

    Raises:
        KeyError: Raised if the `cls`-key is missing
        ValueError: The supplied config was empty
    """

    if not config:
        if fail_if_empty:
            raise ValueError("The block input config was empty")
        else:
            return None

    # Copy the input-dict in order to avoid making changes to downstream objects
    config = config.copy()

    try:
        # Get the class-reference
        cls = config.pop("cls")
    except KeyError as e:
        raise KeyError("Missing mandatory field 'cls'") from e

    # Separate module path and classname
    cls = cls.split(".")
    cls, module = cls[-1], ".".join(cls[:-1])

    # Import module in order to obtain the class-object
    module = importlib.import_module(module)
    cls = getattr(module, cls)

    # Initialize object using the config as kwargs
    return cls(flow, **config)
