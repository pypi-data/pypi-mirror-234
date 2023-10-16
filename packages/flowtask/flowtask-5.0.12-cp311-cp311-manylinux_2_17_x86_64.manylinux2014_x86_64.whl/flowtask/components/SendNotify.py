"""
SendNotify.

Send notifications via Notify Component.
"""
import os
import asyncio
from typing import (
    Dict,
    List
)
from collections.abc import Callable, Iterable
from pathlib import Path
from navconfig.logging import logging
from notify import Notify
from notify.models import (
    Actor
)
from flowtask.exceptions import (
    ComponentError,
    FileNotFound
)

from .abstract import DtComponent


def expand_path(filename: str) -> Iterable[Path]:
    p = Path(filename)
    return Path(p.parent).expanduser().glob(p.name)

class SendNotify(DtComponent):
    """
    SendNotify.

    Overview

        Send notifications via Notify Component

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    | via          |   Yes    | Notification is received via email                     |
    +--------------+----------+-----------+--------------------------------------------+
    | acount       |   Yes    | Enter the access credentials the server: {"hostname"}{"port"}     |
    |              |          | {“password”}{“username”}                               |
    +--------------+----------+-----------+--------------------------------------------+
    | recipients   |   Yes    | I get the data of the target user                      |
    +--------------+----------+-----------+--------------------------------------------+

    Return the list of arbitrary days
    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self.attachments: List = []
        self.list_attachment: List = []
        self.notify: Callable = None
        self.recipients: List = []
        self._recipients: List = []
        self.via: str = 'email'
        self.message: Dict = {}
        super(SendNotify, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key

    def processing_credentials(self, credentials: Dict):
        for key, value in credentials.items():
            print(key, value)
            try:
                val = self.get_env_value(str(value), default=value)
                credentials[key] = val
            except (TypeError, KeyError, ValueError) as err:
                raise ComponentError(
                    f'{__name__}: Wrong processing Credentials'
                ) from err
        return credentials

    def status_sent(self, recipient, message, result, *args, **kwargs):
        print(f'Notification with status {result!s} to {recipient.account!s}')
        # logger:
        logging.info(
            f'Notification with status {result!s} to {recipient.account!s}')
        status = {
            "recipient": recipient,
            "result": result
        }
        self.add_metric('Sent', status)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        # TODO: generate file from dataset (dataframe)
        # using mailing list:
        if hasattr(self, 'list'):
            # getting the mailing list:
            lst = self.list
            sql = f"SELECT * FROM troc.get_mailing_list('{lst!s}')"
            try:
                connection = self.get_connection()
                async with await connection.connection() as conn:
                    result, error = await conn.query(sql)
                    if error:
                        raise ComponentError(
                            f'CreateReport: Error on Recipients: {error!s}.'
                        )
                    for r in result:
                        actor = Actor(**dict(r))
                        self._recipients.append(actor)
            except Exception as err:
                logging.exception(err)
        else:
            # determine the recipients:
            try:
                self._recipients = [
                    Actor(**user) for user in self.recipients
                ]
            except Exception as err:
                raise ComponentError(
                    f'Error formatting Recipients: {err}'
                ) from err
        if not self._recipients:
            raise ComponentError(
                'SendNotify: Invalid Number of Recipients.'
            )
        print(self._recipients)
        if hasattr(self, 'masks'):
            for i, attach in enumerate(self.attachments):
                attachment = self.mask_replacement(
                    attach
                )
                # resolve filenames:
                files = expand_path(attachment)
                for file in files:
                    self.list_attachment.append(file)

            # Mask transform of message
            for key, value in self.message.items():
                self.message[key] = self.mask_replacement(
                    value
                )
        # Verify if file exists
        for file in self.list_attachment:
            if not file.exists():
                raise FileNotFound(
                    f"File doesn't exists: {file}"
                )

    async def close(self):
        if self.notify:
            try:
                await self.notify.close()
            except Exception as err:
                print(err)

    async def run(self):
        """
        Running the Notification over all recipients.
        """
        self._result = self.data  # by-pass override data (pass-through)
        # create the notify component
        account = {}
        if hasattr(self, 'account'):
            account = {**self.account}
        else:
            # getting default account from Notify
            pass
        account = self.processing_credentials(account)
        try:
            self.notify = Notify(
                self.via,
                loop=self._loop,
                **account
            )
            self.notify.sent = self.status_sent
        except Exception as err:
            raise ComponentError(
                f'Error Creating Notification App: {err}'
            ) from err
        try:
            result = await self.notify.send(
                recipient=self._recipients,
                attachments=self.list_attachment,
                **self.message
            )
            logging.debug(f'Notification Status: {result}')
            # add metric:
            self.add_metric('Notification', self.message)
        except Exception as err:
            raise ComponentError(
                f"SendNotify Error: {err}"
            ) from err
        return self._result
