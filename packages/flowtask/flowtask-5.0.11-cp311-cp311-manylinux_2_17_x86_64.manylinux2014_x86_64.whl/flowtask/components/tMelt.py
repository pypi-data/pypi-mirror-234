import asyncio
from typing import (
    Any
)
from collections.abc import Callable
import pandas as pd
from querysource.exceptions import (
    DriverError,
    QueryException
)
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class tMelt(DtComponent):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self.df1: Any = None
        self.df2: Any = None
        self.type = None
        super(tMelt, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", code=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe",
                code=404
            )
        if not hasattr(self, 'index'):
            raise DriverError(
                "Crosstab Transform: Missing Index on definition"
            )
        if not hasattr(self, 'name'):
            self.name = 'name'
        if not hasattr(self, 'value'):
            self.name = 'value'

        if not hasattr(self, 'values'):
            self.values = None

        return True

    async def close(self):
        pass

    async def run(self):
        try:
            df = pd.melt(
                self.data,
                id_vars=self.index,
                var_name=self.name,
                value_name=self.value
            )
            self._result = df
            self.add_metric('NUM_ROWS', self._result.shape[0])
            self.add_metric('NUM_COLUMNS', self._result.shape[1])
            if self._debug:
                print('Debugging: tCrosstab ===')
                print(self._result)
                columns = list(self._result.columns)
                for column in columns:
                    t = self._result[column].dtype
                    print(column, '->', t, '->', self._result[column].iloc[0])
            return self._result
        except (ValueError, KeyError) as err:
            raise QueryException(
                f'Crosstab Error: {err!s}'
            ) from err
        except Exception as err:
            raise QueryException(
                f"Unknown error {err!s}"
            ) from err
