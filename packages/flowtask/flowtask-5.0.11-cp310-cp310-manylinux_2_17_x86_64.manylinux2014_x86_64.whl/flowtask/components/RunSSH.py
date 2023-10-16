import asyncio
from collections.abc import Callable
import logging
import asyncssh
from .abstract import DtComponent
from .interfaces.SSHClient import SSHClient


class RunSSH(SSHClient, DtComponent):
    """
    RunSSH.

    Run any arbitrary command into an SSH server.
    """

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        DtComponent.__init__(
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
        SSHClient.__init__(
            self,
            tunnel=tunnel,
            **self._params
        )

    async def start(self, **kwargs):
        """Start.

        Processing variables and credentials.
        """
        try:
            self.define_host()
            self.processing_credentials()
        except Exception as err:
            logging.error(err)
            raise

    async def run(self):

        result = {}
        await self.open(
            host=self.host,
            port=self.port,
            tunnel=self.tunnel,
            credentials=self.credentials
        )
        for command in self.commands:
            command = self.mask_replacement(command)
            try:
                rst = await self._connection.run(command, check=True)
                result[command] = {
                    "exit_status": rst.exit_status,
                    "returncode": rst.returncode,
                    "error": rst.stderr,
                    # "stdout": rst.stdout
                }
            except asyncssh.process.ProcessError as err:
                logging.error(
                    f"Error executing command: {err}"
                )
        self.add_metric('SSH: COMMAND', result)
        self._result = result
        return result
