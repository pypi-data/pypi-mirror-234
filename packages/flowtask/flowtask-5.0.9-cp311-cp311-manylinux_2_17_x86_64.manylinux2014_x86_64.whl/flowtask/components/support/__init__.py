"""
Support add interfaces for many support options on Task Components.
"""
from .func import FuncSupport
from .db import DBSupport
from .log import LogSupport
from .result import ResultSupport
from .stat import StatSupport
from .locale import LocaleSupport
from .template import TemplateSupport

__all__ = (
    'FuncSupport',
    'DBSupport',
    'LogSupport',
    'ResultSupport',
    'StatSupport',
    'LocaleSupport',
    'TemplateSupport',
)
