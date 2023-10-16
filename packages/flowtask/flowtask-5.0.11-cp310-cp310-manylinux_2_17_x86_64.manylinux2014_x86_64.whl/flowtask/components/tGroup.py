import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from flowtask.exceptions import ComponentError, ConfigError
from .abstract import DtComponent


class tGroup(DtComponent):
    """
    tGroup

    Overview

      Making a Group By a list of Columns.

    .. table:: Properties
       :widths: auto

    """
    condition = ''

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._columns: list = kwargs.pop('group_by', None)
        if not self._columns:
            raise ConfigError(
                "tGroup require a list of Columns for Group By => **group_by**"
            )
        super(tGroup, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", code=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe",
                code=404
            )
        return True

    async def close(self):
        pass

    async def run(self):
        self._result = None
        try:
            # Get unique region names
            df = self.data[self._columns].drop_duplicates().reset_index(drop=True)
        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err
        if hasattr(self, 'columns'):
            # returning only a subset of data
            df = df[self.columns]
        if self._debug is True:
            print('::: Printing Column Information === ')
            print('Grouped: ', df)
            for column, t in df.dtypes.items():
                print(column, '->', t, '->', df[column].iloc[0])
        self._result = df
        return True
