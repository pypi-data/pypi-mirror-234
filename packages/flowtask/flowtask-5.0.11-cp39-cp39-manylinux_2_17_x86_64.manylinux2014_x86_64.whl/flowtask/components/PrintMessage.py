# -*- coding: utf-8 -*-
import logging
from asyncdb.utils.functions import colors, cPrint
from flowtask.utils import SafeDict
from .abstract import DtComponent

logger = logging.getLogger(__name__)


class PrintMessage(DtComponent):
    """
    PrintMessage.

       Overview

         This component print a simple message

    .. table:: Properties
       :widths: auto

    +--------------+----------+-----------+--------------------------------------------+
    | Name         | Required | Summary                                                |
    +--------------+----------+-----------+--------------------------------------------+
    |  message     |   Yes    | Print message to display                               |
    +--------------+----------+-----------+--------------------------------------------+
    |  color       |   Yes    | Print the color of the message to show                 |
    +--------------+----------+-----------+--------------------------------------------+
    |  level       |   Yes    | Identifies the level of the displayed error            |
    +--------------+----------+-----------+--------------------------------------------+
    |  first       |   Yes    | First message                                          |
    +--------------+----------+-----------+--------------------------------------------+
    |  last        |   Yes    | Last message                                           |
    +--------------+----------+-----------+--------------------------------------------+

    Return the list of arbitrary days
    """

    coloring = None
    color = None
    level = 'INFO'

    async def start(self, **kwargs):
        """Initialize the color setup."""
        if self.previous:
            self.data = self.input
        try:
            if self.color:
                try:
                    self.coloring = colors.bold + getattr(
                        colors.fg, self.color)
                except Exception as err:
                    logging.error(
                        f'Wrong color schema {self.color}, error: {err}'
                    )
                    self.coloring = colors.reset
            elif self.level:
                if self.level == 'INFO':
                    self.coloring = colors.bold + colors.fg.green
                elif self.level == 'DEBUG':
                    self.coloring = colors.fg.lightblue
                elif self.level == 'WARN':
                    self.coloring = colors.bold + colors.fg.yellow
                elif self.level == 'ERROR':
                    self.coloring = colors.fg.lightred
                elif self.level == 'CRITICAL':
                    self.coloring = colors.bold + colors.fg.red
                else:
                    self.coloring = colors.reset
            else:
                self.coloring = colors.reset
            return True
        except (NameError, ValueError):
            self.coloring = colors.reset

    async def run(self):
        """Run Message."""
        self._result = self.data
        try:
            if hasattr(self, 'condition'):
                for val in self._variables:
                    self.condition = self.condition.replace(
                        '{{{}}}'.format(str(val)),
                        str(self._variables[val])
                    )
                if not eval(self.condition):  # pylint: disable=W0123
                    return False
            msg = self.message.format_map(SafeDict(**self._params))
            for val in self._variables:
                msg = msg.replace(
                    '{{{}}}'.format(str(val)),
                    str(self._variables[val])
                )
            print(self.coloring + msg, colors.reset)
            if self._debug:
                logging.debug(msg)
                cPrint(msg)
            if 'PRINT_MESSAGE' not in self._variables:
                self._variables['PRINT_MESSAGE'] = {}
            if self.level not in self._variables['PRINT_MESSAGE']:
                self._variables['PRINT_MESSAGE'][self.level] = []
            self._variables['PRINT_MESSAGE'][self.level].append(msg)
            self.add_metric('message', msg)
        except Exception as err:
            self._logger.exception(
                f'PrintMessage Error: {err}'
            )
            return False
        return self._result

    async def close(self):
        """Method."""
