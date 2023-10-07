from abc import ABC
from typing import Optional, Any
from collections.abc import Iterable
from asyncdb import AsyncDB
from asyncdb.drivers.abstract import BaseDriver
from flowtask.conf import (
    MEMCACHE_HOST,
    MEMCACHE_PORT
)

class ResultSupport(ABC):
    """Support for manipulating the results of Components.
    """
    _memory: Optional[BaseDriver] = None
    use_memory: bool = False

    def __init__(self, **kwargs):
        try:
            self.use_memory: bool = bool(kwargs['use_memory'])
            del kwargs['use_memory']
        except KeyError:
            self.use_memory: bool = False
        # collection of results:
        self._result: Optional[Any] = None
        self.data: Optional[Any] = None
        # previous Component
        self._component: Optional[Iterable] = None
        # can pass a previous data as Argument:
        try:
            self._input_result = kwargs['input_result']
            del kwargs['input_result']
        except KeyError:
            self._input_result = None
        # memcache connector
        if self.use_memory is True:
            params = {
                "host": MEMCACHE_HOST,
                "port": MEMCACHE_PORT
            }
            try:
                self._memory = AsyncDB(
                    'memcache', params=params
                )
            except Exception as err:
                self.logger.exception(err)

    def output(self):
        return self._result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def input(self):
        if isinstance(self._component, list):
            # TODO: get an array the results from different components
            result = []
            for component in self._component:
                if component:
                    result.append(component.output())
            if len(result) == 1:
                return result[0]
            else:
                return result
        elif self._component:
            return self._component.output()
        else:
            return self._input_result

    @property
    def previous(self):
        if self._component is not None:
            return self._component
        elif self._input_result is not None:
            return self  # result data is already on component
        else:
            return None

    async def close(self):
        try:
            await self._memory.close()
        except Exception:  # pylint: disable=W0718
            pass
