from abc import ABC
import os
from navconfig import config


class EnvSupport(ABC):
    """EnvSupport.

    Support for Environment Variables
    """
    def __init__(
            self,
            *args,
            **kwargs
    ):
        self._environment = config

    def get_env_value(self, key, default: str = None):
        if key is None:
            return None
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key
