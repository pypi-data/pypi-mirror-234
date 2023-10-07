from typing import Optional, Any
import glob
import os
from abc import ABC, abstractmethod
from pathlib import Path, PurePath
from collections.abc import Callable
import orjson
from navconfig import config
from flowtask.conf import (
    FILE_STORAGES
)
from flowtask.exceptions import FileNotFound
from flowtask.utils import SafeDict, fnExecutor
from flowtask.utils.constants import (
    get_constant,
    get_func_value,
    is_constant,
    is_function
)
from .support import (
    FuncSupport,
    DBSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    TemplateSupport
)
from .support.log import SkipErrors


class DtComponent(
    FuncSupport,
    DBSupport,
    ResultSupport,
    LogSupport,
    StatSupport,
    LocaleSupport,
    TemplateSupport,
    ABC
):
    """Abstract

    Overview:

            Helper for building components that consume REST APIs

        .. table:: Properties
       :widths: auto
    +--------------+----------+-----------+--------------------------------------+
    | Name         | Required | Summary                                          |
    +--------------+----------+-----------+--------------------------------------+
    |  method      |   Yes    | Component for Data Integrator                    |
    +--------------+----------+-----------+--------------------------------------+
    |  attributes  |   Yes    | Attribute: barcode                               |
    +--------------+----------+-----------+--------------------------------------+


    Return the list of arbitrary days

    """
    TaskName: Optional[str] = None

    def __init__(
            self,
            job: Optional[Callable] = None,
            **kwargs
    ):
        # Future Logic: trigger logic:
        self.runIf: list = []
        self.triggers: list = []
        # vars
        self._TaskPile: dict = {}
        self._environment = None
        self._attrs: dict = {}  # attributes
        self._variables = {}  # variables
        self._vars = {}  # other vars
        self._mask = {}  # masks for function replacing
        self._params = {}  # other parameters
        self._args: dict = {}
        self._filestore: Any = None
        ## Function Support
        FuncSupport.__init__(self, **kwargs)
        # Object Name:
        self.__name__: str = self.__class__.__name__
        # logging object
        LogSupport.__init__(
            self,
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
        # Jinja2 Template Support:
        TemplateSupport.__init__(
            self,
        )
        # program
        try:
            self._program = kwargs['program']
            del kwargs['program']
        except KeyError:
            self._program = 'navigator'
        # getting the argument parser:
        try:
            self._argparser = kwargs['argparser']
            del kwargs['argparser']
        except KeyError:
            self._argparser = None
        # getting the Task Pile (components pile)
        try:
            self._TaskPile = kwargs['TaskPile']
            del kwargs['TaskPile']
            setattr(self, 'TaskPile', self._TaskPile)
        except KeyError:
            pass
        # Config Environment
        try:
            self._environment = kwargs['ENV']
            del kwargs['ENV']
        except (KeyError, AttributeError):
            self._environment = config
        # for changing vars (in components with "vars" feature):
        try:
            self._vars = kwargs['_vars']
            del kwargs['_vars']
        except KeyError:
            pass
        # attributes (root-level of component arguments):
        try:
            self._attributes = kwargs['attributes']
            del kwargs['attributes']
        except KeyError:
            self._attributes = {}
        try:
            self._args = kwargs['_args']
            del kwargs['_args']
        except KeyError:
            self._args = {}
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
        self._multi: bool = False
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
                    print(err)
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
                except Exception:
                    value = replace
                value = fnExecutor(value, env=self._environment)
                self._mask[mask] = value
        except Exception as err:
            self._logger.debug(f'Mask Error: {err}')
        # existing parameters:
        try:
            self._params = {**kwargs, **self._params}
        except (TypeError, ValueError):
            pass
        for arg, val in self._params.items():
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
                    self._attrs[arg] = val
                    if arg in self._attributes:
                        val = self._attributes[arg]
                    try:
                        setattr(self, arg, val)
                    except Exception as err:
                        self._logger.warning(f'Wrong Attribute: {arg}={val}')
                        self._logger.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # attributes: component-based parameters (only for that component):
        for key, val in self._attributes.items():
            # TODO: check Attributes
            if key in self._attributes:
                # i need to override attibute
                current_val = self._attributes[key]
                if isinstance(current_val, dict):
                    val = {**current_val, **val}
                elif isinstance(current_val, list):
                    current_val.append(val)
                    val = current_val
                try:
                    object.__setattr__(self, key, val)
                    self._attrs[key] = val
                except (ValueError, AttributeError) as err:
                    self._logger.error(err)
        # Localization:
        LocaleSupport.__init__(
            self, **kwargs
        )
        # processing the variables:
        if hasattr(self, 'vars'):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val
        ### File Storage:
        self._fileStorage = FILE_STORAGES
        # SkipError:
        if self.skipError == 'skip':
            self.skipError = SkipErrors.SKIP
        elif self.skipError == 'log':
            self.skipError = SkipErrors.LOG
        else:
            self.skipError = SkipErrors.ENFORCE

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def set_filestore(self, store):
        self._filestore = store

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

        Run operations declared inside Component.
        """

    @abstractmethod
    async def close(self):
        """
        close.

        Close (if needed) component requirements.
        """

    def ComponentName(self):
        return self.__name__

    def user_params(self):
        return self._params

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def setVar(self, name, value):
        # self._logger.debug(f'Setting VAR ON: {name} = {value}')
        self._variables[name] = value

    def setTaskVar(self, name, value):
        name = f"{self.TaskName}_{name}"
        self._variables[name] = value

    def set_attributes(self, name: str = 'pattern'):
        if hasattr(self, name):
            obj = getattr(self, name)
            for field, val in obj.items():
                if field in self._params:
                    # already calculated:
                    self._attrs[field] = self._params[field]
                    setattr(self, field, self._params[field])
                elif field in self._attributes:
                    self._attrs[field] = self._attributes[field]
                    setattr(self, field, self._attributes[field])
                elif field in self._parameters:
                    self._attrs[field] = self._parameters[field]
                    setattr(self, field, self._parameters[field])
                elif field in self._variables:
                    self._attrs[field] = self._variables[field]
                    setattr(self, field, self._variables[field])
                else:
                    value = self.getFunc(val)
                    self._attrs[field] = value
                    setattr(self, field, value)
            del self._attrs['pattern']

    def get_obj(self, name, parent):
        try:
            if not parent:
                return getattr(self, name)
            else:
                return parent[name]
        except AttributeError:
            return False

    def get_pattern(self, obj):
        try:
            pattern = obj['pattern']
            # del obj['pattern']
            return pattern, obj
        except Exception:
            return None, obj

    def process_pattern(self, name: str = 'file', parent=None):
        if not (obj := self.get_obj(name, parent)):
            return False
        # pattern has the form {file, value}:
        if not isinstance(obj, dict):
            return obj

        # first, I need the pattern object:
        pattern, obj = self.get_pattern(obj)
        if pattern is None:
            return obj

        # processing the rest of variables:
        if self._vars and f'{name}.pattern' in self._vars:
            pattern = self._vars[f'{name}.pattern']
        elif self._variables and 'pattern' in self._variables:
            pattern = self._variables['pattern']
        elif 'value' in self._variables:
            pattern = pattern.format_map(SafeDict(value=self._variables['value']))
        if self._vars and f'{name}.value' in self._vars:
            result = self._vars[f'{name}.value']
            return pattern.format_map(SafeDict(value=result))
        elif 'value' in obj:
            # simple replacement:
            result = self.getFunc(obj['value'])
            # print('RESULT IS ', result)
            return pattern.format_map(SafeDict(value=result))
        elif 'values' in obj:
            variables = {}
            result = obj['values']
            for key, val in result.items():
                variables[key] = self.getFunc(val)
            return pattern.format_map(SafeDict(**variables))
        else:
            # multi-value replacement
            variables = {}
            if self._variables:
                pattern = pattern.format_map(SafeDict(**self._variables))
            for key, val in obj.items():
                if key in self._variables:
                    variables[key] = self._variables[key]
                else:
                    variables[key] = self.getFunc(val)
            return pattern.format_map(SafeDict(**variables))

    def process_mask(self, name):
        if hasattr(self, name):
            obj = getattr(self, name)
            for key, value in obj.items():
                if key in self._vars:
                    obj[key] = self._vars[key]
                elif self._vars and f'{name}.{key}' in self._vars:
                    obj[key] = self._vars[f'{name}.{key}']
                elif key in self._variables:
                    obj[key] = self._variables[key]
                else:
                    # processing mask
                    for mask, replace in self._mask.items():
                        obj[key] = value.replace(mask, str(replace))
            return obj
        else:
            return {}

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

    def set_variables(self, obj):
        return obj.format_map(SafeDict(**self._variables))

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
                elif condition in self._mask:
                    obj[condition] = self._mask[condition]
                elif condition in self.conditions:
                    obj[condition] = val
            if 'pattern' in obj:
                pattern = obj['pattern']
                del obj['pattern']
                # getting conditions as patterns
                for field in pattern:
                    if field in obj:
                        # already settled
                        continue
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        if is_constant(val):
                            result = get_constant(val)
                        else:
                            result = self.getFunc(val)
                        obj[field] = result

    def get_filename(self):
        """
        get_filename.
        Detect if File exists.
        """
        if not self.filename:  # pylint: disable=E0203
            if hasattr(self, "file") and self.file:
                file = self.get_filepattern()
                if (filelist := glob.glob(os.path.join(self.directory, file))):
                    self.filename = filelist[0]
                    self._variables['__FILEPATH__'] = self.filename
                    self._variables['__FILENAME__'] = os.path.basename(
                        self.filename)
                else:
                    raise FileNotFound(
                        f"File is empty or doesn't exists: {file}"
                    )
            elif self.previous:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = filenames[0]
                        self._variables['__FILEPATH__'] = self.filename
                        self._variables['__FILENAME__'] = os.path.basename(
                            self.filename)
                    except IndexError as e:
                        raise FileNotFound(
                            f"({__name__}): File is empty or doesn't exists"
                        ) from e
            else:
                raise FileNotFound(
                    f"({__name__}): File is empty or doesn't exists"
                )
        else:
            return self.filename

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key
