import asyncio
import logging
from collections.abc import Callable
import traceback
import pprint
from asyncdb.exceptions import (
    NoDataFound
)
from flowtask.tasks.task import Task
from flowtask.utils.functions import check_empty
from flowtask.exceptions import (
    DataNotFound,
    NotSupported,
    ComponentError,
    TaskNotFound,
    TaskDefinition,
    TaskFailed
)
from .abstract import DtComponent

class SubTask(DtComponent):
    """
    SubTask.

    Overview

         This component executes the task by identifying the name of the task and the program

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  task        |   Yes    | The parameter is passed the name of the task                      |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  program     |   Yes    | The parameter is passed the name of the program                   |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days

    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._params = {}
        self.task: str = ''
        self._task = None
        self.program: str = ''
        self.conditions = {}
        self._arguments = {}
        self.ignore_steps: list = []
        self.run_only: list = []
        super(SubTask, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        self.program = self._program

    async def start(self, **kwargs):
        program = self.program
        self._program = program
        try:
            del self._params['program']
        except KeyError:
            pass
        try:
            # task = self.task
            del self._params['task']
        except KeyError:
            pass
        # passing variables to SubTask
        params = {
            "vars": self._vars,
            "variables": self._variables,
            # "parameters": self._parameters,
            "ignore_steps": self.ignore_steps,
            "run_only": self.run_only,
            "memory": self._memory,
            "attributes": self._attributes,
            "arguments": self._arguments,
            "is_subtask": True,
            "conditions": self.conditions,
            "params": self._params
        }
        if self._debug is True:
            pp = pprint.PrettyPrinter(indent=4)
            print(' Subtask Properties ==================')
            pp.pprint(params)
            print(' ==================')
        if 'debug' in self._params:
            del self._params['debug']
        # definition of task
        try:
            self._task = Task(
                task=self.task,
                program=self.program,
                loop=self._loop,
                debug=self._debug,
                stat=self.stat.parent(),
                **params
            )
            self.add_metric('TASK', f"{self.program}.{self.task}")
            try:
                if self._task:
                    prepare = await self._task.start()
                    if prepare:
                        return True
                    else:
                        return False
            except (TaskDefinition, TaskFailed) as err:
                logging.exception(err, stack_info=True)
        except TaskNotFound as err:
            logging.exception(err, stack_info=True)
        except Exception as err:
            traceback.print_exc()
            print(err, err.__class__)
            logging.exception(err, stack_info=True)

    async def close(self):
        if self._task:
            try:
                await self._task.close()
            except Exception as err:
                raise TaskFailed(
                    f"Error closing Task {self.task!s}, error: {err}"
                ) from err

    async def run(self):
        result = False
        if not self._task:
            return False
        try:
            result = await self._task.run()
        except (DataNotFound, NoDataFound) as err:
            raise DataNotFound(
                f"{err!s}"
            ) from err
        except NotSupported as err:
            raise NotSupported(
                f"Error running Task {self.task}, error: {err}"
            ) from err
        except (Exception, ComponentError) as err:
            raise ComponentError(
                f"Unknown Component Error on Task {self.task}, error: {err}"
            ) from err
        if check_empty(result):
            return False
        else:
            self._result = self
            return result
