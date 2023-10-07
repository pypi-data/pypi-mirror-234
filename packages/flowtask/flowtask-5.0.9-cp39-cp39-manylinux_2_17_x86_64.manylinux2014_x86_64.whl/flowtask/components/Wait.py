import asyncio
from .abstract import DtComponent


class Wait(DtComponent):
    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        return True

    async def close(self):
        pass

    async def run(self):
        await asyncio.sleep(self.wait)
        self.add_metric('WAIT', self.wait)
        self._result = self.data
        return self._result
