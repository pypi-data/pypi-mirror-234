import asyncio
from typing import (
    Any
)
from collections.abc import Callable
import pandas
from flowtask.exceptions import (
    ComponentError,
    DataNotFound
)
from .abstract import DtComponent

class tConcat(DtComponent):
    """
    tConcat.

    Overview

        Merge (concat) two Dataframes in one

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
    |  close       |   Yes    | This attribute allows me to close the process                     |
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
        self.df1: Any = None
        self.df2: Any = None
        self.type = None
        super(tConcat, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe.
        TODO: iterate over all dataframes.
        """
        if self._multi:
            self.df1 = self.previous[0].output()
            self.df2 = self.previous[1].output()
        return True

    async def run(self):
        args = {}
        if self.df1.empty:
            raise DataNotFound(
                "Data Was Not Found on Dataframe 1"
            )
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound(
                "Data Was Not Found on Dataframe 2"
            )
        if hasattr(self, 'args') and isinstance(self.args, dict):
            args = {**args, **self.args}
        if 'axis' not in args:
            args['axis'] = 1
        # Adding Metrics:
        _left = len(self.df1.index)
        self.add_metric('LEFT: ', _left)
        _right = len(self.df2.index)
        self.add_metric('RIGHT: ', _right)
        # Concat two dataframes
        try:
            df = pandas.concat([self.df1, self.df2], **args)
        except Exception as err:
            raise ComponentError(
                f"Error Merging Dataframes: {err}"
            ) from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound(
                "Concat: Cannot make any Merge"
            )
        self._variables[f'{self.TaskName}_NUMROWS'] = numrows
        self.add_metric('JOINED: ', numrows)
        df.is_copy = None
        print(df)
        self._result = df
        return self._result

    async def close(self):
        pass
