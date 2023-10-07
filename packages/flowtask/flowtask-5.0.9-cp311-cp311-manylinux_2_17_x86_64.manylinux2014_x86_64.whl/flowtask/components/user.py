from typing import Optional, Any, Union
from collections.abc import Callable
from abc import ABC, abstractmethod
import random
from pathlib import Path, PurePath
import aiohttp
import orjson
import pandas as pd
from navconfig import config
from navconfig.logging import logging
from asyncdb.drivers.abstract import BaseDriver
from flowtask.exceptions import ComponentError, DataNotFound
from flowtask.utils import fnExecutor
from flowtask.utils.constants import (
    get_constant,
    get_func_value,
    is_constant,
    is_function
)
from flowtask.utils.functions import check_empty
from .support import (
    FuncSupport,
    DBSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport
)

ua = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (X11; Windows NT 10.0; rv:19.0) Gecko/20100101 Firefox/19.0 Iceweasel/19.0.2",
    "Mozilla/5.0 (X11; U; Linux i686; sk; rv:1.9.0.4) Gecko/2008111217 Fedora/3.0.4-1.fc10 Firefox/3.0.4"
]

class UserComponent(
    FuncSupport,
    DBSupport,
    ResultSupport,
    LogSupport,
    StatSupport,
    LocaleSupport,
    ABC
):
    """
     UserComponent
       Abstract Base Component for User-defined Components.
    """
    _memory: Optional[BaseDriver] = None
    TaskName: Optional[str] = None
    encoding: str = 'UTF-8'
    timeout: int = 60
    accept: str = 'application/xhtml+xml'

    def __init__(
            self,
            job: Optional[Callable] = None,
            **kwargs
    ):
        # stats object:
        self._variables: dict = {}  # variables
        self._vars = {}  # other vars
        self._mask = {}  # masks for function replacing
        self._params = {}  # other parameters
        self._ua = random.choice(ua)  # rotating UA
        ## Function Support
        FuncSupport.__init__(self, **kwargs)
        # Object Name:
        self.__name__: str = self.__class__.__name__
        # logging object
        LogSupport.__init__(
            self,
            name=self.__name__,
            **kwargs
        )
        # Result Object:
        ResultSupport.__init__(
            self,
            **kwargs
        )
        # Stat Support:
        StatSupport.__init__(
            self,
        )
        # Config Environment
        try:
            self._environment = kwargs['ENV']
            del kwargs['ENV']
        except (KeyError, AttributeError):
            self._environment = config
        # program
        try:
            self._program = kwargs['program']
            del kwargs['program']
        except KeyError:
            self._program = 'navigator'
        # getting the Task Pile (components pile)
        try:
            self._TaskPile: dict = kwargs['TaskPile']
            del kwargs['TaskPile']
            setattr(self, 'TaskPile', self._TaskPile)
        except KeyError:
            self._TaskPile = {}
        # Template Parser
        try:
            self._tplparser = kwargs['template']
            del kwargs['template']
        except KeyError:
            self._tplparser = None
        # for changing vars (in components with "vars" feature):
        try:
            self._vars = kwargs['_vars']
            del kwargs['_vars']
        except KeyError:
            pass
        # memcache connector
        try:
            self._memory = kwargs['memory']
            del kwargs['memory']
        except KeyError:
            try:
                self._memory = self._vars['memory']
                del self._vars['memory']
            except KeyError:
                pass
        # attributes (root-level of component arguments):
        try:
            self._attributes = kwargs['attributes']
            del kwargs['attributes']
        except KeyError:
            self._attributes = {}
        # conditions:
        try:
            self.conditions: dict = kwargs['conditions']
            del kwargs['conditions']
        except KeyError:
            pass
        # params:
        try:
            self._params = kwargs['params']
            del kwargs['params']
        except KeyError:
            self._params = {}
        # parameters
        try:
            self._parameters = kwargs['parameters']
            del kwargs['parameters']
        except KeyError:
            self._parameters = []
        # arguments list
        try:
            self._arguments = kwargs['arguments']
            del kwargs['arguments']
        except KeyError:
            self._arguments = []
        # processing variables
        try:
            variables = kwargs['variables']
            del kwargs['variables']
            if isinstance(variables, str):
                try:
                    variables = orjson.loads(variables)
                except ValueError:
                    try:
                        variables = dict(x.split(':')
                                         for x in variables.split(','))
                    except (TypeError, ValueError, IndexError):
                        variables = {}
            if variables:
                for arg, val in variables.items():
                    self._variables[arg] = val
        except KeyError:
            pass
        # previous Job has variables, need to update from existing
        if job:
            self._component = job
            if isinstance(job, list):
                self._multi = True
                variables = {}
                for j in job:
                    variables = {**variables, **j.variables}
                try:
                    self._variables = {**self._variables, **variables}
                except Exception as err:
                    print(err)
            else:
                try:
                    self._variables = {**self._variables, **job.variables}
                except Exception as err:
                    logging.error(f"User Component Error: {err}")
        # mask processing:
        try:
            masks = kwargs['_masks']
            del kwargs['_masks']
        except KeyError:
            masks = {}
        # filling Masks:
        if 'masks' in kwargs:
            self._mask = kwargs['masks']
            del kwargs['masks']
            object.__setattr__(self, 'masks', self._mask)
        for mask, replace in masks.items():
            self._mask[mask] = replace  # override component's masks
        try:
            for mask, replace in self._mask.items():
                # first: making replacement of masks based on vars:
                try:
                    if mask in self._variables:
                        value = self._variables[mask]
                    else:
                        value = replace.format(**self._variables)
                except Exception as err:
                    value = replace
                value = fnExecutor(value, env=self._environment)
                self._mask[mask] = value
        except Exception as err:
            logging.debug(f'Mask Error: {err}')
        try:
            self._params = {**self._params, **kwargs}
        except (TypeError, ValueError):
            pass
        ## parameters:
        for arg, val in self._params.items():
            # print('ALL PARAMETERS: ', arg, val)
            try:
                if arg == 'no-worker':
                    continue
                if arg == self.TaskName:
                    values = dict(x.split(':')
                                  for x in self._params[arg].split(','))
                    for key, value in values.items():
                        self._params[key] = value
                        object.__setattr__(self, key, value)
                elif arg not in ['program', 'TaskPile', 'TaskName']:
                        try:
                            setattr(self, arg, val)
                        except Exception as err:
                            logging.warning(f'UserComponent: Wrong Parameter: {arg}={val}')
                            logging.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # Localization
        LocaleSupport.__init__(
            self, **kwargs
        )
        # processing the variables:
        if hasattr(self, 'vars'):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val

    def config(self, key, default: Any = None) -> Any:
        return self._environment.get(key, fallback=default)

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"<{type(self).__name__}>"


    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def user_params(self):
        return self._params

    @abstractmethod
    async def start(self, **kwargs):
        """
        start.
            Initialize (if needed) a task
        """

    @abstractmethod
    async def run(self):
        """
        run.
            Close (if needed) a task
        """

    @abstractmethod
    async def close(self):
        """
        close.
            Close (if needed) a task
        """
    def mask_replacement(self, obj):
        for mask, replace in self._mask.items():
            if mask in self._variables:
                value = self._variables[mask]
            else:
                value = str(obj).replace(mask, str(replace))
            if isinstance(obj, PurePath):
                obj = Path(value).resolve()
            else:
                obj = value
        return obj

    def set_conditions(self, name: str = 'conditions'):
        if hasattr(self, name):
            obj = getattr(self, name)
            for condition, val in obj.items():
                if hasattr(self, condition):
                    obj[condition] = getattr(self, condition)
                elif is_constant(val):
                    obj[condition] = get_constant(val)
                elif is_function(val):
                    obj[condition] = get_func_value(val)
                if condition in self._variables:
                    obj[condition] = self._variables[condition]
                if condition in self._mask:
                    obj[condition] = self._mask[condition]
            if 'pattern' in obj:
                # getting conditions as patterns
                pattern = obj['pattern']
                del obj['pattern']
                for field in pattern:
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        result = self.getFunc(val)
                        obj[field] = result
            if self.conditions:
                for k, v in self.conditions.items():
                    # print('NEW CONDITION: ', k, v)
                    result = v
                    try:
                        if is_constant(v):
                            result = get_constant(v)
                        elif is_function(v):
                            result = get_func_value(v)
                    except Exception as err:
                        logging.exception(err)
                    obj[k] = result

    def create_dataframe(self, result: Union[list, dict]):
        if check_empty(result):
            self._variables['_numRows_'] = 0
            self._variables[f'{self.TaskName}_NUMROWS'] = 0
            raise DataNotFound(
                "UserComponent: No Data was Found."
            )
        try:
            df = pd.DataFrame(result)
            # Attempt to infer better dtypes for object columns.
            df.infer_objects()
            if hasattr(self, "infer_types"):
                df = df.convert_dtypes()
            if hasattr(self, "drop_empty"):
                df.dropna(axis=1, how='all', inplace=True)
                df.dropna(axis=0, how='all', inplace=True)
            if hasattr(self, 'dropna'):
                df.dropna(subset=self.dropna, how='all', inplace=True)
            if self._debug:
                print(df)
                print('::: Printing Column Information === ')
                columns = list(df.columns)
                for column in columns:
                    t = df[column].dtype
                    print(column, '->', t, '->', df[column].iloc[0])
            self._variables['_numRows_'] = len(df.index)
            self._variables[f'{self.TaskName}_NUMROWS'] = len(df.index)
            return df
        except Exception as err:
            logging.error(
                f'Error Creating Dataframe {err!s}'
            )

    async def session(
            self,
            url: str,
            method: str = 'get',
            headers: Optional[dict] = None,
            auth: Optional[dict] = None,
            data: Optional[dict] = None
        ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        proxy = None
        hdrs = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self._ua
        }
        if headers:
            hdrs = {**hdrs, **headers}
        async with aiohttp.ClientSession(auth) as session:
            if method == 'get':
                obj = session.get(
                    url,
                    headers=hdrs,
                    timeout=timeout,
                    proxy=proxy
                )
            elif method == 'post':
                obj = session.post(
                    url,
                    headers=hdrs,
                    timeout=timeout,
                    proxy=proxy,
                    data=data
                )
            async with obj as response:
                if (status := response.status) not in (200, 204, 203, 206, 404):
                    raise ComponentError(
                        f"Error on Session: status: {status}, {response}"
                    )
                return response
