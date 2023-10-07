import asyncio
from collections.abc import Callable
from pathlib import Path, PurePath
import asyncssh
from navconfig.logging import logging
from flowtask.exceptions import FileError, ComponentError, FileNotFound
from .DownloadFrom import DownloadFromBase
from .interfaces.SSHClient import SSHClient


class DownloadFromSFTP(SSHClient, DownloadFromBase):
    """
    DownloadFromSFTP

    Overview

            Download a file from its source from an-SFTP


    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+-------------------------------------------+
    | Name         | Required | Summary                                               |
    +--------------+----------+-----------+-------------------------------------------+
    | credentials  |   Yes    | Credentials to establish connection with FTP          |
    +--------------+----------+-----------+-------------------------------------------+
    | whole_dir    |   Yes    | Download the entire directory                         |
    +--------------+----------+-----------+-------------------------------------------+

    Return the list of arbitrary days

    """
    to_remove = (
        "file",
        "filename",
        "directory",
        "source",
        "destination",
        "create_destination",
        "overwrite",
        "rename"
    )

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.mdate = None
        self.local_name = None
        self.rename: str = None
        self.filename: str = ''
        self.whole_dir: bool = False
        DownloadFromBase.__init__(
            self,
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        tunnel = {}
        if hasattr(self, 'tunnel'):
            tunnel = self.tunnel
            del self._params['tunnel']
        # removing unnecesary elements on params:
        params = self._params.copy()
        if hasattr(self, 'max_requests'):
            params['max_requests'] = self.max_requests
        if hasattr(self, 'block_size'):
            params['block_size'] = self.block_size
        for el in self.to_remove:
            try:
                del params[el]
            except KeyError:
                pass
        SSHClient.__init__(
            self,
            tunnel=tunnel,
            **params
        )
        self.create_destination: bool = True  # by default

    def start(self):
        super(DownloadFromSFTP, self).start()
        if hasattr(self, 'source'):
            self.whole_dir = self.source['whole_dir'] if 'whole_dir' in self.source else False
        if hasattr(self, 'file'):
            if 'mdate' in self.file:
                self.mdate = self.file['mdate']
        # Mask in rename file
        if hasattr(self, 'masks'):
            try:
                for mask, replace in self._mask.items():
                    if self.rename is not None:
                        self.rename = self.rename.replace(mask, str(replace))
                    if self.mdate is not None:
                        self.mdate = self.mdate.replace(mask, replace)
            except Exception as e:
                raise ComponentError(f"{e!s}") from e
            self.rename = Path(
                '{}/{}'.format(self.directory, self.rename)
            )
        if self.rename is not None:
            self.local_name = self.rename
        else:
            self.local_name = Path(
                '{}/{}'.format(
                    self.directory, PurePath(self.filename).name
                )
            )
        return True

    def download_progress(self, srcpath, dstpath, bytes_copied, total_bytes):
        self._filenames[dstpath] = srcpath
        self._pb.reset(total=total_bytes)
        self._pb.update(bytes_copied)
        self._pb.refresh()

    async def download(self):
        try:
            await self.open(
                host=self.host,
                port=self.port,
                tunnel=self.tunnel,
                credentials=self.credentials
            )
        except asyncio.CancelledError:
            self._logger.info(
                f'{self.host} CANCELED~'
            )
            # break
        except (asyncio.TimeoutError, ComponentError) as err:
            raise ComponentError(
                f"Error: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Error: {err}"
            ) from err
        async with self._connection.start_sftp_client() as sftp:
            # check all versions of functionalities
            args = {
                "block_size": self.block_size,
                "max_requests": self.max_requests,
                "progress_handler": self.download_progress,
                "error_handler": self.err_handler
            }
            if self.whole_dir is True:
                if hasattr(self, 'source'):  # using the source/destination filosophy
                    args['remotepaths'] = self.source_dir
                    args['localpath'] = self.directory
                    args['recurse'] = True if 'recursive' in self.source else False
                else:
                    raise ComponentError(
                        '*Whole Dir* and self.source are mutually inclusive, \
                            missing self.source'
                    )
                # getting the stats of the remote path:
                stats = await sftp.listdir(path=self.source_dir)
                self.start_progress(total=len(stats))
            else:
                filelist = []
                if self._srcfiles:
                    logging.debug(f'FILES::: {self._srcfiles}')
                    for file in self._srcfiles:
                        if self.mdate is not None:
                            flist = await self.get_mtime_files(sftp, file, self.mdate)
                            filelist += flist
                            if not flist:
                                raise FileNotFound(
                                    f'File Not Found for modification date {self.mdate}'
                                )
                        else:
                            filelist.append(file)
                else:
                    filelist = self.filename
                args['remotepaths'] = filelist
                args['localpath'] = self.directory
                args['preserve'] = True
                self.start_progress(total=len(filelist))
            try:
                await sftp.mget(
                    **args
                )
                self.close_progress()
                # get all the files downloaded
                result = list(self._filenames.keys())
                self._result = [
                    v.decode('utf8') for v in result
                ]
                # Rename file if only one
                if len(self._result) == 1 and self.rename is not None:
                    f = Path(self._result[0])
                    f.rename(self.local_name)
                    self._result[0] = self.local_name
                if hasattr(self, 'remove') and self.remove is True:
                    try:
                        for _, filename in self._filenames.items():
                            logging.debug(
                                f'Removing remote file: {filename}'
                            )
                            await sftp.remove(filename)
                    except (asyncssh.sftp.SFTPError) as err:
                        logging.error(f'SFTP error: {err}')
                return True
            except (OSError) as err:
                self._logger.error(err)
                raise ComponentError(
                    f'SFTP Local error: {err}'
                ) from err
            except (asyncssh.sftp.SFTPNoSuchFile) as err:
                raise FileNotFound(
                    f'File Not Found: {err}'
                ) from err
            except (asyncssh.sftp.SFTPError) as err:
                self._logger.error(err)
                raise FileError(
                    f'SFTP server error: {err}'
                ) from err
            except (asyncssh.Error) as err:
                self._logger.error(err)
                raise ComponentError(
                    f'SFTP connection failed: {err}'
                ) from err
            except FileNotFound:
                raise
            except Exception as err:
                self._logger.exception(err, stack_info=True)
                raise ComponentError(
                    f'SFTP Error: {err}'
                ) from err

    async def run(self):
        """Running Download file."""
        self._result = None
        status = False
        if self.overwrite is False and self.local_name.is_file():
            # file already exists and can be skipped
            self._filenames = [str(self.local_name)]
            self._result = [str(self.local_name)]
            status = True
        else:
            try:
                status = await self.download()
            except FileNotFound:
                raise
            except FileError:
                raise
            except ComponentError:
                raise
            except Exception as exc:
                raise ComponentError(
                    f"{exc}"
                ) from exc
        if status is False:
            return False
        else:
            self.add_metric('SFTP_FILES', self._result)
            return self._result
