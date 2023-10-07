import asyncio
from typing import Callable
from dateutil import parser
import pandas as pd
from flowtask.exceptions import ComponentError
from .abstract import DtComponent

class SetVariables(DtComponent):
    """
    SetVariable.

    Overview

        Extract from the data a variable to set and use it in a component

    .. table:: Properties
       :widths: auto
    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | vars         |   Yes    | This attribute allows me to assign different types of variables   |
    |              |          | to print with dates format m-d-Y, it  also allows me to           |
    |              |          | establish parameters for the data with a row range of up to 5     |
    +--------------+----------+-----------+-------------------------------------------------------+


     Return the list of arbitrary days


    """

    data = None

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        super(SetVariables, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

    def close(self):
        pass

    async def run(self):
        if hasattr(self, 'vars'):
            for var, params in self.vars.items():
                variable = ''
                fname = ''
                try:
                    fname = params[0]
                except (KeyError, IndexError, ValueError) as err:
                    raise ComponentError(
                        f"Error Getting the variable definition: {err}"
                    ) from err
                try:
                    fmt = params[1]['format']
                except (KeyError, IndexError, ValueError):
                    fmt = None
                # Si existe una columna llamada fname en el dataframe se saca de ahí
                if isinstance(self.data, pd.DataFrame) and fname in self.data.columns:
                    try:
                        try:
                            row = params[1]['row']
                        except Exception:
                            row = 0
                        if isinstance(row, int):
                            variable = self.data.iloc[row][fname]
                        elif row == 'min':
                            variable = self.data[fname].min()
                        elif row == 'max':
                            variable = self.data[fname].max()
                        elif row == 'array':
                            variable = self.data[fname].unique().tolist()
                        if fmt is not None:
                            # apply Format
                            if fmt == 'date':
                                # convert to a date:
                                _var = parser.parse(str(variable))
                                variable = _var.strftime("%Y-%m-%d")
                            elif fmt == 'timestamp':
                                _var = parser.parse(str(variable))
                                variable = _var.strftime("%Y-%m-%d %H:%M:%S")
                            elif fmt == 'epoch':
                                _var = parser.parse(str(variable))
                                variable = _var.strftime('%s')
                            else:
                                try:
                                    _var = parser.parse(variable)
                                    variable = _var.strftime(fmt)
                                except (parser.ParserError, Exception):
                                    # f-string formatting:
                                    variable = f'{variable:fmt}'
                    except Exception as err:
                        raise ComponentError(
                            f"Error Getting the variable definition: {err}"
                        ) from err
                # Si no existe se saca de una función
                else:
                    try:
                        func = globals()[fname]
                        if callable(func):
                            try:
                                args = params[1]
                                variable = func(**args)
                            except (KeyError, IndexError, ValueError):
                                variable = func()
                            if fmt is not None:
                                print('VAR ', variable)
                    except Exception as err:
                        raise ComponentError(
                            f"Error Getting the variable definition: {err}"
                        ) from err
                self.add_metric(f"{var}!s", variable)
                self._variables[f'{self.TaskName}_{var}'] = variable
                print('VAR: ', f'{self.TaskName}_{var}', variable)
        self._result = self.data
        return self._result
