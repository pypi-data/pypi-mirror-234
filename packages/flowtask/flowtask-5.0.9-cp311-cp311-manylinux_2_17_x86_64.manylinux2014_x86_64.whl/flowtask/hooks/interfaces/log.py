from abc import ABC
import traceback
from navconfig.logging import logging
from flowtask.utils import cPrint
from flowtask.exceptions import ComponentError


class LogSupport(ABC):
    """LogSupport.

    Adding Logging support to every FlowTask Component.
    """
    def __init__(
            self,
            **kwargs
    ):
        try:
            self._name_ = kwargs['name']
        except KeyError:
            self._name_ = self.__class__.__name__
        # logging object
        self._logger = logging.getLogger(
            f"FlowTask.Hooks.{self._name_}"
        )
        # Debugging
        try:
            self._debug = bool(kwargs['debug'])
            del kwargs['debug']
        except KeyError:
            self._debug = False
        if self._debug is True:
            self._logger.setLevel(logging.DEBUG)

    def log(self, message) -> None:
        self._logger.info(message)
        if self._debug is True:
            cPrint(message, level='INFO')

    def debug(self, message):
        self._logger.debug(message)
        if self._debug is True:
            cPrint(message, level='DEBUG')

    def warning(self, message):
        self._logger.warning(message)
        if self._debug is True:
            cPrint(message, level='WARN')

    def exception(self, message):
        self._logger.exception(message, stack_info=True)
        if self._debug is True:
            cPrint(message, level='CRITICAL')

    def echo(self, message: str, level: str = 'INFO') -> None:
        cPrint(message, level=level)

    def error(
            self,
            message: str,
            exc: BaseException,
            status: int = 400,
            stacktrace: bool = False
    ):
        payload = None
        if stacktrace is True:
            payload = traceback.format_exc()
        raise ComponentError(
            f"{message}, error={exc}",
            status=status,
            stacktrace=payload
        ) from exc
