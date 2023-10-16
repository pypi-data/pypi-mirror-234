import filecmp
import json
import logging
import os
import shutil
import sys
import textwrap
import uuid
import warnings
from datetime import datetime
from tempfile import TemporaryDirectory
from typing import Dict, Iterable, List, Optional, Tuple

import cloudpickle
import docker
import prefect
from prefect.blocks.core import Block
from prefect.flows import Flow
from slugify import slugify

from ..block import GenericBlock
from .abstract_storage import AbstractStorage

PREFECT_DIR = "/opt/prefect"
PREFECT_PLATFORM = "linux/amd64"
LOG = logging.getLogger(__name__)


def _multiline_indent(string: str, spaces: int = 4) -> str:
    return string.replace("\n", "\n" + spaces * " ")


def _get_default_base_image() -> str:
    return "prefecthq/prefect:{}-python{}.{}".format(
        prefect.__version__, sys.version_info.major, sys.version_info.minor
    )


class Docker(AbstractStorage):
    ENV_DOCKER_HOST = "DOCKER_HOST"
    ENV_CONTAINER_REGISTRY = "CONTAINER_REGISTRY"

    DEFAULT_BASE_IMAGE = _get_default_base_image()

    def __init__(
        self,
        flow: Optional[Flow] = None,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        base_image: str = DEFAULT_BASE_IMAGE,
        registry: Optional[str] = None,
        dockerfile: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        python_dependencies: Optional[List[str]] = None,
        installation_commands: Optional[List[str]] = None,
        files: Optional[Dict[str, str]] = None,
        extra_dockerfile_commands: Optional[List[str]] = None,
        runtime_storage_block: Optional[Dict[str, str]] = None,
        install_cwd: bool = True,
    ) -> None:
        super().__init__(flow)
        self._image_name = image_name
        self._image_tag = image_tag
        self._base_image = base_image
        self._registry = registry or os.environ.get(self.ENV_CONTAINER_REGISTRY)
        self._dockerfile = dockerfile
        self._env_vars = env_vars
        self._python_dependencies = python_dependencies
        self._installation_commands = installation_commands
        self._copy_files = files
        self._extra_dockerfile_commands = extra_dockerfile_commands
        self._ignore_healthchecks = False
        self._prefect_directory = "/opt/prefect"
        self._install_cwd = install_cwd

        if runtime_storage_block:
            self._runtime_storage_block = GenericBlock(**runtime_storage_block)
        else:
            self._runtime_storage_block = None

    def get_name(self) -> str:
        return f"{self._registry}/{self._image_name}:{self._image_tag}"

    def digest(self) -> Optional[Block]:
        if self._runtime_storage_block:
            return self._runtime_storage_block.digest()
        return None

    def _get_client(self, registry_url: Optional[str] = None, tls: bool = False) -> docker.APIClient:
        if sys.platform == "win32":
            default_url = "npipe:////./pipe/docker_engine"
        else:
            default_url = "unix://var/run/docker.sock"

        base_url = registry_url or os.environ.get(self.ENV_DOCKER_HOST, default_url)

        return docker.APIClient(base_url=base_url, version="auto", tls=tls)

    def _create_dockerfile_object(self, dir: str) -> str:
        if self._dockerfile:
            with open(self._dockerfile, "r") as fd:
                base_commands = fd.read()
        else:
            base_commands = f"FROM {self._base_image}"

        env_vars = ""
        if self._env_vars:
            formatted_vars = [f"{key}={value!r}" for key, value in self._env_vars.items()]
            env_vars = "ENV " + " \\\n    ".join(formatted_vars)

        pip_installs = ""
        if self._python_dependencies:
            pip_installs = "RUN pip install " + " ".join(
                f"'{dep}'".replace("==", "~=") for dep in self._python_dependencies
            )

        installation_commands = ""
        if self._installation_commands:
            installation_commands = "\n".join(f"RUN {cmd}" for cmd in self._installation_commands)

        copy_files = ""
        if self._copy_files:
            for src, dest in self._copy_files.items():
                fname = os.path.basename(src)
                full_fname = os.path.join(dir, fname)

                if os.path.exists(full_fname) and not filecmp.cmp(src, full_fname):
                    raise ValueError(f"The file {fname} already exists in {dir}")
                elif os.path.isdir(src):
                    shutil.copytree(src=src, dst=full_fname, symlinks=False, ignore=None)
                else:
                    shutil.copy2(src=src, dst=full_fname)

                copy_files += f"COPY {fname} {dest}\n"

        copy_flows = ""
        for flow_name, flow in self._flows.items():
            qualified_flow_name = self.flow_qualified_name(flow)

            open(os.path.join(dir, f"{qualified_flow_name}.pickle"), "wb+").write(cloudpickle.dumps(flow))
            open(os.path.join(dir, f"{qualified_flow_name}.py"), "w+").write(
                textwrap.dedent(
                    f"""
                        import cloudpickle
                        import os

                        os.chdir(os.path.dirname(__file__))
                        {qualified_flow_name} = cloudpickle.loads(open("{qualified_flow_name}.pickle", "rb").read())
                    """
                )
            )

            copy_flows = (
                f"COPY {qualified_flow_name}.pickle {PREFECT_DIR}/flows/\n"
                f"COPY {qualified_flow_name}.py {PREFECT_DIR}/flows/\n"
            )

        install_cwd = ""
        if self._install_cwd:
            shutil.copytree(src=os.getcwd(), dst=f"{dir}/src", symlinks=False, ignore=None)
            install_cwd = f"COPY src/ {PREFECT_DIR}/src\nRUN ls {PREFECT_DIR}/src\nRUN pip install {PREFECT_DIR}/src\n"

        final_commands = ""
        if self._extra_dockerfile_commands:
            final_commands = "\n".join(self._extra_dockerfile_commands)

        healtcheck_loc = os.path.join(dir, "healthcheck.py")
        shutil.copy2(
            os.path.join(os.path.dirname(__file__), "prefect_healthcheck.py"),
            healtcheck_loc,
        )

        healthcheck_run = ""
        if not self._ignore_healthchecks:
            warnings.warn("Healthchecks not implemented. Flows are not validated")

        file_contents = textwrap.dedent(
            f"""
            {_multiline_indent(base_commands, 12)}
            {_multiline_indent(env_vars, 12)}

            RUN pip install --upgrade pip
            {_multiline_indent(installation_commands, 12)}
            {pip_installs}

            RUN mkdir -p {self._prefect_directory}

            COPY healthcheck.py {self._prefect_directory}/healthcheck.py
            {_multiline_indent(copy_files, 12)}
            {_multiline_indent(copy_flows, 12)}
            {_multiline_indent(install_cwd, 12)}

            {_multiline_indent(final_commands, 12)}
            {healthcheck_run}
            """
        )

        print(file_contents)

        dockerfile_path = os.path.join(dir, "Dockerfile")
        with open(dockerfile_path, "w+") as fd:
            fd.write(file_contents)
        return dockerfile_path

    def push_image(self):
        if not self._registry:
            raise ValueError("Container registry URL not set")

        client = self._get_client()

        LOG.info("Pushing image '%s:%s' to registry", self._image_name, self._image_tag)

        output = client.push(
            f"{self._registry}/{self._image_name}",
            tag=self._image_tag,
            stream=True,
            decode=True,
        )
        for line in output:
            if line.get("error"):
                raise InterruptedError(line.get("error"))
            if line.get("progress"):
                LOG.info("%s : %s", line.get("status"), line.get("progress"))

    def pull_image(self):
        client = self._get_client()

        LOG.info("Pulling image '%s' to registry", self._base_image)

        output = client.pull(self._base_image, stream=True, decode=True, platform=PREFECT_PLATFORM)
        for line in output:
            if line.get("error"):
                raise InterruptedError(line.get("error"))
            if line.get("progress"):
                LOG.info("%s : %s", line.get("status"), line.get("progress"))

    def build(self, push: bool = False) -> Tuple[str, str]:
        if len(self._flows) != 1:
            self._image_name = self._image_name or str(uuid.uuid4())
        else:
            self._image_name = self._image_name or slugify(list(self._flows.keys())[0])

        self._image_tag = self._image_tag or slugify(datetime.now().isoformat())

        return self._build_image(push)

    def _build_image(self, push: bool = False) -> Tuple[str, str]:
        assert isinstance(self._image_name, str)
        assert isinstance(self._image_tag, str)

        full_image_name = f"{self._image_name}:{self._image_tag}"

        if self._base_image and not self._dockerfile:
            self.pull_image()

        with TemporaryDirectory() as tdir:
            dockerfile_path = self._create_dockerfile_object(tdir)

            LOG.info(f"Building docker image '{full_image_name}'")

            if sys.platform == "win32":
                dockerfile_path = os.path.abspath(dockerfile_path)

            client = self._get_client()

            output = client.build(path=tdir, dockerfile=dockerfile_path, tag=self.get_name(), platform=PREFECT_PLATFORM)

            self._parse_generator_output(output)

            if len(client.images(name=self.get_name())) == 0:
                raise ValueError(
                    "Your docker image failed to build!  Your flow might have "
                    "failed one of its deployment health checks - please ensure "
                    "that all necessary files and dependencies have been included."
                )

            if push:
                if self._registry:
                    self.push_image()
                    client.remove_image(self.get_name())
                else:
                    LOG.warning("Container registry URL not set. Image will not be pushed")

        return self._image_name, self._image_tag

    @staticmethod
    def _parse_generator_output(generator: Iterable) -> None:
        """
        Parses and writes a Docker command's output to stdout
        """
        for item in generator:
            item = item.decode("utf-8")
            for line in item.split("\n"):
                if not line:
                    continue
                parsed = json.loads(line)
                if not isinstance(parsed, dict):
                    continue
                # Parse several possible schemas
                output = (
                    parsed.get("stream") or parsed.get("message") or parsed.get("errorDetail", {}).get("message") or ""
                ).strip("\n")
                if output:
                    print(output)
