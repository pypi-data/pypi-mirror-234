import asyncio
import logging
import os
from typing import Any, Dict, Optional, cast

from prefect import infrastructure
from prefect.client import get_client as get_prefect_client
from prefect.deployments import Deployment
from prefect.flows import Flow
from prefect.settings import PREFECT_API_KEY, PREFECT_API_URL, Setting, temporary_settings

from ...auth.odp import InteractiveLoginTokenHandler, RopcTokenHandler
from ...compute.deploy.runtime import AbstractRuntime, Kubernetes
from ...compute.deploy.schedule import AbstractSchedule
from ...compute.deploy.storage import AbstractStorage

__all__ = ["PrefectB2cClient"]

LOG = logging.getLogger(__name__)


class PrefectB2cClient:
    """Prefect client to handle B2C SSO auth in ODP Prefect deployment"""

    def __init__(
        self,
        api_server: Optional[str] = None,
        auth_method: Optional[str] = None,
        **token_handler_kwargs: Any,
    ):
        auth_method = auth_method or os.getenv("ODP_AUTH_METHOD", "b2c")
        self._api_server = api_server

        if auth_method.lower() == "ropc":
            self._auth_cli = RopcTokenHandler(**token_handler_kwargs)
        else:
            self._auth_cli = InteractiveLoginTokenHandler(**token_handler_kwargs)

    def get_auth_token(self) -> str:
        return self._auth_cli.get_token()

    def get_prefect_config(self, api_server: str) -> Dict[Setting, str]:
        return {
            PREFECT_API_URL: api_server,
            PREFECT_API_KEY: self._auth_cli.get_token(),
        }

    def register(
        self,
        flow: Flow,
        runtime: AbstractRuntime,
        name: str,
        entrypoint: str,
        description: Optional[str] = None,
        storage: Optional[AbstractStorage] = None,
        schedule: Optional[AbstractSchedule] = None,
        api_server: Optional[str] = None,
        work_queue: Optional[str] = None,
        build: bool = True,
        dry_run: bool = False,
        **kwargs,
    ) -> Optional[str]:
        api_server = api_server or self._api_server or os.getenv("ODP_PREFECT_API")
        if not api_server:
            raise ValueError(
                "Prefect API server not set. Please set using the"
                "'api_server' argument or 'ODP_PREFECT_API' environment variable"
            )

        work_queue = work_queue or os.getenv("ODP_PREFECT_WORK_QUEUE")
        if not api_server:
            LOG.info("Prefect work queue not set, using default")
            work_queue = "default"

        if storage:
            runtime.set_storage(storage)
        elif isinstance(infrastructure, Kubernetes):
            raise ValueError("Storage is not set, but the Kubernetes runtime requires this")
        else:
            LOG.warning("Storage not set. Deployment will try to load the flows from a local file system.")

        runtime.apply_flow_options(flow)

        with temporary_settings(set_defaults=self.get_prefect_config(api_server)):
            asyncio.run(get_prefect_client().api_healthcheck())

            deployment = Deployment.build_from_flow(
                flow=flow,
                skip_upload=True,
                entrypoint=entrypoint,
                name=name,
                description=description,
                work_queue_name=work_queue,
                infrastructure=runtime.digest(),
                storage=storage.digest() if storage else None,
                schedule=schedule.digest() if schedule else None,
            )

            deployment = cast(Deployment, deployment)

            if storage and build:
                storage.build(push=not dry_run)

            if dry_run:
                return deployment.json(indent=2)

            deployment_uuid = str(deployment.apply())
            LOG.info(f"New deployment with UUID '{deployment_uuid}' uplaoded to {PREFECT_API_URL.value()}")
            return deployment_uuid
