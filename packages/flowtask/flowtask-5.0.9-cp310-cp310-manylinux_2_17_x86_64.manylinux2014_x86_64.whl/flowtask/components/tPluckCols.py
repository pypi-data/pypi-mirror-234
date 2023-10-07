import asyncio
from typing import List
from collections.abc import Callable
import pandas
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class tPluckCols(DtComponent):
    """
    tPluckCols.

    Overview

         Return only the subset of columns from Dataframe

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  start       |   Yes    | We start by validating if the file exists, then the function      |
    |              |          | to get the data is started                                        |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  run         |   Yes    | This method allows to run the function and change its state       |
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
        self.columns: List = None
        super(tPluckCols, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "Data Was Not Found"
            )
        if not isinstance(self.data, pandas.DataFrame):
            raise ComponentError(
                "PluckCols: Only works with Pandas Dataframes"
            )
        if not self.columns:
            raise ComponentError(
                "Error: need to specify a list of *columns*"
            )

    async def run(self):
        if self.data is None:
            return False
        if isinstance(self.data, pandas.DataFrame):
            self._result = self.data[self.columns].copy()
            return self._result
        else:
            return False

    async def close(self):
        pass
