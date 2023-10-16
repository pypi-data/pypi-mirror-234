import os
from abc import (
    ABC,
    abstractmethod
)
from collections.abc import Callable
from tqdm import tqdm
from navconfig import config
from navconfig.logging import logging
from flowtask.exceptions import ComponentError


class ClientInterface(ABC):
    _credentials: dict = {
        "username": str,
        "password": str
    }

    def __init__(self, credentials: dict, host: str = None, port: str = None, **kwargs) -> None:
        self.credentials: dict = credentials
        # host and port (if needed)
        self.host: str = host
        self.port: int = port
        self._environment = config
        self._connection: Callable = None
        # progress bar
        self._pb: Callable = None
        # any other argument
        self._clientargs = {}  # kwargs

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            # TODO: get from replacing masks or memecached
            return key

    def processing_credentials(self):
        for value, dtype in self._credentials.items():
            try:
                if type(self.credentials[value]) == dtype:
                    # can process the credentials, extracted from environment or variables:
                    default = getattr(self, value, self.credentials[value])
                    val = self.get_env_value(self.credentials[value], default=default)
                    self.credentials[value] = val
            except (TypeError, KeyError) as err:
                logging.error(
                    f'{__name__}: Wrong or missing Credentials'
                )
                raise ComponentError(
                    f'{__name__}: Wrong or missing Credentials'
                ) from err

    def define_host(self):
        try:
            self.host = self.credentials['host']
        except KeyError:
            self.host = self.host
        try:
            self.port = self.credentials['port']
        except KeyError:
            self.port = self.port
        # getting from environment:
        self.host = self.get_env_value(
            self.host,
            default=self.host
        )
        self.port = self.get_env_value(
            str(self.port),
            default=self.port
        )
        if self.host:
            logging.debug(f'<{__name__}>: HOST: {self.host}, PORT: {self.port}')

    @abstractmethod
    async def close(self, timeout: int = 5):
        """close.
            Closing the connection.
        """

    @abstractmethod
    async def open(self, host: str, port: int, credentials: dict, **kwargs):
        """open.
            Starts (open) a connection to external resource.
        """

    async def __aenter__(self) -> "ClientInterface":
        await self.open(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            **self._clientargs
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        return await self.close(
            timeout=1
        )

    def start_progress(self, total: int = 1):
        self._pb = tqdm(total=total)

    def close_progress(self):
        self._pb.close()
