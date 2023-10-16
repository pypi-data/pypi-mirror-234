"""
   UpdateOperationalVars

    Overview

        This component allows us to update the variables specified in
        the table “process_variables” of the schema “troc“

    .. table:: Properties
       :widths: auto


    +--------------+----------+-----------+-------------------------------------------+
    | Name         | Required | Summary                                               |
    +--------------+----------+-----------+-------------------------------------------+
    |  name        |   Yes    | Indicate the name of the variable to updated          |
    +--------------+----------+-----------+-------------------------------------------+
    |  value       |   Yes    | Receive a variable that indicate the value of the     |
    |              |          | established after the updated                         |
    +--------------+----------+-----------+-------------------------------------------+
    |  masks       |   Yes    | This option is a section where we can dynamically     |
    |              |          | define the value of the variable to be set later      |
    +--------------+----------+-----------+-------------------------------------------+

    Return the list of arbitrary days

"""
import asyncio
import logging
from typing import (
    Any
)
from collections.abc import Callable
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class UpdateOperationalVars(DtComponent):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self.value: Any = None
        super(UpdateOperationalVars, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        try:
            self.value = self.mask_replacement(self.value)
        except Exception as err:
            raise ComponentError(
                f'Error adding mask [{err.__class__.__name__}]: {err}'
            ) from err

    async def close(self):
        pass

    async def set_variable(self, variable, value, program: str = None):
        if not program:
            program = self._program
        sql = f"""UPDATE troc.process_variables SET raw_value = '{value}', \
        updated_at = CURRENT_DATE
        WHERE program_slug = '{program}' AND variable_name = '{variable}'"""
        logging.debug(f"VAR SQL: {sql}")
        try:
            connection = self.get_connection(event_loop=self._loop)
        except Exception as err:
            logging.exception(err, stack_info=True)
            raise
        async with await connection.connection() as conn:
            try:
                ok = await conn.execute(sql)
                if ok:
                    self.add_metric('SET_VARIABLE', f"{variable}={value}")
                    return True
                else:
                    return False
            except Exception as err:
                logging.exception(err)
                return False

    async def run(self):
        self._result = self.data
        try:
            # Replace variables
            for val in self._variables:
                if isinstance(self._variables[val], list):
                    if isinstance(self._variables[val], int):
                        self._variables[val] = ', '.join(self._variables[val])
                    else:
                        self._variables[val] = ', '.join(
                            "'{}'".format(v) for v in self._variables[val]
                        )
                self.value = self.value.replace(
                    '{{{}}}'.format(str(val)),
                    str(self._variables[val])
                )
            if hasattr(self, 'program_slug'):
                program = self.program_slug
            else:
                program = self._program
            if hasattr(self, 'name'):
                self._environment.set(self.name, self.value)
                value = self._environment.get(self.name)
                if value == self.value:
                    await self.set_variable(self.name, value, program)
                else:
                    return self._result
            elif hasattr(self, 'names'):
                value = None
                for name in self.names:
                    try:
                        self._environment.set(name, self.value)
                        value = self._environment.get(name)
                    except Exception as err:
                        print(err)
                    if value == self.value:
                        await self.set_variable(name, value, program)
            return self._result
        except Exception as err:
            print(err)
            raise ComponentError(
                f'Error setting operational variable [{err.__class__.__name__}]: {err}'
            ) from err
