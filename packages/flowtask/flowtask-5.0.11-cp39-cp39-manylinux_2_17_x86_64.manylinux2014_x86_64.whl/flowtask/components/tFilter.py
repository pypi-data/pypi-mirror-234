import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class tFilter(DtComponent):
    """
    tFilter

    Overview

      Apply a Filter to a Pandas Dataframe.

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | operator     |   Yes    |  Allows to identify the type of operator                          |
    +--------------+----------+-----------+-------------------------------------------------------+
    | conditions   |   Yes    | The {“column”} attribute: It is the  name of the column           |
    |              |          | that we are going to extract, "{value}" : It is the value that    |
    |              |          | we will assign to the extracted column                            |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days

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
        self.condition: str = ''
        super(tFilter, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

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
        if hasattr(self, 'filter'):
            try:
                if len(self.filter) > 1:
                    if not hasattr(self, 'operator'):
                        raise ComponentError(
                            "Operator not found",
                            code=404
                        )
                    conditions = []
                    for cond in self.filter:
                        value = cond['value']
                        if isinstance(value, str):
                            cond['value'] = "'{}'".format(value)
                            conditions.append("(self.data['{column}'] {expression} {value})".format_map(cond))
                        if isinstance(value, list):
                            if cond['expression'] == '==':
                                conditions.append("(self.data['{column}'].isin({value}))".format_map(cond))
                            elif cond['expression'] == '!=':
                                # not:
                                conditions.append("(~self.data['{column}'].isin({value}))".format_map(cond))
                        # self.condition = f'{self.condition} {self.operator} ' if self.condition else ''
                    # apply:
                    self.condition = f' {self.operator} '.join(conditions)
                    print('CONDITION >> ', self.condition)
                    self.data = self.data.loc[eval(self.condition)]  # pylint: disable=W0123
                else:
                    cond = self.filter[0]
                    column = cond['column']
                    val = cond['value']
                    if isinstance(val, list):
                        self.data = self.data.loc[self.data[column].isin(val)]
                    else:
                        self.condition = '(self.data.{column} {expression} {value})'.format_map(
                            cond
                        )
                        self.data = self.data.loc[eval(self.condition)]  # pylint: disable=W0123
            except Exception as err:
                raise ComponentError(
                    f"Generic Error on Data: error: {err}"
                ) from err
            print('Filtered: ', self.data)
        if hasattr(self, 'columns'):
            # returning only a subset of data
            self.data = self.data[self.columns]
        if self._debug is True:
            print('::: Printing Column Information === ')
            for column, t in self.data.dtypes.items():
                print(column, '->', t, '->', self.data[column].iloc[0])
        self._result = self.data
        return self._result
