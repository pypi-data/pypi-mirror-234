from .abstract import AbstractAction


class Dummy(AbstractAction):
    """Dummy.

    Simply Print the Action object.
    """
    async def open(self):
        pass

    async def run(self, *args, **kwargs):
        print(
            "Running action with arguments:", self._args, self._kwargs
        )

    async def close(self):
        print('Closing Action on Dummy.')
