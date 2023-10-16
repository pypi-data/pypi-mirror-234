from typing import (
    List,
    Dict
)
from abc import abstractmethod
from collections.abc import Callable
import asyncio
import logging
import random
import ssl
from pathlib import Path, PosixPath
from functools import partial
import aiohttp
from aiohttp import web
from tqdm import tqdm
from flowtask.exceptions import ComponentError, FileNotFound
from flowtask.utils.encoders import DefaultEncoder, json_encoder

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

class UploadToBase(DtComponent):
    url: str = None
    _credentials: Dict = {
        "username": str,
        "password": str
    }
    create_destination: bool = False
    headers: Dict = {}
    timeout: int = 60

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.accept: str = 'text/plain'
        self.overwrite: bool = True
        self.rename: bool = True
        self.credentials: Dict = {}
        # source:
        self.source_file: str = None
        self.source_dir: str = None
        # destination:
        self.filename: str = None
        self._filenames: List = []
        self._connection: Callable = None
        self.ssl: bool = False
        self.ssl_cafile: str = None
        self.ssl_certs: list = []
        # host and port (if needed)
        self.host: str = 'localhost'
        self.port: int = 22
        super(UploadToBase, self).__init__(
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
                    f'{__name__}: Wrong Credentials or missing Credentias'
                )
                raise ComponentError(
                    f'{__name__}: Wrong Credentials or missing Credentias'
                ) from ex

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
            if hasattr(self, 'masks'):
                p = self.mask_replacement(
                    self.directory  # pylint: disable=E0203
                )
            else:
                p = Path(self.directory)  # pylint: disable=E0203
            if p.exists() and p.is_dir():
                self._logger.debug(f'Source Directory: {p}')
                self.directory = p
            else:
                if self.create_destination is True:
                    try:
                        PosixPath(self.directory).mkdir(parents=True, exist_ok=True)
                    except (Exception, OSError) as err:
                        raise ComponentError(
                            f'Error creating directory {self.directory}: {err}'
                        ) from err
                else:
                    self._logger.error(
                        f'UploadTo: Source Path doesn\'t exists: {self.directory}'
                    )
                    raise FileNotFound(
                        f'UploadTo: Source Path doesn\'t exists: {self.directory}'
                    )
        if hasattr(self, 'file'):
            filename = self.process_pattern('file')
            print('FILE: ', filename)
            if hasattr(self, 'masks'):
                filename = self.mask_replacement(filename)
            # path for file
            # get path of all files:
            self._logger.debug("Filename > {}".format(filename))
            self._filenames.append(filename)
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
            self.source_dir = Path(self.source_dir)
            # filename:
            if 'file' in self.source:
                self.source_file = self.process_pattern('file', parent=self.source)
            else:
                try:
                    self.source_file = self.mask_replacement(
                        self.source['filename']
                    )
                except KeyError:
                    self.source_file = None
        if hasattr(self, 'destination'):
            self.directory = self.destination['directory']
            # Create directory if not exists
            try:
                if self.create_destination is True:
                    self.directory = Path(self.directory).resolve()
                    self.directory.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                raise ComponentError(
                    f'UploadTo: Error creating destination directory {self.directory}: {err}'
                ) from err
            except Exception as err:
                self._logger.error(
                    f'Error creating destination directory {self.directory}: {err}'
                )
                raise ComponentError(
                    f'Error creating destination directory {self.directory}: {err}'
                ) from err
            try:
                self.filename = self.directory.joinpath(self.destination['filename'])
                self._logger.debug(
                    f'Raw Filename: {self.filename}\n'
                )
                if hasattr(self, 'masks'):
                    self.filename = self.mask_replacement(self.filename)
                    self._filenames.append(self.filename)
            except Exception:
                pass
        if self.url:
            # build headers (if required)
            self.build_headers()
        return True

    async def http_response(self, response: web.Response):
        """http_response.

        Return the request response of the HTTP Session

        Args:
            response (web.Response): the Response of the HTTP Session.

        Returns:
            Any: any processed data.
        """
        return response

    async def upload_session(self, url, method: str = 'get', data: Dict = None, data_format: str = 'json'):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
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
            params["json_serialize"] = json_encoder
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
                        raise ComponentError(
                            f'UploadTo: Error getting data from URL {response}'
                        )
            except aiohttp.HTTPError as err:
                raise ComponentError(
                    f'UploadTo: Error Making an SSL Connection to ({self.url}): {err}'
                ) from err
            except aiohttp.ClientSSLError as err:
                raise ComponentError(
                    f'UploadTo: SSL Certificate Error: {err}'
                ) from err

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    def start_pbar(self, total: int = 1):
        return tqdm(total=total)
