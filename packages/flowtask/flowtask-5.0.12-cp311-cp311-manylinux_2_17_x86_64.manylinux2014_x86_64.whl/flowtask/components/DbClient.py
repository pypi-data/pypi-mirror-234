from abc import ABC
from typing import (
    Union
)
from pathlib import PurePath
from aiofile import AIOFile
import pandas
from asyncdb import BaseProvider
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from flowtask.utils import cPrint
from flowtask.utils.functions import is_empty, as_boolean
from flowtask.exceptions import (
    ComponentError,
    FileError,
    DataNotFound
)
from .interfaces import DBInterface


class DbClient(DBInterface, ABC):
    """
    DbClient.

        Overview

        Abstract Class for Database connections using AsyncDB.

        .. table:: Properties
        :widths: auto

        +---------------+----------+-----------+-------------------------------------------------------+
        | Name          | Required | Summary                                                           |
        +---------------+----------+-----------+-------------------------------------------------------+
        |  DbClient     |   Yes    | Client schema definition file                                     |
        +---------------+----------+-----------+-------------------------------------------------------+
        |  _init_       |   Yes    | Component for Data Integrator                                     |
        +---------------+----------+-----------+-------------------------------------------------------+
        |  close        |   Yes    | This attribute allows me to close the process                     |
        +---------------+----------+-----------+-------------------------------------------------------+
        | open_sqlfile  |   Yes    | Open an sql file to run it                                        |
        +---------------+----------+-----------+-------------------------------------------------------+
        | _query        |   Yes    | Establishes an asynchronous connection with the database provider |
        +---------------+----------+-----------+-------------------------------------------------------+
        | get_dataframe |   Yes    | Obtains a two-dimensional data structure in which data of         |
        |               |          | different types can be stored                                     |
        +-------------- +----------+-----------+-------------------------------------------------------+


    """
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str
    }

    def __init__(self, driver: str, credentials: dict, **kwargs) -> None:
        super(DbClient, self).__init__(
            driver=driver,
            credentials=credentials,
            **kwargs
        )
        try:
            self.raw_result: bool = kwargs['raw_result']
            del kwargs['raw_result']
        except KeyError:
            self.raw_result: bool = False
        try:
            self.infer_types: bool = as_boolean(kwargs['infer_types'])
            del kwargs['infer_types']
        except KeyError:
            self.infer_types: bool = False
        try:
            self.as_dataframe: bool = as_boolean(kwargs['as_dataframe'])
            del kwargs['as_dataframe']
        except KeyError:
            self.as_dataframe: bool = True
        try:
            self.as_string: bool = as_boolean(kwargs['as_string'])
            del kwargs['as_string']
        except KeyError:
            self.as_string: bool = False  # using "string" instead objects in pandas
        if self.as_string is True:
            self.infer_types = True
        # any other argument
        self._args = kwargs

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        if file.exists() and file.is_file():
            content = None
            # open SQL File:
            async with AIOFile(file, 'r+') as afp:
                content = await afp.read()
                # check if we need to replace masks
            if hasattr(self, 'masks'):
                content = self.mask_replacement(
                    content
                )
            if self.use_template is True:
                content = self._templateparser.from_string(
                    content, kwargs
                )
            return content
        else:
            raise FileError(
                f'{__name__}: Missing SQL File: {file}'
            )

    async def close(self, connection: BaseProvider = None) -> None:
        if not connection:
            connection = self._connection
        try:
            if connection is not None:
                await connection.close()
        except Exception as err:  # pylint: disable=W0703
            logging.error(
                f'DbClient Closing error: {err}'
            )

    async def _query(self, query: str, connection: BaseProvider = None) -> Union[list, dict]:
        if not connection:
            connection = self._connection
        try:
            result, error = await connection.query(query)
            if error:
                raise ComponentError(
                    f"DbClient: Query Error: {error}"
                )
            if self.raw_result is True:
                return result
            else:  # converting to dict
                result = [dict(row) for row in result]
                return result
        except (DataNotFound, NoDataFound) as err:
            raise DataNotFound(
                "DbClient: Data not found"
            ) from err
        except Exception as err:
            raise ComponentError(f"{err}") from err

    async def get_dataframe(self, result):
        try:
            df = pandas.DataFrame(
                result
            )
        except Exception as err:  # pylint: disable=W0703
            logging.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        if is_empty(df):
            raise DataNotFound(
                "DbClient: Data not Found"
            )
        df.infer_objects()
        if self.infer_types is True:
            df = df.convert_dtypes(
                convert_string=self.as_string
            )
        if self._debug is True:
            cPrint('Data Types:')
            print(df.dtypes)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how='all', inplace=True)
            df.dropna(axis=0, how='all', inplace=True)
        if hasattr(self, 'dropna'):
            df.dropna(subset=self.dropna, how='all', inplace=True)
        if hasattr(self, 'clean_strings') and getattr(self, 'clean_strings', False) is True:
            u = df.select_dtypes(include=['object', 'string'])
            df[u.columns] = u.fillna('')
        return df
