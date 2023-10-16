import builtins
import logging
import re
from collections.abc import Callable

# from flowtask.utils import *
from querysource.utils.functions import *

### Constants Utilities for DataIntegrator.
DI_CONSTANTS = [
    "CURRENT_DATE",
    "CURRENT_TIMESTAMP",
    "CURRENT_YEAR",
    "CURRENT_MONTH",
    "CURRENT_MIDNIGHT",
    "YESTERDAY_TIMESTAMP",
    "YESTERDAY_MIDNIGHT",
    "TODAY",
    "YESTERDAY",
    "FDOM",
    "LDOM"
]

it_func = re.compile('^(\w+)\((.*)\)')

def is_constant(value):
    return value in DI_CONSTANTS

def is_function(value):
    if '(' in str(value):
        fn, args = it_func.match(value).groups()
        # also, I need to know if exists on global values
        func = globals()[fn]
        if not func:
            return False
        else:
            return True
    else:
        return False

def get_func_value(value):
    result = None
    f, args = it_func.match(value).groups()
    args = args.split(',')
    # logging.debug(f'Conditions: Calling FN {f}, {args}')
    try:
        func = globals()[f]
        if not func:
            try:
                func = getattr(builtins, f)
            except AttributeError:
                return None
        if callable(func):
            # logging.debug(f'CALLING FUNCTION {func!s} with args: {args!r}')
            result = func(*args)
    except Exception as err:
        logging.exception(err)
    finally:
        return result



def get_constant(value: str, *args, **kwargs) -> Callable:
    fn = None
    try:
        f = value.lower()
        # logging.debug(f'Conditions: Calling function {value}, {f}')
        if value in DI_CONSTANTS:
            fn = globals()[f](*args, **kwargs)
        else:
            func = globals()[f]
            if not func:
                try:
                    func = getattr(builtins, f)
                except AttributeError:
                    return None
            if func and callable(func):
                try:
                    fn = func(*args, **kwargs)
                except Exception as err:
                    raise Exception(err) from err
    finally:
        return fn
