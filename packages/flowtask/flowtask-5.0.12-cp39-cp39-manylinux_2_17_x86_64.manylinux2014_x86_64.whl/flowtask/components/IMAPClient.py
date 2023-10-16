"""
IMAP/POP Client.

Class for operations with IMAP Mailboxes.

"""
import socket
import asyncio
import ssl
from collections.abc import Callable
import imaplib
from flowtask.exceptions import (
    ComponentError
)
from .interfaces import ClientInterface
from .azureauth import AzureAuth


class IMAPClient(ClientInterface):
    """
    IMAPClient.

   Overview

        Component for IMAP connections

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    |   _init_     |   Yes    | This attribute is to initialize the component methods  |
    +--------------+----------+-----------+--------------------------------------------+
    |   close      |   Yes    | This attribute allows me to close the process          |
    +--------------+----------+-----------+--------------------------------------------+
    |   start      |   Yes    | We start by validating if the file exists, then the    |
    |              |          | function to get the data is started                    |
    +--------------+----------+-----------+--------------------------------------------+
    |   run        |   Yes    | This method allows to run function and change its state|
    +--------------+----------+-----------+--------------------------------------------+
    |  async_run   |   Yes    | This method allows to execute function asynchronously  |
    +--------------+----------+-----------+--------------------------------------------+

    """
    _credentials: dict = {
        "user": str,
        "password": str
    }
    authmech: str = 'XOAUTH2'
    use_ssl = True

    def __init__(
        self,
        credentials: str,
        host: str = None,
        port: str = None,
        **kwargs
    ) -> None:
        self._connected: bool = False
        self._client: Callable = None
        try:
            self.use_ssl: bool = kwargs['use_ssl']
            del kwargs['use_ssl']
        except KeyError:
            self.use_ssl: bool = True
        if 'use_ssl' in credentials:
            self.use_ssl = credentials['use_ssl']
            del credentials['use_ssl']
        try:
            self.mailbox: str = kwargs['mailbox']
            del kwargs['mailbox']
        except KeyError:
            self.mailbox: str = 'Inbox'
        self._sslcontext = ssl.create_default_context()
        self._client: Callable = None
        # timeout:
        try:
            self._timeout = kwargs['timeout']
            del kwargs['timeout']
        except KeyError:
            self._timeout = 20
        try:
            self.overwrite = kwargs['overwrite']
            del kwargs['overwrite']
        except KeyError:
            self.overwrite = False
        super(IMAPClient, self).__init__(
            credentials,
            host,
            port,
            **kwargs
        )

    async def open(self, host: str, port: int, credentials: dict, **kwargs):
        try:
            if self.use_ssl:
                self._client = imaplib.IMAP4_SSL(
                    host,
                    port,
                    timeout=10,
                    ssl_context=self._sslcontext
                )
            else:
                self._client = imaplib.IMAP4(
                    host,
                    port,
                    timeout=10
                )
        except socket.error as e:
            raise ComponentError(
                f'Socket Error: {e}'
            ) from e
        except ValueError as ex:
            print('IMAP err', ex)
            raise RuntimeError(
                f'IMAP Invalid parameters or credentials: {ex}'
            ) from ex
        except Exception as ex:
            print('IMAP err', ex)
            self._logger.error(
                f'Error connecting to server: {ex}'
            )
            raise ComponentError(
                f'Error connecting to server: {ex}'
            ) from ex
        # start the connection
        try:
            # disable debug:
            self._client.debug = 0
        except Exception:
            pass
        try:
            await asyncio.sleep(0.5)
            self._client.timeout = 20
            if self.authmech is not None:
                ### we need to build an Auth token:
                azure = AzureAuth()  # default values
                result, msg = self._client.authenticate(
                    self.authmech,
                    lambda x: azure.binary_token(
                        credentials['user'], credentials['password']
                    )
                )
                print('RESULT ', result, msg)
                if result == 'OK':
                    self._connected = True
                    return self._connected
                else:
                    raise ComponentError(
                        f'IMAP: Wrong response from Server {msg}'
                    )
            else:
                # using default authentication
                r = self._client.login(credentials['user'], credentials['password'])
                if r.result != 'NO':
                    self._connected = True
                    return self._connected
                else:
                    raise ComponentError(
                        f'IMAP: Wrong response from Server {r.result}'
                    )
        except AttributeError as err:
            raise ComponentError(
                f'Login Forbidden, wrong username or password: {err}'
            ) from err
        except Exception as err:
            raise ComponentError(
                f'Error connecting to server: {err}'
            ) from err

    async def close(self, timeout: int = 5):
        try:
            if self._client:
                self._client.close()
                self._client.logout()
                self._connected = False
        except imaplib.IMAP4.abort as err:
            self._logger.warning(err)
