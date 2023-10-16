import asyncio
from collections.abc import Callable
from functools import partial
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from querysource.types.validators import Entity
from qw.wrappers import TaskWrapper
from flowtask.conf import (
    DEBUG,
    default_pg, SCHEDULER_WORKER_TIMEOUT,
    SCHEDULER_WORKER_RETRY_ENQUEUE
)
from flowtask.tasks.task import Task
from flowtask.exceptions import (
    FileError, FileNotFound, NotSupported,
    TaskFailed, TaskNotFound
)
from .notifications import send_notification


def import_from_path(path):
    """Import a module / class from a path string.
    :param str path: class path, e.g., ndscheduler.corescheduler.job
    :return: class object
    :rtype: class
    """
    components = path.split('.')
    module = __import__('.'.join(components[:-1]))
    for comp in components[1:-1]:
        module = getattr(module, comp)
    return getattr(module, components[-1])


class TaskScheduler:
    def __init__(
        self,
        program,
        task,
        priority: str = 'low',
        worker: Callable = None,
        **kwargs
    ):
        self.task = task
        self.program = program
        self.priority = priority
        self.worker = worker
        self.wrapper = TaskWrapper(
            program=program,
            task=task,
            ignore_results=True,
            **kwargs
        )
        self.logger = logging.getLogger(
            'TaskScheduler'
        )

    async def set_task_status(self, state, error):
        # TODO: migrate to Prepared statements
        _new = False
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(event_loop)
            _new = True
        trace = Entity.escapeString(error)
        sentence = f"""UPDATE {self.program}.tasks
        SET task_state='{state}', traceback='{trace}'
        WHERE task = '{self.task}';"""
        result = None
        options = {
            "server_settings": {
                'application_name': 'Flowtask.Scheduler',
                'client_min_messages': 'notice',
                'max_parallel_workers': '256'
            }
        }
        conn = AsyncDB(
            'pg',
            dsn=default_pg,
            loop=event_loop,
            **options
        )
        try:
            async with await conn.connection() as conn:
                result, error = await conn.execute(sentence)
                if error:
                    self.logger.error(str(error))
            return result
        except Exception as err:
            self.logger.error(
                f"Task State Error: {err}"
            )

    async def _schedule_task(self, wrapper, queue):
        try:
            return await asyncio.wait_for(
                queue.queue(wrapper),
                timeout=SCHEDULER_WORKER_TIMEOUT
            )
        except (asyncio.QueueFull, asyncio.TimeoutError) as exc:
            self.logger.warning(
                f"Task {wrapper!r} was missed for enqueue due Queue Full {exc}"
            )
            try:
                self.logger.warning(
                    f"Task {wrapper!r} will be requeued at {SCHEDULER_WORKER_RETRY_ENQUEUE} sec."
                )
                await asyncio.sleep(
                    SCHEDULER_WORKER_RETRY_ENQUEUE
                )  # wait for N-seconds
                # re-enqueue task
                return await queue.queue(wrapper)
            except Exception as err:
                self.logger.error(f'{err}')
                # Set Task State as Discarded:
                await self.set_task_status(13, str(err))
                raise TaskFailed(
                    f"Task {wrapper!r} was discarded due timeout {err}"
                ) from err
        except OSError as exc:
            msg = f"Task {wrapper!r} {exc}"
            await self.set_task_status(13, str(msg))
            raise
        except Exception as exc:
            msg = f"Task {wrapper!r} can't be enqueued by Error {exc}"
            await self.set_task_status(13, str(msg))
            self.logger.warning(
                f"Task {wrapper!r} can't be enqueued by Error {exc}"
            )
            raise

    async def _publish_task(self, wrapper, queue):
        try:
            result = await queue.publish(wrapper)
            await asyncio.sleep(.01)
            return result
        except asyncio.TimeoutError:
            raise
        except Exception as exc:
            self.logger.error(f'{exc}')
            raise

    def __call__(self, *args, **kwargs):
        try:
            try:
                loop = asyncio.new_event_loop()
            except RuntimeError as exc:
                raise RuntimeError(
                    f"Unable to create a New Event Loop for Dispatching Tasks: {exc}"
                ) from exc
            asyncio.set_event_loop(loop)
            self.logger.info(
                f':::: Calling Task {self.program}.{self.task}: priority {self.priority!s}'
            )
            if self.priority == 'pub':
                # Using Channel Group mechanism (avoid queueing)
                task = loop.create_task(
                    self._publish_task(
                        self.wrapper, self.worker
                    )
                )
            else:
                task = loop.create_task(
                    self._schedule_task(
                        self.wrapper, self.worker
                    )
                )
            try:
                result = loop.run_until_complete(task)
                message = result.get('message', None)
                self.logger.info(
                    f'SCHED: {message!r}'
                )
            except asyncio.TimeoutError:  # pragma: no cover
                self.logger.error(
                    f"Scheduler: Cannot add task {self.program}.{self.task} to Queue Worker due Timeout."
                )
                send_notification(
                    loop,
                    message=f"Scheduler: Error sending task {self.program}.{self.task} to Worker",
                    provider='telegram'
                )
        except OSError as exc:
            self.logger.error(
                f'IO: Connection Refused: {exc}'
            )
            send_notification(
                loop,
                message=f"Scheduler: Task {self.program}.{self.task} Connection Refused: {exc!s}",
                provider='telegram'
            )
            raise
        except Exception as exc:
            self.logger.exception(
                f'Exception: {exc}'
            )
            send_notification(
                loop,
                message=f"Scheduler: Exception on Enqueue {self.program}.{self.task}: {exc!s}",
                provider='telegram'
            )
            raise
        finally:
            try:
                loop.close()
            except Exception:
                pass


async def launch_task(program, task_id, loop, ENV):
    task = Task(
        task=task_id,
        program=program,
        loop=loop,
        ignore_results=True,
        ENV=ENV,
        debug=DEBUG
    )
    try:
        start = await task.start()
        if not start:
            logging.error(
                f'Failing Task Start: {program}.{task_id}'
            )
    except Exception as err:
        logging.error(err)
        raise TaskFailed(f"{err!s}") from err
    try:
        result = await task.run()
        return result
    except (NotSupported, FileNotFound, NoDataFound):
        raise
    except TaskNotFound as err:
        raise TaskNotFound(
            f'Task: {task_id}: {err!s}'
        ) from err
    except TaskFailed as err:
        raise TaskFailed(
            f'Task {task_id} failed: {err}'
        ) from err
    except FileError as err:
        raise FileError(
            f'Task {task_id}, File Not Found: {err}'
        ) from err
    except Exception as err:
        raise TaskFailed(
            f'Error: Task {task_id} failed: {err}'
        ) from err
    finally:
        try:
            await task.close()
        except Exception as err:
            logging.error(err)

def get_function(
    job: dict,
    priority: str = 'low',
    worker: Callable = None
):
    fn = job['job']
    t = fn['type']
    params = {}
    if job['params']:
        params = {**job['params']}
    try:
        func = fn[t]
    except KeyError as e:
        raise RuntimeError(
            f'Error getting Function on Schedule {t}'
        ) from e
    if t == 'function':
        try:
            fn = globals()[func]
            return fn
        except Exception as err:
            raise RuntimeError(
                f'Error: {err!s}'
            ) from err
    elif t == 'package':
        try:
            fn = import_from_path(func)
            return fn
        except Exception as err:
            raise RuntimeError(
                f'Error: {err!s}'
            ) from err
    elif t == 'task':
        task, program = fn['task'].values()
        if priority == 'local':
            # run in a function wrapper
            func = partial(
                launch_task,
                program,
                task
            )
            return func
        else:
            sched = TaskScheduler(
                program,
                task,
                priority,
                worker,
                **params
            )
            sched.__class__.__name__ = f'Task({program}.{task})'
            return sched
    else:
        return None
