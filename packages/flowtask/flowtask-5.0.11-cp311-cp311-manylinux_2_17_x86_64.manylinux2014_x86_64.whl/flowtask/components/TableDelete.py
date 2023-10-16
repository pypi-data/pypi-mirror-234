import asyncio
# logging system
import logging
import datetime
from decimal import Decimal
from typing import (
    Any
)
from collections.abc import Callable
import pandas as pd
import numpy as np
from asyncdb.exceptions import NoDataFound
from asyncdb.models import Model
from asyncdb.drivers.pg import pg
# for database
from querysource.conf import (
    sqlalchemy_url,
    default_dsn,
    DB_STATEMENT_TIMEOUT,
    DB_SESSION_TIMEOUT,
    DB_IDLE_TRANSACTION_TIMEOUT,
    DB_KEEPALIVE_IDLE
)
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from flowtask.exceptions import ComponentError, DataNotFound
from flowtask.utils import AttrDict
from .abstract import DtComponent


dtypes = {
    "varchar": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "int64": int,
    "uint64": int,
    "Int64Dtype": np.int64,
    "Int64": int,
    "Int32": int,
    "Int16": int,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "datetime64[ns, UTC]": datetime.datetime
}


class TableDelete(DtComponent):
    """
    TableDelete.

     Overview

        Merge (concat) two Dataframes in one

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  tablename   |   Yes    | Name of the table in the database                                 |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  schema      |   Yes    | Name of the schema where is to the table                          |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  flavor      |   Yes    | Database type                                                     |
    +--------------+----------+-----------+-------------------------------------------------------+
    |  close       |   Yes    | Primary key to the table in the database                          |
    +--------------+----------+-----------+-------------------------------------------------------+


    Return the list of arbitrary days


    """

    flavor: str = 'postgresql'

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.pk = []
        self.data: Any = None
        self._engine = None
        self.tablename = ''
        self.schema = ''
        try:
            self._dsn = kwargs['dsn']
        except KeyError:
            self._dsn = None
        try:
            self.multi = bool(kwargs['multi'])
            del kwargs['multi']
        except KeyError:
            self.multi = False
        super(TableDelete, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def get_engine(self, dsn: str = None):
        if not dsn:
            dsn = sqlalchemy_url
        try:
            self._engine = create_engine(
                dsn, echo=False, poolclass=NullPool)
            self._session = Session(bind=self._engine)
        except Exception as err:
            logging.exception(err)

    async def start(self, **kwargs):
        """Get Pandas Dataframe."""
        self.data = None
        if self.previous:
            self.data = self.input
        else:
            raise NoDataFound(
                "TableDelete: Data missing"
            )
        try:
            # getting sqlAlchemy engine
            self.get_engine(dsn=self._dsn)
        except Exception as err:
            raise ComponentError(
                f"Connection Error: {err}"
            ) from err
        if self.data is None:
            raise NoDataFound(
                "TableDelete: Data missing"
            )
        elif isinstance(self.data, pd.DataFrame):
            # detect data type for colums
            columns = list(self.data.columns)
            for column in columns:
                t = self.data[column].dtype
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
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    'Invalid Result type for Attribute Multiple: {err}'
                ) from err
            for name, rs in result:
                el = getattr(self, name)
                if not isinstance(rs, pd.DataFrame):
                    raise ComponentError(
                        'Invalid Resultset: not a Dataframe'
                    )
        else:
            # incompatible datasource:
            raise DataNotFound(
                "TableDelete: Incompatible Data Source"
            )

    async def close(self):
        """Closing Operations."""
        if self._engine:
            try:
                self._engine.dispose()
            except Exception:
                pass

    async def get_connection(self):  # pylint: disable=W0236,W0221
        try:
            kwargs: dict = {
                "min_size": 2,
                "server_settings": {
                    "application_name": "FlowTask.TableDelete",
                    "client_min_messages": "notice",
                    "max_parallel_workers": "512",
                    "jit": "on",
                    "statement_timeout": f"{DB_STATEMENT_TIMEOUT}",
                    "idle_session_timeout": f"{DB_SESSION_TIMEOUT}",
                    "effective_cache_size": "2147483647",
                    "tcp_keepalives_idle": f"{DB_KEEPALIVE_IDLE}",
                    "idle_in_transaction_session_timeout": f"{DB_IDLE_TRANSACTION_TIMEOUT}",
                }
            }
            return pg(
                dsn=default_dsn,
                loop=self._loop,
                **kwargs
            )
        except Exception as err:
            raise ComponentError(
                f'Error configuring TableDelete Connection: {err!s}'
            ) from err

    async def table_delete(self, elem, df):
        """ Running the process of Upsert-delete."""
        pk = elem.pk
        options = {
            "if_exists": "append",
            'index_label': pk,
            "index": False,
            "method": "multi"
        }
        if hasattr(elem, 'sql_options'):
            options = {**options, **elem.sql_options}
        tablename = elem.tablename
        try:
            schema_name = elem.schema
        except AttributeError:
            schema_name = 'public'
        options['schema'] = schema_name
        cols = []
        for field in pk:
            datatype = df.dtypes[field]

            t = dtypes[f"{datatype!s}"]
            f = (field, t)
            cols.append(f)
        # make a intermediate model:
        try:
            cls = Model.make_model(
                name=f"{tablename!s}_deleted",
                schema=schema_name,
                fields=cols
            )
            mdl = cls()  # empty model, I only need the schema
        except Exception as err:
            logging.exception(
                f'TableDelete: Error creating DB Model for {tablename}: {err}'
            )
            return False
        result = None
        if sql := mdl.model(dialect='sql'):
            print('SQL is: ', sql)
            deltable = text(f"DROP TABLE IF EXISTS {schema_name}.{tablename!s}_deleted;")
            qry = text(sql)
            try:
                with self._engine.begin() as connection:
                    connection.execute(deltable)
                    result = connection.execute(qry)
                logging.debug(
                    f'Created Temp Table: {mdl!s}'
                )
            except Exception as error:
                raise ComponentError(
                    f'Error on Table creation: {error}'
                ) from error
        else:
            raise ComponentError(
                "Cannot Create TEMP Table"
            )

        # table exists: copy data into table:
        new = df[pk].copy()
        with self._engine.begin() as connection:
            new.to_sql(
                f"{tablename!s}_deleted",
                con=connection,
                **options
            )
        # data is on temp Table, deleted
        columns = ', '.join(pk)
        # TODO: using an EXISTS instead IN to speed-up delete
        delete = f"""DELETE FROM {schema_name!s}.{tablename!s} WHERE ({columns})
        IN (SELECT {columns} FROM {schema_name}.{tablename!s}_deleted)"""
        print(delete)
        connection = await self.get_connection()
        try:
            async with await connection.connection() as conn:
                try:
                    result, error = await conn.execute(
                        sentence=delete
                    )
                    print('TableDelete: ', result)
                    self.add_metric('TABLE_DELETED', result)
                    if error:
                        raise ComponentError(
                            f'Error Deleting Data: {error}'
                        )
                    if error:
                        raise ComponentError(
                            f'Error on TableDelete: {error}'
                        )
                except Exception as err:
                    logging.error(err)
                finally:
                    # at now, delete the table:
                    drop = f"DROP TABLE IF EXISTS {schema_name}.{tablename!s}_deleted"
                    result, error = await conn.execute(
                        sentence=drop
                    )
        finally:
            await connection.close()

    async def run(self):
        """Run TableDelete."""
        if self.multi is False:
            # set the number of rows:
            numrows = len(self.data.index)
            self._variables[f'{self.TaskName}_NUMROWS'] = numrows
            await self.table_delete(self, self.data)
            self._result = self.data
            return True
        else:
            # running in multi Mode
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    'Invalid Result type for Attribute Multiple: {err}'
                ) from err
            for name, rs in result:
                try:
                    el = getattr(self, name)
                except AttributeError:
                    continue
                await self.table_delete(AttrDict(el), rs)
            # return the same dataframe
            self._result = self.data
            return True
