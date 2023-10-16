"""
Office365 Client.

Authentication/Authorization for Office 365.
"""
from abc import abstractmethod
from typing import (
    Any
)
from collections.abc import Callable
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.auth.client_credential import ClientCredential
from navconfig.logging import logging
from navconfig import config
from flowtask.exceptions import ComponentError

class O365Client:
    url: str = None
    no_host: bool = True

    _credentials: dict = {
        "username": str,
        "password": str,
        "client_id": str,
        "client_secret": str,
        "tenant": str,
        "site": str
    }

    def __init__(
        self,
        credentials: dict,
        *args,
        **kwargs
    ) -> None:
        self.tenant: str = None
        self.site: str = None
        self.auth_context: Any = None
        self.context: Any = None
        self.credentials: dict = credentials
        self._environment: Callable = config

    def get_env_value(self, key, default: str = None):
        if val := self._environment.get(key, default):
            return val
        else:
            return key

    @abstractmethod
    def get_context(self, url: str, *args):
        pass

    def processing_credentials(self):
        for value, dtype in self._credentials.items():
            try:
                if value in self.credentials:
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
        ## getting Tenant and Site from credentials:
        try:
            self.tenant = self.credentials['tenant']
            self.site = self.credentials['site'] if 'site' in self.credentials else None
        except KeyError as e:
            raise RuntimeError(
                f"Office365: Missing Tenant or Site Configuration: {e}."
            ) from e

    async def connection(self):
        if hasattr(self, 'credentials'):
            username = None
            password = None
            client_id = None
            client_secret = None
            try:
                username = self.credentials['username']
            except KeyError:
                client_id = self.credentials['client_id']
            try:
                password = self.credentials['password']
            except KeyError:
                client_secret = self.credentials['client_secret']
        else:
            logging.error('Office365: Wrong Credentials or missing Credentias')
            raise RuntimeError(
                'Office365: Wrong Credentials or missing Credentias'
            )
        try:
            self.auth_context = AuthenticationContext(self.url)
            if username is not None:
                if self.auth_context.acquire_token_for_user(username, password):
                    self.context = self.get_context(self.url, self.auth_context)
                logging.debug("Office365: Authentication success")
            else:
                # using Client ID and Secret:
                self.auth_context = ClientCredential(
                    client_id, client_secret
                )
                self.context = self.get_context(self.url).with_credentials(self.auth_context)
        except Exception as err:
            logging.error(
                f'Office365: Authentication Error: {err}'
            )
            raise RuntimeError(
                f'Office365: Authentication Error: {err}'
            ) from err
