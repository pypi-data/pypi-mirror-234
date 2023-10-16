from collections.abc import Callable, Iterable
import asyncio
from pathlib import Path
from notify.models import (
    Actor
)
from notify import Notify
from flowtask.exceptions import FileNotFound, ActionError
from .interfaces import ClientInterface
from .abstract import AbstractEvent

def expand_path(filename: str) -> Iterable[Path]:
    p = Path(filename)
    return Path(p.parent).expanduser().glob(p.name)

class SendFile(ClientInterface, AbstractEvent):

    def __init__(self, *args, **kwargs):
        self.list_attachment: list = []
        self.notify: Callable = None
        super(SendFile, self).__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        # status = kwargs.pop('status', 'event')
        # task = kwargs.pop('task', None)
        # cPrint(
        #     f' == TASK {task} EXECUTED {status} WITH: {self._kwargs}, {args}, {kwargs} === ',
        #     level="INFO"
        # )
        # determine the recipients:
        # TODO: add support for mailing lists
        try:
            self._recipients = [
                Actor(**user) for user in self.recipients
            ]
        except Exception as err:
            raise RuntimeError(
                f'Error formatting Recipients: {err}'
            ) from err
        if not self._recipients:
            raise RuntimeError(
                'SendNotify: Invalid Number of Recipients.'
            )

        # File Attachment:
        # TODO: multiple attachments
        if hasattr(self, 'directory'):
            d = self.mask_replacement(self.directory)  # pylint: disable=access-member-before-definition
            p = Path(d)  # pylint: disable=E0203
            if p.exists() and p.is_dir():
                self.directory = p
            else:
                self._logger.error(
                    f'Path doesn\'t exists: {self.directory}'
                )
        else:
            self.directory = None

        if hasattr(self, 'filename'):
            file = self.mask_replacement(self.filename)
            if self.directory:
                file = self.directory.joinpath(file)
            else:
                file = expand_path(file)
            if file.exists():
                self.list_attachment.append(file)
            else:
                raise FileNotFound(
                    f"File doesn't exists: {file}"
                )

        # print('ATTACHMENTS > ', self.list_attachment)

        # Mask transform of message
        for key, value in self.message.items():
            self.message[key] = self.mask_replacement(
                value
            )

        try:
            await self.open()
            async with self.notify as mail:
                try:
                    result = await mail.send(
                        recipient=self._recipients,
                        attachments=self.list_attachment,
                        **self.message
                    )
                    self._logger.debug(f'Notification Status: {result}')
                except Exception as err:
                    raise ActionError(
                        f"SendNotify Error: {err}"
                    ) from err
                return None
        finally:
            await self.close()

    # def status_sent(self, recipient, message, result, *args, **kwargs):
    #     print(f'Notification with status {result!s} to {recipient.account!s}')
    #     # logger:
    #     self._logger.info(
    #         f'Notification with status {result!s} to {recipient.account!s}')
    #     status = {
    #         "recipient": recipient,
    #         "result": result
    #     }
    #     return status

    async def close(self):
        """close.
            Closing the connection.
        """
        if self.notify:
            try:
                await self.notify.close()
            except Exception as err:
                print(err)

    async def open(self):
        """open.
            Starts (open) a connection to an external resource.
        """
        try:
            self.notify = Notify(
                'email',
                loop=asyncio.get_event_loop(),
                **self.credentials
            )
            # self.notify.sent = self.status_sent
        except Exception as err:
            raise ActionError(
                f'Error Creating Notification App: {err}'
            ) from err
        return self
