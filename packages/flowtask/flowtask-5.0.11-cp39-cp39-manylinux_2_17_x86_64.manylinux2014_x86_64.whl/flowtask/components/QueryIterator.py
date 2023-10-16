import asyncio
from decimal import Decimal
from typing import Any
from collections.abc import Callable
from pathlib import Path, PurePath
from aiofile import AIOFile
import numpy as np
import pandas as pd
from navconfig.logging import logging
from asyncdb.exceptions import NoDataFound, ProviderError
from querysource.queries.qs import QS
from flowtask.conf import TASK_PATH
from flowtask.exceptions import (
    ComponentError,
    NotSupported,
    DataNotFound,
    FileError
)
from .IteratorBase import IteratorBase


class QueryIterator(IteratorBase):
    """
    QueryIterator.

    Creates a Pandas Iterator from a QuerySource query.
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.pk = []
        self.data = None
        self._iterator: Any = None
        self._variables = {}
        self.vars = {}
        self._columns = []
        self._query: str = None
        try:
            self.use_template: bool = bool(kwargs['use_template'])
            del kwargs['use_template']
        except KeyError:
            self.use_template: bool = False
        super(QueryIterator, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

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
                f'{self.__name__}: Missing SQL File: {file}'
            )

    async def start(self, **kwargs):
        """Getting kind of Query."""
        if hasattr(self, 'file_sql'):
            try:
                file_path = Path(TASK_PATH).joinpath(
                    self._program, 'sql', self.file_sql
                )
                if file_path.exists() and file_path.is_file():
                    self._query = await self.open_sqlfile(file_path)
            except Exception as e:
                raise FileError(
                    f'File SQL doesn\'t exists: {self.file_sql!s}, {e}'
                ) from e
        elif hasattr(self, 'query_slug'):
            self.query_slug = self.mask_replacement(
                self.query_slug
            )
            self._query = self.query_slug
        elif hasattr(self, 'query'):
            self._query = self.query
            if hasattr(self, 'masks'):
                self._query = self.mask_replacement(
                    self._query
                )
                try:
                    self._query = self._query.format(**self._variables)
                except Exception as err:
                    print('Error replacing Vars in Query: ', err)
        if hasattr(self, 'conditions'):
            self.set_conditions('conditions')
        return True

    async def close(self, job=None):
        close = getattr(job, 'close', None)
        if job:
            if asyncio.iscoroutinefunction(close):
                await job.close()
            else:
                job.close()

    def createJob(self, target, params, row):
        """Create the Job Component."""
        self._result = self.data
        dt = {}
        for column in self._columns:
            value = row[column]
            if isinstance(value, (int, np.int64, np.integer)):
                value = int(value)
            elif isinstance(value, (float, Decimal)):
                value = float(value)
            self.setVar(column, value)
            # print('ITER ', value, type(value))
            params[column] = value
            dt[column] = value
        for name, value in self.vars.items():
            # TODO: check this logic
            print('VARS: ', name, value, column)
            val = row[column]
            # print('VAL ', val)
            # need to build this attribute
            if isinstance(value, list):
                pass
                # TODO: logic to use functions with dataframes
            #     # need to calculate the value
            else:
                if '{' in str(value):
                    value = value.format(**dt)
                else:
                    value = val
            params[name] = value
            self.setVar(name, value)
        return self.get_job(target, **params)

    async def run(self):
        """Async Run Method."""
        # first: getting data:
        df = None
        result = None
        if not self._query:
            raise ComponentError(
                'QueryToPandas: Empty Query/Slug or File'
            )
        if hasattr(self, 'query') or hasattr(self, 'file_sql'):
            try:
                connection = self.get_connection(event_loop=self._loop)
            except Exception as err:
                logging.exception(err, stack_info=True)
                raise
            async with await connection.connection() as conn:
                try:
                    res, error = await conn.query(self._query)
                    if error:
                        logging.error(f'QueryIterator: {error}')
                        raise NoDataFound(error)
                    result = [dict(row) for row in res]
                    df = await self.get_dataframe(
                        result
                    )
                except NoDataFound:
                    result = []
                except Exception as err:
                    logging.error(err)
                    raise
        elif hasattr(self, 'query_slug'):
            conditions = {}
            if hasattr(self, 'conditions'):
                conditions = self.conditions
            result = await self.get_query(self._query, conditions)
            df = await self.get_dataframe(
                result
            )
        else:
            raise NotSupported(
                f"{self.__name__}: Method not allowed"
            )
        # getting the iterator:
        if not hasattr(self, 'columns'):
            # iterate over the total columns of dataframe
            self._columns = df.columns
        else:
            self._columns = self.columns
        self._iterator = df.iterrows()
        # iterate over next task
        step, target, params = self.get_step()
        step_name = step.name
        for index, row in self._iterator:
            logging.debug(f'ITER: index:{index} row: {row}')
            # iterate over every row
            # get I got all values, create a job:
            job = self.createJob(target, params, row)
            # print('JOB: ', job)
            if job:
                try:
                    self._result = await self.async_job(job, step_name)
                except (NoDataFound, DataNotFound) as err:
                    # its a data component a no data was found
                    logging.debug(
                        f'Data not Found for Task {step_name}, got: {err}'
                    )
                    continue
                except (ProviderError, ComponentError) as err:
                    raise ComponentError(
                        f"Error on {step_name}, error: {err}"
                    ) from err
                except NotSupported as err:
                    raise NotSupported(
                        f"Not Supported: {err}") from err
                except Exception as err:
                    raise ComponentError(
                        f"Component Error {step_name}, error: {err}"
                    ) from err
                finally:
                    await self.close(job)
        # returning last value generated by iteration
        return self._result

    async def get_dataframe(self, result) -> pd.DataFrame:
        try:
            df = pd.DataFrame(
                result
            )
        except Exception as err:
            logging.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        df.infer_objects()
        df = df.convert_dtypes(
            convert_string=True
        )
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how='all', inplace=True)
            df.dropna(axis=0, how='all', inplace=True)
        if hasattr(self, 'dropna'):
            df.dropna(subset=self.dropna, how='all', inplace=True)
        return df

    async def get_query(self, slug, conditions: dict = None):
        result: Any = []
        if not conditions:
            conditions = self.conditions
        try:
            qry = QS(
                slug=slug,
                conditions=conditions,
                loop=self._loop,
                lazy=True
            )
            await qry.get_query()
        except (DataNotFound, NoDataFound) as ex:
            raise DataNotFound(f"{ex!s}") from ex
        except Exception as err:
            raise ComponentError(f'{err}') from err
        try:
            res, error = await qry.query()
            if not res:
                raise NoDataFound(
                    f'{slug}: Data Not Found'
                )
            if error:
                raise ComponentError(
                    f"Error on Query: {error}"
                )
            result = result + [dict(row) for row in res]
            return result
        except (DataNotFound, NoDataFound) as err:
            raise DataNotFound(
                f"{err!s}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Error on Query: {err}"
            ) from err
        finally:
            try:
                await qry.close()
            except Exception as err:
                logging.exception(err, stack_info=True)
