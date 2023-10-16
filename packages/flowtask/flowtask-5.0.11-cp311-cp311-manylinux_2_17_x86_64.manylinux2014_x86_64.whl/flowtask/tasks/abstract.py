import os
import time
import asyncio
import uuid
import random
import locale
import traceback
from collections.abc import Callable, Awaitable
from abc import ABC, abstractmethod
import jsonschema
# asyncdb
from asyncdb import AsyncDB
from asyncdb.drivers.abstract import BaseDriver
from asyncdb.exceptions import ProviderError
from asyncdb.meta import Record
# and navconfig
from navconfig import config, DEBUG
from navconfig.logging import logging
# DI
from flowtask.conf import (
    default_dsn,
    SYSTEM_LOCALE,
    TASK_STORAGES,
    FILE_STORAGES
)
from flowtask.utils.stats import TaskMonitor
from flowtask.models import (
    TaskState
)
from flowtask.exceptions import (
    TaskError,
    TaskParseError
)
from ..events import (
    EventManager,
    LogEvent,
    LogError
)


class AbstractTask(ABC):
    """
    AbstractTask.

        Base class for all Dataintegration tasks.
    """
    _logger: logging.Logger = None

    # pre-init and post-end functions
    pre_init: Awaitable[asyncio.Task] = None
    post_end: Awaitable[asyncio.Task] = None
    _event_list: list = [
        "started",
        "running",
        "exception",
        "data_not_found",
        "data_error",
        "file_not_found",
        "file_empty"
    ]

    def __init__(
        self,
        task_id: str = None,
        task: str = None,
        program: str = None,
        loop: asyncio.AbstractEventLoop = None,
        parser: Callable = None,
        **kwargs
    ):
        self._state = TaskState.PENDING
        self.stat = None
        self.enable_stat: bool = True
        self._task = None
        self._taskname = task
        self._taskdef = None
        self._env = config
        self._attrs = {}
        self._variables: dict = {}
        # program definition
        self._program = program
        if not self._program:
            self._program = 'navigator'
        self._schema = program
        self._kwargs = {}
        self._args = {}
        self._conditions = {}
        self._argparser = None
        self._options = None
        self._parameters: list = []
        self._arguments: list = []
        # configure logging
        self.logger = logging.getLogger(
            'FlowTask.Task'
        )
        # re-use task Stat object from parent (subtasks)
        try:
            self.stat = kwargs['stat']
            del kwargs['stat']
        except KeyError:
            pass
        if parser:
            self._argparser = parser
            self._options = parser.options
        self._taskdef: Record = None
        # define if results are returned or not (when run on scheduler)
        try:
            self._ignore_results: bool = bool(kwargs['ignore_results'])
            del kwargs['ignore_results']
        except KeyError:
            self._ignore_results: bool = False
            if parser:
                if 'ignore-results' in parser.attributes:
                    self._ignore_results: bool = bool(
                        parser.attributes['ignore-results']
                    )
        # disable notifications
        try:
            self._no_notify = kwargs.get('disable_notifications', False)
            del kwargs['disable_notifications']
        except KeyError:
            self._no_notify = False
        if self._no_notify is True:
            self.enable_stat = False
        self._new_loop: bool = False
        if loop:
            self._loop = loop
        else:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                self._new_loop: bool = True
        # Task ID:
        self.task_id = task_id if task_id else uuid.uuid1(
            node=random.getrandbits(48) | 0x010000000000
        )
        # DEBUG
        try:
            self._debug = kwargs['debug']
            del kwargs['debug']
        except KeyError:
            self._debug = DEBUG
        info = {
            "task_id": task_id,
            "task": self._taskname,
            "program": self._program,
            "debug": self._debug,
            "started": time.time()
        }
        self.logger.info(
            f'::: TASK: {info!r} :::'
        )
        if self._debug:
            self.logger.setLevel(
                logging.DEBUG
            )
        else:
            self.logger.setLevel(
                logging.INFO
            )
        # defining Locale
        try:
            locale.setlocale(
                locale.LC_ALL,
                SYSTEM_LOCALE
            )
        except locale.Error as e:
            self.logger.error(e)
        # initialize the event system
        self._events = EventManager(name='task')
        self.task_events()
        # On Finish Events:
        log = LogEvent(use_notice=True)
        errlog = LogError()
        self._events.addEvent(
            done=[log]
        )
        self._events.addEvent(
            completed=[log]
        )
        self._events.addEvent(
            on_error=[log, errlog]
        )
        # TaskStorage
        ### default Filesystem Storage:
        self._storage = kwargs.pop('storage', 'default')
        try:
            self.taskstore = TASK_STORAGES[self._storage]
        except KeyError as exc:
            raise RuntimeError(
                f"Invalid Task Storage {self._storage}"
            ) from exc
        # File Storage:
        # Site where Files are stored during Task execution
        fstore = kwargs.pop('filestore', 'default')
        try:
            self._filestore = FILE_STORAGES[fstore]
            self._filestore.set_program(self._program)
        except KeyError as exc:
            raise RuntimeError(
                f"Invalid File Store {fstore}"
            ) from exc
        # params
        self._params = {}
        if 'params' in kwargs:
            self._params = {**kwargs['params']}
            del kwargs['params']
        # also, work with arguments
        # command-line arguments
        self._arguments = []
        if parser:
            self._arguments = self._options.arguments
        try:
            args = kwargs['arguments']
            del kwargs['arguments']
            if isinstance(args, list):
                self._arguments = self._arguments + args
        except KeyError:
            pass
        if parser:
            try:
                self._args = self._options.args
            except (KeyError, ValueError, TypeError):
                pass
        elif 'args' in kwargs:
            self._args = kwargs['args']
        # processed parameters
        try:
            self._parameters = self._options.parameters
        except AttributeError:
            pass
        if kwargs:
            # remain args go to kwargs:
            self._kwargs = {**kwargs}

    def get_variables(self):
        return self._variables

    # Context Methods:
    async def __aenter__(self) -> "AbstractTask":
        """ Magic Context Methods """
        if callable(self.pre_init):
            # this is a function called before start.
            await self.pre_init()  # pylint: disable=E1102
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        try:
            await self.close()
        finally:
            # this is a function called when Task Ends.
            if callable(self.post_end):
                await self.post_end()  # pylint: disable=E1102

    def task_events(self):
        """Initialize Event manager with a default list of events.
        """
        log = LogEvent()
        event_list = {}
        for event in self._event_list:
            event_list[event] = [log]  # Create a new list for each event
        self._events.addEvent(**event_list)

    def event_defaults(self, function: Callable):
        for event in self._event_list:
            evt = getattr(self._events, event)
            evt.add(function)

    def set_timezone(self, timezone: str = 'UTC') -> None:
        os.environ['TZ'] = timezone
        time.tzset()

    async def start(self) -> bool:
        self._state = TaskState.STARTED
        self._events.started(
            message=f":: Starting Task: {self._program}.{self._taskname}",
            task=self,
            status='start',
            disable_notification=self._no_notify
        )
        if not self.stat:
            if self.enable_stat is True:
                # create the stat component:
                try:
                    self.stat = TaskMonitor(
                        name=self._taskname,
                        program=self._program,
                        task_id=self.task_id
                    )
                    await self.stat.start()
                except Exception as err:
                    raise TaskError(
                        f"Task: Error on TaskMonitor: {err}"
                    ) from err
        try:
            # getting Task information
            await self.get_task()
        except Exception as err:
            self.logger.exception(err)
            self._state = TaskState.EXCEPTION
            self._events.exception(
                message=f'Task Error: {self._taskname}: {err!r}',
                task=self,
                status='exception'
            )
            return False
        # check for different types of Tasks
        if self._taskdef:
            self._events.started(
                message=f'Database-based Task {self._taskname!s}',
                task=self,
                status='start',
                disable_notification=self._no_notify
            )
        else:
            self._events.started(
                message=f':: File-based Task {self._taskname!s}',
                task=self,
                status='start',
                disable_notification=self._no_notify
            )
        return True

    @abstractmethod
    async def run(self) -> bool:
        pass

    @property
    def taskname(self):
        return self._taskname

    @property
    def id(self):
        return self.task_id

    def getState(self):
        return self._state

    def getProgram(self):
        return self._program

    def schema(self):
        return self._schema

    @property
    def stats(self) -> TaskMonitor:
        """stats.
        Return a TaskMonitor object with all collected stats.
        Returns:
            TaskMonitor: stat object.
        """
        return self.stat

    def setStat(self, stat):
        self.stat = stat

    async def get_taskrow(self, table: str, conn: BaseDriver) -> Record:
        definition = None
        # TODO: add column "storage" and "datastore"
        t = """
         SELECT task_id, url, url_response, task_function, task_path,
         task_definition, attributes, params, is_coroutine, executor,
         program_slug, storage FROM {table} WHERE enabled = true AND task='{task}';
        """
        task = t.format(table=table, task=self._taskname)
        self.logger.debug(
            f':: Task Query: {task}'
        )
        try:
            result, error = await conn.queryrow(task)
            if error:
                return None
            if result:
                definition = Record.from_dict(dict(result))
                return definition
        except ProviderError as exc:
            if 'does not exist' in str(exc):
                # Table doesn't exist
                self.logger.warning(
                    f"Table {table} does not exist"
                )
            else:
                self.logger.error(str(exc))
        except Exception as err:  # pylint: disable=W0718
            self.logger.exception(
                str(err), stack_info=False
            )

    def retry(self):
        try:
            return self._taskdef['attributes']['retry']
        except (KeyError, AttributeError, TypeError):
            return False

    async def get_task(self):
        try:
            db = AsyncDB('pg', dsn=default_dsn, loop=self._loop)
            async with await db.connection() as conn:
                # first, check if a Tasks table exists on tenant:
                sql = f"""SELECT EXISTS (
                       SELECT FROM pg_catalog.pg_class c
                       JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
                       WHERE  n.nspname = '{self._program}'
                       AND    c.relname = 'tasks'
                       AND    c.relkind = 'r');"""
                try:
                    row, error = await conn.queryrow(sql)
                    if error:
                        self.logger.error(
                            f'{error}'
                        )
                    if row and row['exists']:
                        # its a database-defined task
                        table = f"{self._program}.tasks"
                        self._schema = self._program
                        taskdef = await self.get_taskrow(table, conn)
                        if not taskdef:
                            # fallback to navigator.tasks:
                            table = "navigator.tasks"
                            self._schema = 'navigator'
                        else:
                            self._taskdef = taskdef
                            if self._storage == 'row':
                                ### getting Task directly from taskdef
                                self.taskstore.set_definition(taskdef)
                            return True
                    else:
                        # fallback to navigator.tasks:
                        table = "navigator.tasks"
                        self._schema = 'navigator'
                    # getting task definition
                    taskdef = await self.get_taskrow(table, conn)
                    if taskdef is not None:
                        self._taskdef = taskdef
                        if self._storage == 'row':
                            ### getting Task directly from taskdef
                            self.taskstore.set_definition(taskdef)
                        elif self._taskdef.storage != 'default':
                            # Changing the default storage for Task.
                            self._storage = self._taskdef.storage
                            self.taskstore = TASK_STORAGES[self._storage]
                        return True
                    else:
                        self._schema = None
                        self.logger.warning(
                            f'Task \'{self._taskname}\' not found in database.'
                        )
                        return False
                except Exception as err:
                    print(err)
                    return False
        except Exception as err:
            dump = traceback.format_exc()
            self._state = TaskState.EXCEPTION
            self._events.exception(
                message=f'Error on Task definition: {err!s}',
                cls=err,
                trace=dump,
                task=self,
                status='exception'
            )
            return False

    def check_syntax(self, task):
        """
        check_syntax.

        Check syntax of JSON task (if is json-based)
        """
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "timezone": {"type": "string"},
                "comments": {"type": "string"},
                "events": {
                    "type": "object",
                    "properties": {
                        "publish": {"type": "boolean"}
                    },
                    "additionalProperties": {
                        "anyOf": [
                            {
                                "type": "object",
                                "additionalProperties": True
                            },
                            {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": True
                                }
                            }
                        ]
                    }
                },
                "steps": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {"type": "object"}
                        ]
                    }
                }
            },
            "required": [
                "name", "steps"
            ]
        }
        try:
            jsonschema.validate(instance=task, schema=schema)
            return True
        except jsonschema.ValidationError as err:
            self._state = TaskState.ERROR
            self._events.exception(
                message=f'Error on Task Parse: {err!s}',
                cls=err,
                task=self,
                status='TaskError'
            )
            raise TaskParseError(
                f'Task: Error parsing {self._taskname}: {err!s}'
            ) from err
        except Exception as err:
            self._state = TaskState.EXCEPTION
            self._events.exception(
                message=f'Exception on Task: {err!s}',
                cls=err,
                task=self,
                status='TaskError'
            )
            raise TaskParseError(
                f'Task: Unknown parsing Error on {self._taskname}: {err!s}'
            ) from err

    async def close(self):
        self.set_timezone('UTC')  # forcing UTC at Task End.
        # TODO: closing Memcached-related connections
        if self._new_loop is True:
            self._loop.close()
        # closing also the Event Manager
        # self._events.close()
