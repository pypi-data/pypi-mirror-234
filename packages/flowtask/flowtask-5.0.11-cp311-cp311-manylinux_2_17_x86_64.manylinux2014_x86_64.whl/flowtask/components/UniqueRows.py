import asyncio
from typing import List
from collections.abc import Callable
import pandas as pd
from asyncdb.exceptions import StatementError, DataError
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class UniqueRows(DtComponent):
    """
    UniqueRows.

        Overview

        Get Only Unique Rows from a DataFrame

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  start       |   Yes    | We initialize the component obtaining the data through the        |
    |              |          | the parameter type                                                |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  close       |   Yes    | The close method of a file object flushes any unwritten data and  |
    |              |          | closes the file object                                            |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  run         |   Yes    | This method executes the function                                 |
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
        self.unique: List = None
        super(UniqueRows, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        """Start Component"""
        if self.previous:
            self.data = self.input

    def close(self):
        """Close."""

    async def run(self):
        """Getting Unique rows from a Dataframe."""
        self._result = None
        try:
            if isinstance(self.data, pd.DataFrame):
                start = len(self.data.index)
                self.add_metric('Start', start)
                if hasattr(self, 'order'):
                    # making a pre-ordering before drop duplicates:
                    ordering = []
                    ascending = []
                    for col, order in self.order.items():
                        ordering.append(col)
                        if order == 'asc':
                            ascending.append(True)
                        else:
                            order.append(False)
                    self.data.sort_values(
                        by=ordering,
                        inplace=True,
                        ascending=ascending
                    )
                keep = {}
                if hasattr(self, 'keep'):
                    keep = {
                        "keep": self.keep
                    }
                # get only unique rows from this dataframe
                self._result = self.data.drop_duplicates(
                    self.unique, **keep
                )
                passed = len(self._result.index)
                self.add_metric('Passed', passed)
                rejected = start - passed
                self.add_metric('Rejected', rejected)
                self._variables[f'{self.TaskName}_PASSED'] = passed
                self._variables[f'{self.TaskName}_REJECTED'] = rejected
                if hasattr(self, 'save_rejected'):
                    # find elements in df1 that are not in df2
                    rejected = self._result.merge(self.data, indicator=True, how='outer')
                    rejected = rejected.loc[rejected['_merge'] != 'both']
                    filename = self.save_rejected['filename']
                    try:
                        rejected.to_csv(
                            filename,
                            sep='|'
                        )
                    except IOError:
                        self._logger.warning(f'Error writing Rejectd File: {filename}')
                    self.add_metric('rejected_file', filename)
            else:
                # return expected data
                self._result = self.data
            return self._result
        except StatementError as err:
            print(err)
            return None
        except DataError as err:
            print(err)
            raise ComponentError(
                f'UniqueRows: Error with Data: {err}'
            ) from err
