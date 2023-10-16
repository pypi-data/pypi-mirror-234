import logging
import time
from contextlib import asynccontextmanager

import anyio
from prefect import Task, get_client
from prefect.client import OrionClient
from prefect.context import get_run_context
from prefect.orion.schemas.filters import TaskRunFilter
from prefect.orion.schemas.states import TERMINAL_STATES

LOG = logging.getLogger(__name__)


async def wait_for_concurrency_limit(client: OrionClient, tag: str, check_interval: float = 1.0, timeout: float = 0.0):
    start_time = time.time()

    while True:
        if 0 < timeout < (time.time() - start_time):
            LOG.warning("Concurrency wait timeout")
            break

        tasks = await client.read_task_runs(task_run_filter=TaskRunFilter(tags={"all_": [tag]}))
        active_tasks = [x for x in tasks if x.state.type not in TERMINAL_STATES]

        if len(active_tasks) > 0:
            await anyio.sleep(check_interval)
        else:
            break


@asynccontextmanager
async def concurrency_limit(task: Task, limit: int = 10) -> Task:
    context = get_run_context()

    tag = f"{context.flow_run.id}-{task.name}"

    client = get_client()

    await client.create_concurrency_limit(tag, limit)
    decorated_task: Task = task.with_options(tags=[tag])

    try:
        yield decorated_task
        await anyio.sleep(1.0)
        await wait_for_concurrency_limit(client, tag)
    finally:
        await client.delete_concurrency_limit_by_tag(tag)
