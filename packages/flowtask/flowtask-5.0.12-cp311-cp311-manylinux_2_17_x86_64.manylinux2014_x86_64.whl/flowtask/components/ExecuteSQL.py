import asyncio
from collections.abc import Callable
from pathlib import PurePath
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from aiofile import AIOFile
from asyncdb.drivers.pg import pg
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from querysource.conf import (
    default_dsn,
    DB_STATEMENT_TIMEOUT,
    DB_SESSION_TIMEOUT,
    DB_IDLE_TRANSACTION_TIMEOUT,
    DB_KEEPALIVE_IDLE
)
from navconfig.logging import logging

from flowtask.exceptions import (
    ComponentError,
    FileError
)
from flowtask.utils import SafeDict
from settings.settings import TASK_PATH
from .abstract import DtComponent


class ExecuteSQL(DtComponent):
    """
    ExecuteSQL

    Overview

            Does not support mutually exclusive data sources: query,file sql.
            The ExecuteSQL only does WARNING if it fails

        .. table:: Properties
        :widths: auto


    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    | use_template |   Yes    | Pass the content of the SQL through a Jinja2 processor.|
    |              |          | Receive component variables                            |
    +--------------+----------+-----------+--------------------------------------------+
    | multi        |   Yes    | Is True, there are multiple queries. to execute        |
    +--------------+----------+-----------+--------------------------------------------+


    Return the list of arbitrary days.

    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.tablename: str = ''
        self.schema: str = ''
        self._connection: Callable = None
        self._queries = []
        self.exec_timeout: float = 3600000.0
        try:
            self.multi = bool(kwargs['multi'])
            del kwargs['multi']
        except KeyError:
            self.multi = False
        try:
            self.use_template: bool = bool(kwargs['use_template'])
            del kwargs['use_template']
        except KeyError:
            self.use_template: bool = False
        super(ExecuteSQL, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # set the program:
        if hasattr(self, 'program'):
            self._program = self.program

    async def close(self):
        """Closing Database Connection."""

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        content = None
        self._logger.info(f'Open SQL File: {file}')
        if file.exists() and file.is_file():
            # open SQL File:
            async with AIOFile(file, 'r+') as afp:
                content = await afp.read()
                # check if we need to replace masks
                if '{' in content:
                    content = self.mask_replacement(
                        content
                    )
            if self.use_template is True:
                content = self._templateparser.from_string(
                    content,
                    kwargs
                )
            return content
        else:
            raise FileError(
                f'ExecuteSQL: Missing SQL File: {file}'
            )

    async def start(self, **kwargs):
        """Start Component"""
        if self.previous:
            self.data = self.input
        # check if sql comes from a filename:
        if hasattr(self, 'file_sql'):
            self._logger.debug(
                f"SQL File: {self.file_sql}"
            )
            self._queries = []
            qs = []
            if isinstance(self.file_sql, str):
                qs.append(self.file_sql)
            elif isinstance(self.file_sql, list):
                qs = self.file_sql
            else:
                raise ComponentError(
                    'ExecuteSQL: Unknown type for *file_sql* attribute.'
                )
            for fs in qs:
                self._logger.debug(
                    f'Execute SQL File: {fs!s}'
                )
                file_path = TASK_PATH.joinpath(self._program, 'sql', fs)
                try:
                    sql = await self.open_sqlfile(file_path)
                    self._queries.append(sql)
                except Exception as err:
                    raise ComponentError(
                        f"{err}"
                    ) from err
        if hasattr(self, 'pattern'):
            # need to parse variables in SQL
            pattern = self.pattern
            self._queries = []
            try:
                variables = {}
                for field, val in pattern.items():
                    variables[field] = self.getFunc(val)
            except (TypeError, AttributeError) as err:
                self._logger.error(err)
            # replace all ocurrences on SQL
            try:
                # TODO: capture when sql is a list of queries
                sql = self.sql.format_map(SafeDict(**variables))
                # Replace variables
                for val in self._variables:
                    if isinstance(self._variables[val], list):
                        if isinstance(self._variables[val], int):
                            self._variables[val] = ', '.join(self._variables[val])
                        else:
                            self._variables[val] = ', '.join(
                                "'{}'".format(v) for v in self._variables[val]
                            )
                    sql = sql.replace(
                        '{{{}}}'.format(str(val)), str(self._variables[val])
                    )
                self._queries.append(sql)
            except Exception as err:
                logging.exception(err, stack_info=True)
        if hasattr(self, 'sql'):
            if isinstance(self.sql, str):
                self._queries = [self.sql]
            elif isinstance(self.sql, list):
                self._queries = self.sql
        # Replace variables
        for val in self._variables:
            sqls = []
            for sql in self._queries:
                if isinstance(self._variables[val], list):
                    if isinstance(self._variables[val], int):
                        self._variables[val] = ', '.join(self._variables[val])
                    else:
                        self._variables[val] = ', '.join(
                            "'{}'".format(v) for v in self._variables[val]
                        )
                sql = sql.replace(
                    '{{{}}}'.format(str(val)),
                    str(self._variables[val])
                )
                sqls.append(sql)
            self._queries = sqls
        return True

    def get_connection(self, event_loop: asyncio.AbstractEventLoop):
        kwargs: dict = {
            "min_size": 2,
            "server_settings": {
                "application_name": "FlowTask.ExecuteSQL",
                "client_min_messages": "notice",
                "max_parallel_workers": "512",
                "jit": "off",
                "statement_timeout": f"{DB_STATEMENT_TIMEOUT}",
                "idle_session_timeout": f"{DB_SESSION_TIMEOUT}",
                "effective_cache_size": "2147483647",
                "tcp_keepalives_idle": f"{DB_KEEPALIVE_IDLE}",
                "idle_in_transaction_session_timeout": f"{DB_IDLE_TRANSACTION_TIMEOUT}",
            },
        }
        return pg(
            dsn=default_dsn,
            loop=event_loop,
            **kwargs
        )

    async def _execute(self, query, event_loop):
        try:
            connection = self.get_connection(event_loop)
            async with await connection.connection() as conn:
                if hasattr(self, 'background'):
                    future = asyncio.create_task(
                        conn.execute(query)
                    )
                    # query will be executed in background
                    _, pending = await asyncio.wait(
                        [future],
                        timeout=self.exec_timeout,
                        return_when='ALL_COMPLETED'
                    )
                    if future in pending:
                        ## task reachs timeout
                        for t in pending:
                            t.cancel()
                        raise asyncio.TimeoutError(
                            f"Query {query!s} was cancelled due timeout."
                        )
                    result, error = future.result()
                else:
                    try:
                        result, error = await conn.execute(query)
                    except asyncio.TimeoutError as exc:
                        raise asyncio.TimeoutError(
                            f"Query {query!s} was cancelled due Timeout."
                        ) from exc
                    except Exception as exc:
                        raise ComponentError(
                            f"ExecuteSQL Error: {exc!s}"
                        ) from exc
                    # try:
                    #     res = await asyncio.wait_for(
                    #         future, timeout=self.exec_timeout
                    #     )
                    #     result, error = res
                    # except asyncio.TimeoutError as exc:
                    #     raise asyncio.TimeoutError(
                    #         f"Query {query!s} was cancelled due timeout."
                    #     ) from exc
                if error:
                    raise ComponentError(
                        f"Execute SQL error: {result!s} err: {error!s}"
                    )
                else:
                    return result
        except StatementError as err:
            raise StatementError(
                f"Statement error: {err}"
            ) from err
        except DataError as err:
            raise DataError(
                f"Data error: {err}"
            ) from err
        except ComponentError:
            raise
        except Exception as err:
            raise ComponentError(
                f"ExecuteSQL error: {err}"
            ) from err
        finally:
            connection = None

    def execute_sql(self, query: str, event_loop: asyncio.AbstractEventLoop) -> str:
        asyncio.set_event_loop(event_loop)
        if self._debug:
            self._logger.verbose(
                f"::: Exec SQL: {query}"
            )
        future = event_loop.create_task(
            self._execute(
                query, event_loop
            )
        )
        try:
            result = event_loop.run_until_complete(
                future
            )
            st = {
                "sql": query,
                "result": result
            }
            self.add_metric('EXECUTED', st)
            return result
        except Exception as err:
            self.add_metric('QUERY_ERROR', str(err))
            self._logger.error(
                f"{err}"
            )

    async def run(self):
        """Run Raw SQL functionality."""
        try:
            _new = True
            event_loop = asyncio.new_event_loop()
        except RuntimeError:
            event_loop = asyncio.get_running_loop()
            _new = False
        ct = len(self._queries)
        if ct <= 0:
            ct = 1
        result = []
        try:
            loop = asyncio.get_event_loop()
            asyncio.set_event_loop(loop)
            with ThreadPoolExecutor(max_workers=ct) as executor:
                for query in self._queries:
                    fn = partial(
                        self.execute_sql, query, event_loop
                    )
                    res = await loop.run_in_executor(
                        executor, fn
                    )
                    result.append(res)
        except ComponentError:
            raise
        except Exception as err:
            raise ComponentError(
                f"{err}"
            ) from err
        finally:
            if _new is True:
                event_loop.close()
        # returning the previous data:
        if self.data is not None:
            self._result = self.data
        else:
            self._result = result
        return self._result
