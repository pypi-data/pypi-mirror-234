from aiohttp import web
from .http import HTTPHook


class UploadHook(HTTPHook):
    """UploadHook.

        Can be used to receive files on a web URL.
    """
    methods: list = ['GET', 'PUT']

    async def get(self, request: web.Request):
        print('CALLING GET')
        headers = {
            "x-status": "Empty",
            "x-message": "Module information not found",
        }
        return self.no_content(headers=headers)

    async def put(self, request: web.Request):
        pass
