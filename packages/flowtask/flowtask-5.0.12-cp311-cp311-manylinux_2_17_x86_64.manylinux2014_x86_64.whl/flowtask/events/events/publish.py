import socket
from datetime import datetime
from redis import asyncio as aioredis
from navconfig.logging import logging
from flowtask.utils.json import json_encoder
from flowtask.conf import (
    ENVIRONMENT,
    PUBSUB_REDIS
)
from .abstract import AbstractEvent

EVENT_HOST = socket.gethostbyname(socket.gethostname())

class PublishEvent(AbstractEvent):
    async def __call__(self, *args, **kwargs):
        status = kwargs.pop('status', 'event')
        task = kwargs.pop('task', None)
        program = task.getProgram()
        task_name = task.taskname.replace('.', ':')  # Convert dots to colons for Redis channel name
        channel_name = f"{program}:{task_name}"
        task_id = task.task_id
        redis = await aioredis.from_url(
            PUBSUB_REDIS,
            encoding="utf-8",
            decode_responses=True
        )
        try:
            stat = task.stats  # getting the stat object:
            stats = json_encoder(stat.to_json())
        except AttributeError:
            stats = None
        msg = {
            "task": f"{program}.{task_name}",
            "task_id": task_id,
            "status": status,
            "environment": ENVIRONMENT,
            "host": EVENT_HOST,
            "stats": stats,
            "end_time": datetime.utcnow()
        }
        message = json_encoder(msg)
        try:
            rst = await redis.publish(channel_name, message)
            print(rst)
        except Exception as e:
            logging.warning(f"Publis Error: {e}")
        finally:
            await redis.close()
            try:
                await redis.connection_pool.disconnect()
            except Exception:
                pass
