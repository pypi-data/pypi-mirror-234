import asyncio
import logging
from collections.abc import Callable
import pandas as pd
from flowtask.exceptions import ComponentError, DataNotFound
from flowtask.components import DtComponent
from flowtask.utils import AttrDict
from .postgres import PgOutput
from .mysql import MysqlOutput
from .sa import SaOutput

class TableOutput(DtComponent):
    """
    TableOutput: copy data to SQL table.

        Copy data into a Table using Pandas/SQLalchemy features and
        INSERT-UPDATE mechanism
    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self._pk = []
        self._fk: str = None
        self.data = None
        self._engine = None
        self._columns: list = []
        self._schema: str = ''
        self._constraint: list = None
        try:
            self._dsn = kwargs['dsn']
            del kwargs['dsn']
        except KeyError:
            self._dsn = None
        try:
            self.flavor = kwargs['flavor']
            del kwargs['flavor']
        except KeyError:
            self.flavor = 'postgresql'
        try:
            self.multi: bool = bool(kwargs['multi'])
            del kwargs['multi']
        except KeyError:
            self.multi: bool = False
        super(TableOutput, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def constraints(self):
        return self._constraint

    def get_schema(self):
        return self._schema

    def foreign_keys(self):
        return self._fk

    def primary_keys(self):
        return self._pk

    async def start(self, **kwargs):
        """Get Pandas Dataframe."""
        self.data = None
        if self.flavor == 'postgres':
            self._engine = PgOutput(parent=self)
        elif self.flavor == 'mysql':
            self._engine = MysqlOutput(parent=self)
        elif self.flavor == 'sqlalchemy':
            self._engine = SaOutput(parent=self, dsn=self._dsn)
        else:
            raise ComponentError(
                'TableOutput: unsupported DB flavor: {self.flavor}'
            )
        if self.previous:
            self.data = self.input
        else:
            raise DataNotFound(
                "Previous Data was Not Found"
            )
        if self.data is None:
            raise DataNotFound(
                "TableOutput: Data missing"
            )
        elif isinstance(self.data, pd.DataFrame):
            # detect data type for colums
            columns = list(self.data.columns)
            for column in columns:
                t = self.data[column].dtype
                # print(column, '->', t, '->', self.data[column].iloc[0])
                if isinstance(t, pd.core.dtypes.dtypes.DatetimeTZDtype):
                    self.data[column] = pd.to_datetime(
                        self.data[column],
                        format='%Y-%m-%dT%H:%M:%S.%f%z',
                        cache=True,
                        utc=True
                    )
                    self.data[column].dt.tz_convert('UTC')
                elif str(t) == 'datetime64[ns]':
                    tmp_data = self.data.copy()
                    tmp_data[column] = pd.to_datetime(
                        self.data[column],
                        format='%Y-%m-%dT%H:%M:%S.%f%z',
                        cache=True,
                        utc=True
                    )
                    self.data = tmp_data.copy()
                else:
                    # this is an special column from RethinkDB
                    # rethinkdb.ast.RqlTzinfo
                    if column == 'inserted_at':
                        try:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                format='%Y-%m-%dT%H:%M:%S.%f%z',
                                cache=True,
                                utc=True
                            )
                        except ValueError:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                # format='%Y-%m-%d %H:%M:%S.%f+%z',
                                cache=True,
                                utc=True
                            )
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    f'Invalid Result type for Multiple: {err}'
                ) from err
            for name, rs in result:
                if hasattr(self, name):
                    el = getattr(self, name)
                    print(el)
                    if not isinstance(rs, pd.DataFrame):
                        raise ComponentError(
                            'Invalid Resultset: not a Dataframe'
                        )

    def close(self):
        """Closing Operations."""
        try:
            self._engine.close()
        except Exception as err:
            logging.error(err)

    async def table_output(self, elem, datasource):
        # get info
        options = {
            'chunksize': 100
        }
        table = elem.tablename
        try:
            schema = elem.schema
        except AttributeError:
            schema = 'public'
        options['schema'] = schema
        # starting metric:
        try:
            data = {
                'NUM_ROWS': datasource.shape[0],
                'NUM_COLUMNS': datasource.shape[1]
            }
            self.add_metric(f"{schema}.{table}", data)
        except Exception:
            pass
        if hasattr(elem, 'sql_options'):
            options = {**options, **elem.sql_options}
        if hasattr(elem, 'pk') or hasattr(elem, 'constraint'):
            options["index"] = False
        if hasattr(elem, 'if_exists'):
            options['if_exists'] = elem.if_exists
        else:
            options['if_exists'] = 'append'
        # define index:
        try:
            self._pk = elem.pk
            options['index_label'] = self._pk
        except AttributeError:
            self._pk = []
        # set the upsert method:
        options['method'] = self._engine.db_upsert
        if hasattr(elem, 'foreign_key'):
            self._fk = elem.foreign_key
        else:
            self._fk = None
        if hasattr(elem, 'constraint'):
            self._constraint = elem.constraint
        else:
            self._constraint = None
        self._columns = list(datasource.columns)
        self._engine.columns = self._columns
        self._schema = schema
        # add metrics for Table Output
        u = datasource.select_dtypes(include=['object', 'string'])
        datasource[u.columns] = u.replace(['<NA>', 'None'], None)
        try:
            datasource.to_sql(
                name=table,
                con=self._engine.engine(),
                **options
            )
            logging.debug(
                f':: Saving Table Data {schema}.{table} ...'
            )
            return True
        except Exception as exc:
            raise ComponentError(
                f"{exc}"
            ) from exc

    async def run(self):
        """Run TableOutput."""
        try:
            self._result = None
            if self.multi is False:
                # set the number of rows:
                self._variables['{self.TaskName}_NUMROWS'] = len(self.data.index)
                await self.table_output(self, self.data)
                self._result = self.data
                try:
                    self.add_metric(
                        'ROWS_SAVED',
                        len(self.data.index)
                    )
                except (TypeError, ValueError):
                    pass
                return self._result
            else:
                # running in multi Mode
                try:
                    result = self.data.items()
                except Exception as err:
                    raise ComponentError(
                        f'Invalid Result type for Multiple: {err}'
                    ) from err
                for name, rs in result:
                    try:
                        el = getattr(self, name)
                    except AttributeError:
                        continue
                    await self.table_output(
                        AttrDict(el), rs
                    )
                    # set the number of rows:
                    self._variables[f'{self.TaskName}_{name}_NUMROWS'] = len(rs.index)
                # return the same dataframe
                self._result = self.data
                try:
                    self.add_metric(
                        'ROWS_SAVED',
                        self._engine.result()
                    )
                except Exception as err:
                    logging.error(err)
                return self._result
        except ValueError as err:
            raise ComponentError(
                f"Value Error: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"TableOutput: {err}"
            ) from err
