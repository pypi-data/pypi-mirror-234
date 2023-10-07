"""
TaskPîle.
"""
from numbers import Number
from typing import (
    Any
)
from collections.abc import Callable
from functools import partial
from navconfig.logging import logging
from flowtask.components import (
    getComponent,
    GroupComponent
)
from flowtask.exceptions import (
    TaskDefinition,
    ComponentError
)

logging.getLogger('matplotlib').setLevel(logging.CRITICAL)
logging.getLogger('PIL').setLevel(logging.CRITICAL)

import matplotlib.pyplot as plt  # pylint: disable=C0411,C0413
import networkx as nx  # pylint: disable=C0411,C0413

class Step(object):
    """Step.

    Step is the basic component of a Task.
    """
    def __init__(self, step_name: str, step_id: int, params: dict, program: str = None) -> None:
        try:
            self._component = getComponent(step_name, program=program)
        except Exception as e:
            logging.exception(e, stack_info=False)
            raise ComponentError(
                f'Step Error: Unable to load Component {step_name}: {e}'
            ) from e
        self.step_id = f"{step_name}_{step_id}"
        self.step_name = step_name
        self.params = params
        self.job: Callable = None
        self.depends: list = []
        try:
            self.depends = params['depends']
        except KeyError:
            pass

    def get_depends(self, previous) -> Any:
        if not self.depends:
            return previous
        else:
            return self.depends

    def __str__(self) -> str:
        return f"<{self.step_id}>: {self.params!r}"

    def __repr__(self) -> str:
        return f"<{self.step_id}>: {self.params!r}"

    @property
    def name(self):
        return self.step_id

    @property
    def component(self):
        return self._component


class GroupStep(Step):
    def __init__(self, step_name: str, step_id: int, params: dict, program: str = None) -> None:
        try:
            self._component = GroupComponent
        except Exception as e:
            logging.exception(e, stack_info=False)
            raise ComponentError(
                f'Step Error: Unable to load Group Component {step_name}: {e}'
            ) from e
        self.step_id = f"{step_name}_{step_id}"
        self.step_name = step_name
        self.params = params
        self.job: Callable = None
        self.depends: list = []
        self._steps: list = []
        try:
            self.depends = params['depends']
        except KeyError:
            pass

    def add_step(self, step) -> None:
        self._steps.append(step)

    @property
    def component(self):
        return partial(self._component, component_list=self._steps)


class TaskPile(object):
    """
    TaskPile.

        Compile Task and components and got every step on Task
        and creating a dependency graph of Task Definition.
    """
    def __init__(self, task: dict, program: str = None):
        self._size: int = 0
        self._n = 0
        self.task: dict = task
        self._task: list = []  # List of Steps components
        self.__name__ = self.task['name']
        self._program: str = program
        self._groups: dict = {}
        try:
            self._steps: list = task['steps']
        except KeyError as e:
            raise TaskDefinition(
                "Task Error: This task has no Steps."
            ) from e
        self._step = None
        self._graph = nx.DiGraph(task=self.__name__)  # creates an empty Graph
        self.build()

    def build(self):
        counter = 1
        for step in self._steps:
            for step_name, params in step.items():
                try:
                    if 'Group' in params:
                        group = params['Group']
                        group_name = f'{group}'
                        if group_name in self._groups:  # already exists:
                            cp = self._groups[group_name]
                        else:
                            cp = GroupStep(group_name, counter, params={}, program=self._program)
                            self._groups[group_name] = cp
                            s = {
                                "task_id": f"{group_name}_{counter}",
                                "step": cp
                            }
                            self._graph.add_node(cp.name, attrs=params)
                            self._task.append(s)
                        # create the step:
                        sp = Step(step_name, counter, params=params, program=self._program)
                        # add the step to the group:
                        cp.add_step(sp)
                        continue
                    else:
                        cp = Step(step_name, counter, params, program=self._program)
                        s = {
                            "task_id": f"{step_name}_{counter}",
                            "step": cp
                        }
                except Exception as e:
                    raise ComponentError(
                        f"Task Error: Error loading Component: {e}"
                    ) from e
                counter += 1
                prev = None
                try:
                    prev = self._task[-1]
                except IndexError:
                    pass
                self._graph.add_node(cp.name, attrs=params)
                self._task.append(s)
                # calculate dependencies:
                depends = cp.get_depends(prev)
                if isinstance(depends, dict):
                    self._graph.add_edge(depends['task_id'], cp.name)
                elif isinstance(depends, list):
                    # making calculation of edges.
                    pass
        # size of the Pile of Components
        self._size = len(self._task)
        # check if Task is a DAG:
        if nx.is_directed_acyclic_graph(self._graph) is False:
            raise TaskDefinition(
                "Task Error: This task is not an Acyclic Graph."
            )

    def plot_task(self):
        plt.tight_layout()
        nx.draw_networkx(self._graph, arrows=True)
        plt.savefig(f"task_{self.__name__}.png", format="PNG")
        plt.clf()

    def __len__(self):
        return len(self._steps)

    def __del__(self):
        del self._steps

    # Iterators:
    def __iter__(self):
        self._n = 0
        self._step = self._task[0]['step']
        return self

    def __next__(self):
        if self._n < self._size:
            try:
                result = self._task[self._n]['step']
            except IndexError as e:
                raise StopIteration from e
            self._step = result
            self._n += 1
            return self
        else:
            self._step = None
            raise StopIteration

    # Get properties of the Step
    @property
    def name(self):
        return self._step.name

    @property
    def component(self):
        return self._step.component

    @property
    def step(self):
        return self._step.step_name

    def params(self):
        return self._step.params

## Component Properties
    def getStepByID(self, task_id):
        return self._task[task_id]

    def delStep(self, task_id):
        del self._task[task_id]

    def getStep(self, name):
        obj = next(
            (item for item in self._task if item["task_id"] == name), None)
        if obj:
            self._step = obj
            return self

    def nextStep(self, name):
        idx = next(
            (i for i, item in enumerate(self._task) if item["task_id"] == name), None
        )
        if idx != -1:
            i = idx + 1
            self._step = self._task[i]['step']
            return [self, i]

    def setStep(self, step):
        self._step.job = step

    def getDepends(self, previous=None):
        depends = self._step.depends
        if not depends:
            return previous
        else:
            if isinstance(depends, Number):
                try:
                    obj = self._task[depends]
                    return obj['job']
                except (KeyError, IndexError):
                    task = self._step['task']
                    logging.error(
                        f"Task Error: invalid Step index {depends} on task name {task}"
                    )
                    return None
            elif isinstance(depends, list):
                # list of depends
                obj = []
                for d in depends:
                    o = next(
                        (item for item in self._task if item["task_id"] == d), None)
                    if o:
                        component = o['step']
                        obj.append(component.job)
                return obj
            else:
                # is a string, this is the task id
                obj = next(
                    (item for item in self._task if item["task_id"] == depends), None)
                if obj:
                    component = obj['step']
                    return component.job
