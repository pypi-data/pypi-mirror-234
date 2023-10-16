from typing import Optional
from abc import ABC
import asyncio
import builtins
from navconfig.logging import logging
from flowtask.exceptions import ComponentError
from flowtask.types import SafeDict

## functions
# TODO: as object like TransformRows (replacing *)
from flowtask.utils.functions import *  # pylint: disable=W0614,W0401
from querysource.utils.functions import *  # pylint: disable=W0401,C0411


class FuncSupport(ABC):
    """
    Interface for adding Add Support for Function Replacement.
    """
    def __init__(
            self,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            **kwargs
    ):
        self._loop = self.event_loop(loop)

    def event_loop(
        self,
        evt: Optional[asyncio.AbstractEventLoop] = None
    ) -> asyncio.AbstractEventLoop:
        if evt is not None:
            asyncio.set_event_loop(evt)
            return evt
        else:
            try:
                return asyncio.get_event_loop()
            except RuntimeError as exc:
                raise RuntimeError(
                    f"There is no Event Loop: {exc}"
                ) from exc

    def getFunc(self, val):
        result = None
        try:
            if isinstance(val, list):
                fname = val[0]
                args = {}
                try:
                    args = val[1]
                except IndexError:
                    args = {}
                try:
                    fn = getattr(builtins, fname)
                except (TypeError, AttributeError):
                    fn = globals()[fname]
                if args:
                    result = fn(**args)
                else:
                    result = fn()
            elif val in self._variables:
                result = self._variables[val]
            elif val in self._mask:
                result = self._mask[val]
            else:
                result = val
            return result
        except Exception as err:
            raise ComponentError(
                f"{__name__}: Error parsing Pattern Function: {err}"
            ) from err

    def get_filepattern(self):
        if not hasattr(self, 'file'):
            return None
        fname = self.file['pattern']
        result = None
        try:
            val = self.file.get('value', fname)
            if isinstance(val, str):
                if val in self._variables:
                    # get from internal variables
                    result = self._variables[val]
            elif isinstance(val, list):
                func = val[0]
                try:
                    kwargs = val[1]
                except IndexError:
                    kwargs = None
                try:
                    f = getattr(builtins, func)
                    if kwargs:
                        result = f(**kwargs)
                    else:
                        result = f()
                except (TypeError, AttributeError):
                    try:
                        if kwargs:
                            result = globals()[func](**kwargs)
                        else:
                            result = globals()[func]()
                    except (TypeError, ValueError) as e:
                        logging.error(e)
            else:
                result = val
        except (NameError, KeyError) as err:
            logging.warning(f'FilePattern Error: {err}')
        return fname.format_map(SafeDict(value=result))
