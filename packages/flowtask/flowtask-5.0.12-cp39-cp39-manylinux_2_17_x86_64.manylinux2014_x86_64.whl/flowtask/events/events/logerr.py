import socket
from datetime import datetime
from redis import asyncio as aioredis
from navconfig.logging import logging
from flowtask.utils.json import json_encoder
from flowtask.conf import (
    ENVIRONMENT,
    PUBSUB_REDIS,
    ERROR_CHANNEL
)
from .abstract import AbstractEvent


EVENT_HOST = socket.gethostbyname(socket.gethostname())


class LogError(AbstractEvent):
    def __init__(self, *args, **kwargs):
        super(LogError, self).__init__(*args, **kwargs)
        self._logger = logging.getLogger('FlowTask.LogError')

    async def __call__(self, *args, **kwargs):
        status = kwargs.pop('status', 'event')
        task = kwargs.pop('task', None)
        program = task.getProgram()
        task_name = task.taskname
        task_id = task.task_id
        msg = kwargs.pop('message', None)
        cls = kwargs.pop('cls', None)
        if not msg:
            msg = getattr(cls, 'message', str(cls))
        redis = await aioredis.from_url(
            PUBSUB_REDIS,
            encoding="utf-8",
            decode_responses=True
        )
        msg = {
            "task": f"{program}.{task_name}",
            "task_id": task_id,
            "type": "error",
            "status": status,
            "environment": ENVIRONMENT,
            "host": EVENT_HOST,
            "end_time": datetime.utcnow()
        }
        message = json_encoder(msg)
        try:
            await redis.publish(ERROR_CHANNEL, message)
        except Exception as e:
            logging.warning(f"Publis Error: {e}")
        finally:
            await redis.close()
            try:
                await redis.connection_pool.disconnect()
            except Exception:
                pass
