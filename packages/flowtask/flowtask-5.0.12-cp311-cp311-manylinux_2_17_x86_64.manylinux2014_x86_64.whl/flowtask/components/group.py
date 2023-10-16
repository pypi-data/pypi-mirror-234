import asyncio
from collections.abc import Callable
from navconfig.logging import logging
from asyncdb.exceptions import NoDataFound, ProviderError
from flowtask.utils.stats import StepMonitor
from flowtask.components import SkipErrors
from flowtask.exceptions import (
    DataNotFound,
    NotSupported,
    ComponentError
)
from flowtask.utils import cPrint
from .abstract import DtComponent


class GroupComponent(DtComponent):
    """
    GroupComponent.

        Executing a Group of task as one Component.
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            component_list: list = None,
            **kwargs
    ):
        """Init Method."""
        self._params = {}
        self._components = component_list
        super(GroupComponent, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        return True

    async def close(self):
        pass

    async def run(self):
        steps = []
        prev = None
        result = None
        for step in self._components:
            step_name = step.name
            try:
                _prev = prev
                component = self.get_component(step=step, previous=prev)
                prev = component
            except Exception as e:
                raise ComponentError(
                    f"{e!s}"
                ) from e
            # calling start method for component
            start = getattr(component, 'start', None)
            if callable(start):
                try:
                    if asyncio.iscoroutinefunction(start):
                        st = await component.start()
                    else:
                        st = component.start()
                    logging.debug(f'{step_name} STARTED: {st}')
                except (NoDataFound, DataNotFound) as err:
                    if component.skipError == SkipErrors.SKIP:
                        print(
                            f'::: SKIPPING Error on {step_name} :::: '
                        )
                        prev = _prev
                        continue
                    raise DataNotFound(
                        f"{err}"
                    ) from err
                except (ProviderError, ComponentError, NotSupported) as err:
                    raise ComponentError(
                        f"Group Error: calling Start on {step.name}, error: {err}"
                    ) from err
            else:
                raise ComponentError(
                    f"Group Error: missing Start on {step.name}"
                )
            # then, calling the run method:
            try:
                run = getattr(component, 'run', None)
                if asyncio.iscoroutinefunction(run):
                    result = await run()
                else:
                    result = run()
            except (NoDataFound, DataNotFound) as err:
                if component.skipError == SkipErrors.SKIP:
                    print(
                        f'::: SKIPPING Error on {step_name} :::: '
                    )
                    continue
                raise DataNotFound(
                    f"{err}"
                ) from err
            except (ProviderError, ComponentError, NotSupported) as err:
                if component.skipError == SkipErrors.SKIP:
                    print(
                        f'::: SKIPPING Error on {step_name} :::: '
                    )
                    continue
                raise NotSupported(
                    f"Group Error: Not Supported on {step.name}, error: {err}"
                ) from err
            except Exception as err:
                if component.skipError == SkipErrors.SKIP:
                    print(
                        f'::: SKIPPING Error on {step_name} :::: '
                    )
                    continue
                raise ComponentError(
                    f"Group Error: Calling Start on {step.name}, error: {err}"
                ) from err
            finally:
                steps.append(step_name)
                try:
                    close = getattr(component, 'close', None)
                    if asyncio.iscoroutinefunction(close):
                        await close()
                    else:
                        close()
                except Exception as e:  # pylint: disable=W0703
                    logging.warning(e)
        self._result = result
        return self._result

    def get_component(self, step, previous):
        if self.stat:
            parent_stat = self.stat.parent()
            stat = StepMonitor(name=step.name, parent=parent_stat)
            parent_stat.add_step(stat)
        else:
            stat = None
        params = step.params
        params['ENV'] = self._environment
        # params
        if self._params:
            try:
                params['params'] = {**params['params'], **self._params}
            except (KeyError, TypeError):
                pass
        # parameters
        if self._parameters:
            parameters = params.get('parameters', {})
            params['parameters'] = {**parameters, **self._parameters}
        # useful to change variables in set var components
        params['_vars'] = self._vars
        # variables dictionary
        params['variables'] = self._variables
        params['_args'] = self._args
        # argument list for components (or tasks) that need argument lists
        params['arguments'] = self._arguments
        # for components with conditions, we can add more conditions
        conditions = params.get('conditions', {})
        params['conditions'] = {**conditions, **self.conditions}
        # attributes only usable component-only
        params['attributes'] = self._attributes
        # the current Pile of components
        params['TaskPile'] = self._TaskPile
        # params['TaskName'] = step_name
        params['debug'] = self._debug
        params['argparser'] = self._argparser
        # the current in-memory connector
        params['memory'] = self._memory
        target = step.component
        job = None
        try:
            job = target(
                job=previous,
                loop=self._loop,
                stat=stat,
                **params
            )
            cPrint(f'LOADED STEP: {step.name}', level='DEBUG')
            return job
        except Exception as err:
            raise ComponentError(
                f"Component Error on {target}, error: {err}"
            ) from err
