"""
  DownloadFromSmartSheet
  Download an Excel file from SmartSheet.
"""
import asyncio
from collections.abc import Callable
from typing import Dict
import aiofiles
from flowtask.exceptions import ComponentError
from .DownloadFrom import DownloadFromBase

class DownloadFromSmartSheet(DownloadFromBase):
    """
    DownloadFromSmartSheet.

    Overview

            This component downloadFromSmartSheet,  a excel file from SmartSheet

        .. table:: Properties
        :widths: auto

    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | credentials  |   Yes    | Credentials to establish connection with smartsheet if it is null |
    |              |          | get the credentials of the environment                            |
    +--------------+----------+-----------+-------------------------------------------------------+
    | file_id      |   Yes    | Identificador del archivo en smartsheet                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | destination  |   Yes    | Format of how I will save the file                                |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days

    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.file_format: str = 'application/vnd.ms-excel'
        self.url: str = 'https://api.smartsheet.com/2.0/sheets/'
        self._credentials: Dict = {
            "token": str,
            "scheme": str
        }
        DownloadFromBase.__init__(
            self,
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self.create_destination: bool = True  # by default

    def start(self):
        if hasattr(self, 'api_key'):
            api_key = self.get_env_value(self.api_key)
            if not api_key:
                raise ComponentError(
                    f'SmartSheet: Invalid API Key name {self.api_key}'
                )
        else:
            api_key = self.get_env_value('SMARTSHEET_API_KEY')
        self.credentials = {
            "token": api_key,
            "scheme": "Bearer"
        }
        self.url = f'{self.url}{self.file_id}'
        if self.file_format not in ['application/vnd.ms-excel', 'text/csv']:
            # only supported
            raise ComponentError(
                f'SmartSheet: Format {self.file_format} is not suported'
            )
        try:
            self.accept = 'text/csv' if self.file_format == 'dataframe' else self.file_format
        except Exception as err:
            print(err)
        return super(DownloadFromSmartSheet, self).start()


    async def close(self):
        pass

    async def http_response(self, response):
        # getting aiohttp response:
        if response.status == 200:
            try:
                async with aiofiles.open(self.filename, mode='wb') as fp:
                    await fp.write(await response.read())
                return True
            except Exception as err:
                self.exception(f'Error saving File {err!s}')
        else:
            raise ComponentError(
                f'DownloadFromSmartSheet: Wrong response from Smartsheet: {response!s}'
            )
        return response

    async def run(self):
        self._result = None
        try:
            if await self.http_session(self.url, method = 'get'):
                self._filenames = [str(self.filename)]
                self._result = self._filenames
                self.add_metric('SMARTSHEET_FILE', self.filename)
            return self._result
        except ComponentError:
            raise
        except Exception as err:
            raise ComponentError(
                f'DownloadFromSmartSheet: Unknown Error: {err}'
            ) from err
