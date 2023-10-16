import asyncio

from celery.result import AsyncResult
from redis.asyncio import from_url

from .general_utils import get_required_env


redis = from_url(get_required_env('BROKER_URI'), decode_responses=True)


async def wait_and_receive_messages(task_result: AsyncResult):
    # Todo: Check if will lose message if waiting for too long
    sub = redis.pubsub(ignore_subscribe_messages=True)
    await sub.subscribe(f'task-messages-{task_result.task_id}')
    while not task_result.ready():
        await asyncio.sleep(0.5)
        while (message_raw := await sub.get_message()) is not None:
            yield message_raw['data']
