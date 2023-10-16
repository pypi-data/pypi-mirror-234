import asyncio
from collections.abc import Callable
import numpy as np
import pandas as pd
from asyncdb.exceptions import (
    NoDataFound
)
from flowtask.exceptions import (
    ComponentError,
    DataNotFound,
    TaskError
)
from flowtask.utils import cPrint
from .abstract import DtComponent


class AddDataset(DtComponent):
    """AddDataset.

    Join two Datasets based on some criteria.
    """
    df1 = None
    df2 = None

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self.type: str = 'left'
        self._dtypes: dict = {}
        self.infer_types: bool = False
        self.to_string: bool = True
        self.as_objects: bool = False
        super(AddDataset, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        try:
            if self._multi:
                self.df1 = self.previous[0].output()
            else:
                self.df1 = self.previous.output()
        except IndexError as ex:
            raise ComponentError(
                "Missing LEFT Dataframe"
            ) from ex
        ### check info for creating the second dataset:
        self.df2 = None
        if not hasattr(self, 'fields'):
            raise TaskError(
                "Wrong Task configuration: need *fields* declaration."
            )
        if not hasattr(self, 'dataset'):
            raise TaskError(
                "Wrong Task configuration: need *dataset* name declaration."
            )
        if not hasattr(self, 'datasource'):
            self.datasource = 'datasets'
        if self.datasource in ('datasets', 'vision'):
            # using current datasets on pg database
            self.connection = self.pg_connection()
        else:
            # TODO: add datasource logic for discovering external data.
            self.connection = self.pg_connection()
        return True

    async def run(self):
        args = {}
        if self.df1.empty:
            raise DataNotFound(
                "Data Was Not Found on Dataframe 1"
            )
        ## getting second dataset:
        try:
            ### TODO: instrumentation for getting dataset from different sources
            async with await self.connection.connection() as conn:
                fields = ', '.join(self.fields)
                if hasattr(self, 'distinct'):
                    join = ', '.join(self.join)
                    query = f"SELECT DISTINCT ON ({join}) {fields} FROM {self.datasource}.{self.dataset}"
                else:
                    query = f"SELECT {fields} FROM {self.datasource}.{self.dataset}"
                self._logger.info(f'DATASET QUERY: {query}')
                result, error = await conn.query(query)
                if error or not result:
                    raise DataNotFound(
                        "Empty Dataset"
                    )
                ## converting on Dataframe:
                self.df2 = await self.get_dataframe(result, infer_types=True)
        except (DataNotFound, NoDataFound) as exc:
            self._result = self.data
            raise DataNotFound(str(exc)) from exc
        finally:
            self.connection = None
        if self.type == 'left' and (self.df2 is None or self.df2.empty):
            self._result = self.df1
            return True
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound(
                "Data Was Not Found on Dataframe 2"
            )
        if hasattr(self, 'no_copy'):
            args['copy'] = self.no_copy
        if not self.type:
            self.type = 'left'
        elif self.type == 'inner':
            args['left_index'] = True
        if hasattr(self, 'args') and isinstance(self.args, dict):
            args = {**args, **self.args}
        if hasattr(self, 'operator'):
            operator = self.operator
        else:
            operator = 'and'
            if hasattr(self, 'join'):
                args['on'] = self.join
            else:
                args['left_index'] = True
        # making a Join between 2 dataframes
        try:
            if operator == 'and':
                df = pd.merge(
                    self.df1,
                    self.df2,
                    how=self.type,
                    suffixes=('_left', '_right'),
                    **args
                )
            else:
                if hasattr(self, 'join'):
                    args['left_on'] = self.join
                else:
                    args['left_index'] = True
                ndf = self.df1
                sdf = self.df2.copy()
                merge = []
                for key in self.join_with:
                    d = pd.merge(
                        ndf,
                        sdf,
                        right_on=key,
                        how=self.type,
                        suffixes=('_left', None),
                        **args
                    )
                    ndf = d[d[key].isnull()]
                    ndf.drop(ndf.columns[ndf.columns.str.contains(
                        '_left')], axis=1, inplace=True)
                    ddf = d[d[key].notnull()]
                    ddf.drop(ddf.columns[ddf.columns.str.contains(
                        '_left')], axis=1, inplace=True)
                    merge.append(ddf)
                # merge the last (not matched) rows
                merge.append(ndf)
                df = pd.concat(merge, axis=0)
                df.reset_index(drop=True)
                df.is_copy = None
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f'Cannot Join with missing Column: {err!s}'
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Unknown JOIN error {err!s}"
            ) from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound(
                "Cannot make any JOIN, returns zero coincidences"
            )
        self._variables[f'{self.TaskName}_NUMROWS'] = numrows
        print('ON END> ', numrows)
        self.add_metric('JOINED_ROWS', numrows)
        if self._debug is True:
            print('::: Printing Column Information === ')
            for column, t in df.dtypes.items():
                print(column, '->', t, '->', df[column].iloc[0])
        # helping some transformations
        df.is_copy = None
        self._result = df
        return True

    async def close(self):
        pass

    async def get_dataframe(self, result, infer_types: bool = False):
        self.set_datatypes()
        print(self._dtypes)
        ### TODO: using QS iterables instead
        result = [dict(row) for row in result]
        try:
            if self.as_objects is True:
                df = pd.DataFrame(
                    result,
                    dtype=object
                )
            else:
                df = pd.DataFrame(
                    result,
                    **self._dtypes
                )
        except Exception as err:  # pylint: disable=W0718
            self._logger.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        if hasattr(self, "infer_types") or infer_types is True:
            df.infer_objects()
            df = df.convert_dtypes(
                convert_string=self.to_string
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

    def set_datatypes(self):
        if hasattr(self, 'datatypes'):
            dtypes = {}
            for field, dtype in self.datatypes.items():
                if dtype == 'uint8':
                    dtypes[field] = np.uint8
                elif dtype == 'uint16':
                    dtypes[field] = np.uint16
                elif dtype == 'uint32':
                    dtypes[field] = np.uint32
                elif dtype == 'int8':
                    dtypes[field] = np.int8
                elif dtype == 'int16':
                    dtypes[field] = np.int16
                elif dtype == 'int32':
                    dtypes[field] = np.int32
                elif dtype == 'float':
                    dtypes[field] = float
                elif dtype == 'float32':
                    dtypes[field] = float
                elif dtype in ('string', 'varchar', 'str'):
                    dtypes[field] = str
                else:
                    # invalid datatype
                    self._logger.warning(
                        f'Invalid DataType value: {field} for field {dtype}'
                    )
                    continue
            if dtypes:
                self._dtypes['dtype'] = dtypes
