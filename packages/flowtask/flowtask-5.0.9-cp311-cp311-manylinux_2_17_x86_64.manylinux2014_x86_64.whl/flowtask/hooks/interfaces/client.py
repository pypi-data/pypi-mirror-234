from abc import (
    abstractmethod
)
from collections.abc import Callable
from tqdm import tqdm
from navconfig.logging import logging
from flowtask.exceptions import ComponentError
from .env import EnvSupport

class ClientInterface(EnvSupport):
    _credentials: dict = {
        "username": str,
        "password": str
    }

    def __init__(self, credentials: dict, **kwargs) -> None:
        super(ClientInterface, self).__init__(**kwargs)
        self.credentials = self.set_credentials(credentials)
        # host and port (if needed)
        self.host: str = kwargs.pop('host', None)
        self.port: int = kwargs.pop('port', None)
        self._connection: Callable = None
        # progress bar
        self._pb: Callable = None
        # any other argument
        self._clientargs = {}  # kwargs

    def set_credentials(self, credentials: dict):
        for key, default in credentials.items():
            try:
                if hasattr(self, 'credentials'):
                    # there are credentials in the component
                    default = getattr(self, key, self.credentials[key])
                # can process the credentials, extracted from environment or variables:
                val = self.get_env_value(credentials[key], default=default)
                credentials[key] = val
            except (TypeError, KeyError) as ex:
                self._logger.error(
                    f'{__name__}: Wrong or missing Credentias'
                )
                raise ComponentError(
                    f'{__name__}: Wrong or missing Credentias'
                ) from ex
        return credentials

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
            logging.debug(
                f'<{__name__}>: HOST: {self.host}, PORT: {self.port}'
            )

    @abstractmethod
    async def close(self, timeout: int = 5):
        """close.
            Closing the connection.
        """

    @abstractmethod
    async def open(self, credentials: dict, **kwargs):
        """open.
            Starts (open) a connection to external resource.
        """

    async def __aenter__(self) -> "ClientInterface":
        await self.open(
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
