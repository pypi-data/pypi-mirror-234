from typing import Optional
from abc import ABC
import logging
import locale


class LocaleSupport(ABC):
    """LocaleSupport.

    Adding Support for Encoding and Locale to every Component in FlowTask.
    """
    encoding: str = 'UTF-8'
    locale: Optional[str] = None

    def __init__(self, **kwargs):
        if not self.encoding:
            self.encoding = 'UTF-8'
        if 'l18n' in kwargs:
            self.locale = kwargs['l18n']
        # Localization
        if self.locale is None:
            newloc = (locale.getlocale())[0]
            self.locale = f'{newloc}.{self.encoding}'
        else:
            self.locale = f'{self.locale}.{self.encoding}'
        try:
            # avoid errors on unsupported locales
            locale.setlocale(locale.LC_TIME, self.locale)
        except (RuntimeError, NameError, locale.Error) as err:
            logging.warning(f'Error on Locale Support: {err}')
            newloc = (locale.getlocale())[0]
            self.locale = f'{newloc}.UTF-8'
            locale.setlocale(locale.LC_TIME, self.locale)
