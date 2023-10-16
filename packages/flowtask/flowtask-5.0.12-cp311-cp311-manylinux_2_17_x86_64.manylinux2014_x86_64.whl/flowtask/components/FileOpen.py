from pathlib import Path, PurePath
import io
from aiofile import AIOFile
from flowtask.exceptions import FileNotFound, FileError

from .FileBase import FileBase

class FileOpen(FileBase):
    """
    FileOpen.

        Open a file and returns content.
    """
    async def run(self):
        """Run File checking."""
        self._result = {}
        file = None
        if isinstance(self._filenames, list) and len(self._filenames) > 0:
            # concatenate all files in one result:
            for file in self._filenames:
                if isinstance(file, str):
                    file = Path(file)
                if file.exists() and file.is_file():
                    async with AIOFile(file, 'w+') as afp:
                        content = await afp.read()
                        stream = io.StringIO(content)
                        stream.seek(0)
                        self._result[file.name] = stream
                else:
                    self._logger.error(
                        f'FileExists: File doesn\'t exists: {file}'
                    )
        elif hasattr(self, 'filename'):
            if isinstance(self.filename, str):
                file = Path(file)
            elif isinstance(self.filename, PurePath):
                file = self.filename.resolve()
            else:
                raise FileError(
                    f'FileExists: unrecognized type for Filename: {type(self.filename)}'
                )
            if file.exists() and file.is_file():
                async with AIOFile(file, 'w+') as afp:
                    content = await afp.read()
                    stream = io.StringIO(content)
                    stream.seek(0)
                    self._result[file.name] = stream
            else:
                raise FileNotFound(
                    f'FileExists: Empty result: {self._filenames}'
                )
        # add metric:
        self.add_metric('FILENAME', self._filenames)
        return self._result

    async def close(self):
        """Method."""
