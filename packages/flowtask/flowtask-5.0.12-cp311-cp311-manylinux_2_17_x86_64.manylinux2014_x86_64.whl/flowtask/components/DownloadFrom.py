import asyncio
import random
import ssl
from abc import abstractmethod
from functools import partial
from typing import Dict, List
from collections.abc import Callable
from pathlib import Path, PosixPath
from tqdm import tqdm
import aiohttp
from flowtask.exceptions import ComponentError, FileNotFound
from flowtask.utils.encoders import DefaultEncoder


from .abstract import DtComponent

ua = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (X11; Windows NT 10.0; rv:19.0) Gecko/20100101 Firefox/19.0 Iceweasel/19.0.2",
    "Mozilla/5.0 (X11; U; Linux i686; sk; rv:1.9.0.4) Gecko/2008111217 Fedora/3.0.4-1.fc10 Firefox/3.0.4"
]

class DownloadFromBase(DtComponent):

    """
    DownloadFrom.

    Overview

            Download a file from its source

    .. table:: Properties
       :widths: auto

    +---------------+----------+-----------+-------------------------------------------------------+
    | Name          | Required | Summary                                                           |
    +---------------+----------+-----------+-------------------------------------------------------+
    | file          |   Yes    | Access the file download through a url, with the required user    |
    |               |          | credentials and password                                          |
    +---------------+----------+-----------+-------------------------------------------------------+
    | download      |   Yes    | File destination and directory                                    |
    +---------------+----------+-----------+-------------------------------------------------------+
    | source        |   Yes    | Origin of the file to download and location where the file is     |
    |               |          | located                                                           |
    +---------------+----------+-----------+-------------------------------------------------------+
    | destination   |   Yes    | Destination where I will save the file                            |
    +---------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days
    """
    url: str = None
    _credentials: dict = {
        "username": str,
        "password": str
    }
    headers: dict = {}
    timeout: int = 60
    no_host: bool = False

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.accept: str = 'text/plain'
        self.overwrite: bool = True
        try:
            self.create_destination = kwargs['create_destination']
            del kwargs['create_destination']
        except KeyError:
            self.create_destination: bool = False
        self.rename: str = None
        self.credentials: Dict = {}
        # source:
        self.source_file: str = None
        self.source_dir: str = None
        # destination:
        self.filename: str = None
        self._srcfiles: List = []
        self._filenames: Dict = {}
        self._connection: Callable = None
        self.ssl: bool = False
        self.ssl_cafile: str = None
        self.ssl_certs: list = []
        # host and port (if needed)
        self.host: str = 'localhost'
        self.port: int = 22
        super(DownloadFromBase, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self._encoder = DefaultEncoder()
        self.response_status: List = (200, 201, 202)
        # SSL Context:
        if self.ssl:
            # TODO: add CAFile and cert-chain
            self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=self.ssl_cafile)
            self.ssl_ctx.options &= ~ssl.OP_NO_SSLv3
            self.ssl_ctx.verify_mode = ssl.CERT_NONE
            if self.ssl_certs:
                self.ssl_ctx.load_cert_chain(*self.ssl_certs)
        else:
            self.ssl_ctx = None

    def processing_credentials(self):
        for value, dtype in self._credentials.items():
            try:
                if type(self.credentials[value]) == dtype:
                    # can process the credentials, extracted from environment or variables:
                    default = getattr(self, value, self.credentials[value])
                    val = self.get_env_value(self.credentials[value], default=default)
                    self.credentials[value] = val
            except (TypeError, KeyError) as ex:
                self._logger.error(
                    f'{__name__}: Wrong or missing Credentias'
                )
                raise ComponentError(
                    f'{__name__}: Wrong or missing Credentias'
                ) from ex

    def define_host(self):
        if self.no_host is False:
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
                self._logger.debug(f'<{__name__}>: HOST: {self.host}, PORT: {self.port}')

    def build_headers(self):
        self.headers = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **self.headers
        }

    def start(self):
        """Start.

        Processing variables and credentials.
        """
        try:
            self.define_host()
            self.processing_credentials()
        except Exception as err:
            self._logger.error(err)
            raise
        if hasattr(self, 'directory'):
            self.directory = Path(self.directory)
            try:
                if hasattr(self, 'masks'):
                    p = self.mask_replacement(
                        self.directory
                    )
                else:
                    p = self.directory
                if not p.exists():
                    if self.create_destination is True:
                        try:
                            PosixPath(p).mkdir(parents=True, exist_ok=True)
                        except (Exception, OSError) as err:
                            raise ComponentError(
                                f'Error creating directory {self.directory}: {err}'
                            ) from err
                    else:
                        self._logger.error(
                            f'DownloadFrom: Path doesn\'t exists: {p}'
                        )
                        raise FileNotFound(
                            f'DownloadFrom: Path doesn\'t exists: {p}'
                        )
            except Exception as err:
                self._logger.error(err)
                raise ComponentError(f"{err!s}") from err
            self._logger.debug(f'Destination Directory: {self.directory}')
        if hasattr(self, 'file'):
            if isinstance(self.file, list):
                # is a list of files:
                for file in self.file:
                    filename = file
                    if hasattr(self, 'masks'):
                        filename = self.mask_replacement(file)
                    self._logger.debug(f"Filename > {filename}")
                    self._srcfiles.append(filename)
            else:
                try:
                    filename = self.process_pattern('file')
                    if hasattr(self, 'masks'):
                        if isinstance(filename, dict):
                            for key, value in filename.items():
                                filename[key] = self.mask_replacement(value)
                        else:
                            filename = self.mask_replacement(filename)
                    # path for file
                    self._logger.debug(f"Filename > {filename}")
                    self.filename = filename
                    self._srcfiles.append(filename)
                    # for some exception, directory is on file:
                    if 'directory' in self.file:
                        self.source_dir = self.file['directory']
                        if hasattr(self, 'masks'):
                            self.source_dir = self.mask_replacement(self.source_dir)
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
        if hasattr(self, 'source'):  # using the destination filosophy
            try:
                if hasattr(self, 'masks'):
                    self.source_dir = self.mask_replacement(
                        self.source['directory']
                    )
                else:
                    self.source_dir = self.source['directory']
            except KeyError:
                self.source_dir = '/'
            print('Source Dir: ', self.source_dir)
            # filename:
            if 'file' in self.source:
                self.source_file = self.process_pattern('file', parent=self.source)
                self._srcfiles.append(self.source_file)
            else:
                try:
                    if isinstance(self.source['filename'], list):
                        for file in self.source['filename']:
                            filename = self.mask_replacement(
                                file
                            )
                            self._srcfiles.append(filename)
                    else:
                        self.source_file = self.mask_replacement(
                            self.source['filename']
                        )
                        self._srcfiles.append(self.source_file)
                except KeyError:
                    self.source_file = None
        if hasattr(self, 'destination'):
            self.directory = Path(self.destination['directory'])
            # Create directory if not exists
            try:
                if self.create_destination is True:
                    self.directory.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                raise ComponentError(
                    f'DownloadFrom: Error creating directory {self.directory}: {err}'
                ) from err
            except Exception as err:
                self._logger.error(
                    f'Error creating directory {self.directory}: {err}'
                )
                raise ComponentError(
                    f'Error creating directory {self.directory}: {err}'
                ) from err
            try:
                if 'filename' in self.destination:
                    self.filename = self.directory.joinpath(self.destination['filename'])
                else:
                    self.filename = self.directory.joinpath(self.filename['filename'])
                self._logger.debug(f'Raw Destination Filename: {self.filename}\n')
                if hasattr(self, 'masks'):
                    self.filename = self.mask_replacement(self.filename)
            except Exception:
                pass
        if self.url:
            self.build_headers()
        return True

    async def http_response(self, response):
        return response

    async def http_session(
        self,
        url: str = None,
        method: str = 'get',
        data: dict = None,
        data_format: str = 'json'
    ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        if url is not None:
            self.url = url
        # TODO: Auth, Data, etc
        auth = {}
        params = {}
        _data = {
            "data": None
        }
        if self.credentials:
            if 'username' in self.credentials:  # basic Authentication
                auth = aiohttp.BasicAuth(
                    self.credentials['username'],
                    self.credentials['password']
                )
                params = {
                    "auth": auth
                }
            elif 'token' in self.credentials:
                self.headers['Authorization'] = "{scheme} {token}".format(
                    scheme=self.credentials['scheme'],
                    token=self.credentials['token']
                )
        if data_format == 'json':
            params["json_serialize"] = self._encoder.dumps
            _data['json'] = data
        else:
            _data['data'] = data
        async with aiohttp.ClientSession(**params) as session:
            meth = getattr(session, method)
            if self.ssl:
                ssl = {
                    "ssl": self.ssl_ctx,
                    "verify_ssl": True
                }
            else:
                ssl = {}
            fn = partial(
                meth,
                self.url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True,
                **ssl,
                **_data
            )
            try:
                async with fn() as response:
                    if response.status in self.response_status:
                        return await self.http_response(response)
                    else:
                        print('ERROR RESPONSE >> ', response)
                        raise ComponentError(
                            f'DownloadFrom: Error getting data from URL {response}'
                        )
            except Exception as err:
                raise ComponentError(
                    f'DownloadFrom: Error Making an SSL Connection to ({self.url}): {err}'
                ) from err
            except aiohttp.exceptions.HTTPError as err:
                raise ComponentError(
                    f'DownloadFrom: SSL Certificate Error: {err}'
                ) from err

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    def start_pbar(self, total: int = 1):
        return tqdm(total=total)
