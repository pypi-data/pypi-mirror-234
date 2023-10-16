"""RESTClient.

Basic component for making RESTful queries to URLs.
"""
import asyncio
from abc import ABC
from typing import (
    List,
    Dict,
    Union
)
from collections.abc import Callable
from urllib.parse import urlencode
from navconfig.logging import logging
from flowtask.exceptions import (
    DataNotFound,
    ComponentError
)
from .HTTPClient import HTTPClient


class RESTClient(HTTPClient):
    """
    RESTClient.

    Overview

         This Component Inherits the HTTPClient method

    .. table:: Properties
       :widths: auto

    Return the list of arbitrary days

    """


    accept: str = 'application/json' # by default


    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self._result: Union[List, Dict] = None
        self.accept: str = 'application/json' # by default
        super(RESTClient, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def run(self):
        self.url = self.build_url(
            self.url,
            args=self._arguments,
            queryparams=urlencode(self.parameters)
        )
        try:
            result, error = await self.request(
                self.url, self.method
            )
            if not result:
                raise DataNotFound(
                    f"Data was not found on: {self.url}"
                )
            elif error is not None:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(
                        f"RESTClient Error: {error}"
                    )
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(
                f"RESTClient Error: {err}"
            ) from err
        # at here, processing Result
        if self.as_dataframe is True:
            try:
                result = self.create_dataframe(result)
            except Exception as err:
                raise ComponentError(
                    f"RESTClient Error: {err}"
                ) from err
        self._result = result
        return self._result



class AbstractREST(RESTClient, ABC):
    """AbstractREST.
        Abstract Method for RESTful Components.
    """
    _default_method: str = None
    base_url: str = None

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self._result: Union[List, Dict] = None
        self.accept: str = 'application/json' # by default
        self.url: str = None
        try:
            self._method = kwargs['method']
            del kwargs['method']
        except KeyError:
            self._method = self._default_method
        super(AbstractREST, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self._args = self._params

    async def start(self, **kwargs):
        if not hasattr(self, self._method):
            raise ComponentError(
                f'{self.__name__} Error: has no Method {self._method}'
            )
        await super(AbstractREST, self).start(
            **kwargs
        )

    async def run(self):
        method = getattr(self, self._method)
        try:
            await method()
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(
                f"{self.__name__}: Error calling Method {self._method}: {err}"
            ) from err
        self.url = self.build_url(
            self.url,
            args=self._arguments,
            queryparams=urlencode(self.parameters)
        )
        try:
            result, error = await self.request(
                self.url, self.method
            )
            print('RESULT ', result, error)
            if self._debug:
                print(result)
            if not result:
                raise DataNotFound(
                    f"Data was not found on: {self.url}"
                )
            elif error is not None:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(
                        f"HTTPClient Error: {error}"
                    )
            # at here, processing Result
            if self.as_dataframe is True:
                try:
                    result = self.create_dataframe(result)
                    if self._debug is True:
                        print(result)
                        print('::: Printing Column Information === ')
                        for column, t in result.dtypes.items():
                            print(column, '->', t, '->', result[column].iloc[0])
                except Exception as err:
                    raise ComponentError(
                        f"HTTPClient Error: {err}"
                    ) from err
            self._result = result
            return self._result
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise ComponentError(
                f"HTTPClient Error: {err}"
            ) from err
