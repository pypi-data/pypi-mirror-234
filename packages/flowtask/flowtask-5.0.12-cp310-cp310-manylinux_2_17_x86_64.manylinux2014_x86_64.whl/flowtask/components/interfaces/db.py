import os
import asyncio
from abc import (
    ABC
)
from collections.abc import Callable
from navconfig import config
from navconfig.logging import logging
from querysource.conf import (
    # postgres main database:
    # postgres read-only
    PG_DRIVER,
    PG_HOST,
    PG_USER,
    PG_PWD,
    PG_DATABASE,
    PG_PORT,
    # rethinkdb
    rt_driver,
    rt_host,
    rt_port,
    rt_user,
    rt_password,
    rt_database,
    # SQL Server
    MSSQL_DRIVER,
    MSSQL_HOST,
    MSSQL_PORT,
    MSSQL_USER,
    MSSQL_PWD,
    MSSQL_DATABASE,
    # MySQL Server
    MYSQL_DRIVER,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PWD,
    MYSQL_DATABASE,
    # influxdb
    INFLUX_DRIVER,
    INFLUX_HOST,
    INFLUX_PORT,
    INFLUX_ORG,
    INFLUX_TOKEN,
    # INFLUX_USER,
    # INFLUX_PWD,
    INFLUX_DATABASE,
    # cassandra
    CASSANDRA_DRIVER,
    CASSANDRA_HOST,
    CASSANDRA_PORT,
    CASSANDRA_USER,
    CASSANDRA_PWD,
    CASSANDRA_DATABASE
)
from asyncdb import AsyncDB
from asyncdb.drivers.abstract import BaseDriver
from asyncdb.exceptions import ProviderError
from navigator.conf import default_dsn
from flowtask.exceptions import ComponentError


class DBInterface(ABC):
    """DBInterface.

    Abstract Interface for Database-based connectors.
    """
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str
    }

    def __init__(self, driver: str, credentials: dict, **kwargs) -> None:
        self.driver: str = driver
        self.credentials: dict = credentials
        self.datasource: str = None
        self._environment = config
        self._connection: Callable = None

    def get_env_value(self, key: str, default: str = None):
        """get_env_value

        Variable replacement from environment values.

        Args:
            key (str): variable name
            default (str, optional): Optional default if variable does not exist.

        Returns:
            Any: Any value.
        """
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            if hasattr(self, 'masks'):
                if key in self._masks.keys():
                    return self._masks[key]
            return key

    def process_credentials(self):
        for value, dtype in self._credentials.items():
            try:
                if isinstance(self.credentials[value], dtype):
                    # can process the credentials, extracted from environment or variables:
                    default = getattr(self, value, self.credentials[value])
                    if dtype is not int:
                        val = self.get_env_value(self.credentials[value], default=default)
                    else:
                        val = default
                    self.credentials[value] = val
            except KeyError:
                pass
            except (TypeError, ValueError) as err:
                logging.error(
                    f'{__name__}: Wrong or missing Credentials'
                )
                raise ComponentError(
                    f'{__name__}: Wrong or missing Credentials'
                ) from err

    async def connection(
        self,
        driver: str = 'pg',
        credentials: dict = None,
        event_loop: asyncio.AbstractEventLoop = None,
        **kwargs
    ) -> BaseDriver:
        if not event_loop:
            event_loop = asyncio.get_event_loop()
        if driver == 'pg':  # default driver:
            args = {
                "server_settings": {
                    'client_min_messages': 'notice',
                    'max_parallel_workers': '24',
                    'statement_timeout': '36000000'
                }
            }
        else:
            args = kwargs
        try:
            self._connection = AsyncDB(driver, params=credentials, loop=event_loop, **args)
        except ProviderError as e:
            raise ComponentError(
                f"DbClient: Error creating connection: {e}"
            ) from e
        except Exception as e:
            raise ComponentError(
                f"DbClient: unknown DB error: {e}"
            ) from e
        if self._connection:
            return self._connection
        else:
            raise ComponentError(
                f"DbClient: Unable to connect to {driver}"
            )

    def pg_connection(self, event_loop: asyncio.AbstractEventLoop = None) -> BaseDriver:
        pgargs: dict = {
            "server_settings": {
                "application_name": 'Flowtask',
                "client_min_messages": "notice",
                "max_parallel_workers": "48",
                "jit": "off",
                "statement_timeout": "3600000",
                "effective_cache_size": "2147483647"
            },
        }
        if not event_loop:
            try:
                event_loop = asyncio.get_running_loop()
            except RuntimeError:
                event_loop = asyncio.get_event_loop()
        return AsyncDB(
            'pg', dsn=default_dsn, loop=event_loop, **pgargs
        )

    async def get_driver(self, driver: str, conn: BaseDriver) -> BaseDriver:
        # TODO: migration to Model
        result = None
        query = "SELECT driver, params, credentials FROM troc.datasources where name = '{}'"
        try:
            result, error = await conn.queryrow(query.format(driver))
            if error:
                raise ComponentError(
                    f'DbClient: Error on Getting Datasource: {error!s}'
                )
            if result:
                try:
                    self.driver = result['driver']
                except KeyError as ex:
                    raise RuntimeError(
                        f"DbClient Error: there is no *Driver* column on datasource {driver}"
                    ) from ex
                try:
                    params = result['params']
                    logging.debug(f'DB: connection params: {params}')
                    self.credentials = {**dict(params), **dict(result['credentials'])}
                except (TypeError, ValueError, KeyError) as ex:
                    raise RuntimeError(
                        f"DbClient Error: wrong or missing credentials on Datasource {driver}"
                    ) from ex
        except Exception as e:
            logging.exception(f'DB Error: {e}', stack_info=True)
            raise
        if not result:
            # getting the default for any kind of database connection:
            # based on provider (rethink, mssql, etc) get default connection
            if driver == 'sqlserver':
                self.driver = MSSQL_DRIVER
                self.credentials = {
                    "host": MSSQL_HOST,
                    "port": MSSQL_PORT,
                    "database": MSSQL_DATABASE,
                    "user": MSSQL_USER,
                    "password": MSSQL_PWD
                }
            elif driver == 'cassandra':
                self.driver = CASSANDRA_DRIVER
                self.credentials = {
                    "host": CASSANDRA_HOST,
                    "port": CASSANDRA_PORT,
                    "database": CASSANDRA_DATABASE,
                    "user": CASSANDRA_USER,
                    "password": CASSANDRA_PWD
                }
            elif driver in ('influx', 'influxdb'):
                self.driver = INFLUX_DRIVER
                self.credentials = {
                    "host": INFLUX_HOST,
                    "port": INFLUX_PORT,
                    "database": INFLUX_DATABASE,
                    "org": INFLUX_ORG,
                    "token": INFLUX_TOKEN
                }
            elif driver in ('rethink', 'rethinkdb'):
                self.driver = rt_driver
                self.credentials = {
                    "host": rt_host,
                    "port": rt_port,
                    "database": rt_database,
                    "user": rt_user,
                    "password": rt_password
                }
            elif driver in ('postgres', 'postgresql'):
                self.driver = PG_DRIVER
                self.credentials = {
                    "host": PG_HOST,
                    "port": PG_PORT,
                    "database": PG_DATABASE,
                    "user": PG_USER,
                    "password": PG_PWD
                }
            elif driver == 'mysql':
                self.driver = MYSQL_DRIVER
                self.credentials = {
                    "host": MYSQL_HOST,
                    "port": MYSQL_PORT,
                    "database": MYSQL_DATABASE,
                    "user": MYSQL_USER,
                    "password": MYSQL_PWD
                }
            else:
                raise ComponentError(
                    f'Unknown Database Driver {driver}'
                )

    async def get_credentials(self) -> BaseDriver:
        if self.credentials:
            return True  # credentials are passed to Component
        if self.datasource is not None:
            driver = self.datasource
        else:
            driver = 'pg'
        if driver in ('db', 'pg'):
            # default credentials
            self.driver = PG_DRIVER
            self.credentials = {
                "user": PG_USER,
                "password": PG_PWD,
                "host": PG_HOST,
                "port": PG_PORT,
                "database": PG_DATABASE
            }
            return True
        else:
            # getting from "datasources" table:
            db = self.pg_connection()
            try:
                async with await db.connection() as conn:
                    await self.get_driver(driver, conn)
                    if not self.credentials:
                        raise RuntimeError(
                            f"DB Error: wrong or missing credentials: {driver}"
                        )
            except Exception as e:
                logging.exception(f"DB Error: {e}")
                raise

    async def start(self, **kwargs):
        # first: getting credential from datasource or creds dictionary.
        # second: processing credentials (extracting value replacements from environment)
        await self.get_credentials()
        self.process_credentials()
        await super(DBInterface, self).start(**kwargs)
