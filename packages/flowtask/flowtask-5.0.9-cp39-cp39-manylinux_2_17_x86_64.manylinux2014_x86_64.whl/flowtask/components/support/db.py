from typing import Optional
import asyncio
from abc import ABC
from asyncdb import AsyncDB
from querysource.conf import asyncpg_url
from flowtask.conf import default_dsn


class DBSupport(ABC):
    """
    Interface for adding AsyncbDB-based Database Support to Components.
    """
    _loop: asyncio.AbstractEventLoop

    def get_connection(
        self,
        driver: str = 'pg',
        params: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        **kwargs
    ):
        # TODO: datasources and credentials
        if not kwargs and driver == 'pg':
            kwargs = {
                "server_settings": {
                    'application_name': 'Flowtask.DB',
                    'client_min_messages': 'notice',
                    'max_parallel_workers': '256',
                    'jit': 'on',
                    'statement_timeout': '3600000'
                }
            }
        if not event_loop:
            event_loop = self._loop
        return AsyncDB(
            driver,
            dsn=default_dsn,
            loop=event_loop,
            params=params,
            **kwargs
        )

    def db_connection(
        self,
        driver: str = 'pg',
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        if not credentials:
            credentials = {
                "dsn": default_dsn
            }
        else:
            credentials = {
                "params": credentials
            }
        kwargs = {}
        if driver == 'pg':
            kwargs = {
                "server_settings": {
                    'application_name': 'Flowtask.DB',
                    'client_min_messages': 'notice',
                    'max_parallel_workers': '512',
                    'jit': 'on',
                    'statement_timeout': '3600000'
                }
            }
        if not event_loop:
            event_loop = self._loop
        return AsyncDB(driver, loop=event_loop, **credentials, **kwargs)

    def pg_connection(
        self,
        dsn: Optional[str] = None,
        credentials: Optional[dict] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        if not credentials:
            if dsn is not None:
                credentials = {
                    "dsn": dsn
                }
            else:
                credentials = {
                    "dsn": asyncpg_url
                }
        else:
            credentials = {
                "params": credentials
            }
        kwargs: dict = {
            "min_size": 2,
            "server_settings": {
                'application_name': 'Flowtask.DB',
                'client_min_messages': 'notice',
                'max_parallel_workers': '256',
                'jit': 'on',
                'statement_timeout': '3600000'
            }
        }
        if not event_loop:
            event_loop = self._loop
        return AsyncDB(
            'pg',
            loop=event_loop,
            **credentials,
            **kwargs
        )
