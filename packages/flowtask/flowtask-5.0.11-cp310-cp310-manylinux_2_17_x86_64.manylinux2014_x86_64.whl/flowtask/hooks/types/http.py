from navigator.views import BaseHandler
from navigator.libs.json import JSONContent
from navigator.types import WebApp
from .base import BaseHook


class HTTPHook(BaseHook, BaseHandler):
    """HTTPHook.

        base Hook for all aiohttp-based hooks.
    """
    methods: list = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(HTTPHook, self).__init__(*args, **kwargs)
        self.url = f"/api/v1/webhook/{self.trigger_id}"
        self._json = JSONContent()

    def setup(self, app: WebApp) -> None:
        super().setup(app)
        self.logger.notice(
            f"Set the unique URL Trigger to: {self.url}"
        )
        for method in self.methods:
            cls = getattr(self, method.lower())
            if cls:
                self.app.router.add_route(
                    method, self.url, cls
                )
