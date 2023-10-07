import os
import asyncio
import logging
from collections.abc import Callable
from pathlib import Path
from tqdm import tqdm
from asyncdb.exceptions import ProviderError
from flowtask.exceptions import (
    ComponentError,
    NotSupported
)
from flowtask.utils import check_empty
from .IteratorBase import IteratorBase


class FileList(IteratorBase):
    """
    FileList.

    Return the list of files in a Directory
    """
    generator: bool = False

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._path = None
        self.pattern = None
        self.data = None
        self.conditions = {}
        self.directory: str = None
        super(FileList, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Check if Directory exists."""
        await super(FileList, self).start()
        if not self.directory:
            raise ComponentError(
                "Error: need to specify a Directory"
            )
        # check if directory exists
        p = Path(self.directory)
        if p.exists() and p.is_dir():
            self._path = p
        else:
            raise ComponentError(
                "Error: Directory doesn't exist!"
            )
        return True

    def get_filelist(self):
        if self.pattern:
            value = self.pattern
            if hasattr(self, 'masks'):
                for mask, replace in self._mask.items():
                    value = str(value).replace(mask, replace)
            if self._variables:
                value = value.format(**self._variables)
            files = (f for f in self._path.glob(value))
        elif hasattr(self, 'file'):
            # using pattern/file version
            value = self.get_filepattern()
            files = (f for f in self._path.glob(value) if f.is_file())
        else:
            files = (f for f in self._path.iterdir() if f.is_file())
        files = sorted(files, key=os.path.getmtime)
        return files

    async def run(self):
        status = False
        if not self._path:
            return False
        if self.iterate:
            iterator = list(self.get_filelist())
            step, target, params = self.get_step()
            step_name = step.name
            # generate and iterator
            with tqdm(total=len(iterator)) as pbar:
                for file in iterator:
                    self._result = file
                    params['filename'] = file
                    params['directory'] = self.directory
                    logging.debug(f' :: Loading File: {file}')
                    status = False
                    job = self.get_job(target, **params)
                    if job:
                        pbar.set_description(f"Processing {file.name}")
                        try:
                            status = await self.async_job(job, step_name)
                            pbar.update(1)
                        except (ProviderError, ComponentError, NotSupported) as err:
                            raise NotSupported(
                                f"Error running Component {step_name}, error: {err}"
                            ) from err
                        except Exception as err:
                            raise ComponentError(
                                f"Generic Component Error on {step_name}, error: {err}"
                            ) from err
            if check_empty(status):
                return False
            else:
                return status
        else:
            files = self.get_filelist()
            if files:
                if self.generator is False:
                    self._result = list(files)
                else:
                    self._result = files
                self.add_metric('FILE_LIST', self._result)
                return self._result
            else:
                return False

    async def close(self):
        pass
