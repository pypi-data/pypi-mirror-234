
import asyncio
from typing import Dict
from collections.abc import Callable
from pathlib import Path
import csv
import numpy as np
import pandas as pd
from flowtask.exceptions import ComponentError
from .abstract import DtComponent

excel_based = [
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel"
]


class PandasToFile(DtComponent):
    '''
    PandasToFile.

    Overview

        This component allows download files to identify their extension and path

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  filename    |   Yes    | Validate the name of the file and its location                    |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  mime        |   Yes    | Identifies the file type                                          |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  pd_args     |   No     | Send all component attributes Send all component attributes       |
    |              |          | directly to an asynchronous Pandas function                       |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  sep         |   Yes    | Make a separation of the file name with this sign                 |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  masks       |   Yes    | A mask is applied with the today attribute, with date             |
    |              |          | format {“Y-m-d”}                                                  |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days
    '''
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self.zerofill: bool = False
        self.quoting = None
        self.params: Dict = {}
        self.args: Dict = {}
        self.filename: str = None
        self.directory: str = None
        self.mime: str = 'text/csv'
        super(PandasToFile, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        if hasattr(self, 'pd_args'):
            self.args = getattr(self, 'pd_args', {})

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe: hint> add \"export_dataframe\"\
                :true to tMap component"
            )
        if hasattr(self, 'masks'):
            self.filename = self.mask_replacement(self.filename)
        # Create directory if not exists
        try:
            if not self.directory:
                self.directory = Path(self.filename).parents[0]
            self.directory.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            self._logger.error(
                f'Error creating directory {self.directory}: {err}'
            )
            raise ComponentError(
                f'Error creating directory {self.directory}: {err}'
            ) from err

    async def close(self):
        pass

    async def run(self):
        if self.zerofill:
            cols = self.data.select_dtypes(include=["object", "string"])
            self.data[cols.columns] = cols.fillna('0')
            # self.data.fillna('0', inplace=True)
            self.data.replace(np.nan, 0)
            intcols = self.data.select_dtypes(include=["Int64"])
            self.data[intcols.columns] = intcols.fillna(0)
        try:
            #filename, file_extension = os.path.splitext(self.filename)
            if self.mime == 'text/csv' or self.mime == 'text/plain':
                if self.quoting == 'all':
                    quoting = csv.QUOTE_ALL
                elif self.quoting == 'string':
                    quoting = csv.QUOTE_NONNUMERIC
                else:
                    quoting = csv.QUOTE_NONE
            #if file_extension == '.csv':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
                self._logger.debug(f'PandasToFile: Export to CSV: {self.filename}')
                self.data.to_csv(
                    self.filename,
                    index=False,
                    quoting=quoting,
                    quotechar='"',
                    escapechar='\\',
                    **self.args
                )
            elif self.mime in excel_based:
                #elif file_extension == '.xlsx':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
                self._logger.debug(f'PandasToFile: Export to EXCEL: {self.filename}')
                self.data.to_excel(
                    self.filename,
                    index=False,
                    **self.args
                )
            elif self.mime == 'application/json':
                #elif file_extension == '.json':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
                self._logger.debug(f'PandasToFile: Export to JSON: {self.filename}')
                self.data.to_json(
                    self.filename,
                    index=False,
                    **self.args
                )
            else:
                raise ComponentError(
                    'Error: Only extension supported: csv, xlsx and json are supported'
                )
            self._result = self.filename
            return self._result
        except Exception as err:
            raise ComponentError(
                f'Error in PandasToFile: {err}'
            ) from err
