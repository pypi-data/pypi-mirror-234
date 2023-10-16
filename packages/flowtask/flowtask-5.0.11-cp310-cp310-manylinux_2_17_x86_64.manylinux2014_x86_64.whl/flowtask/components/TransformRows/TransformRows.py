import asyncio
import copy
from collections.abc import Callable
import pandas
import numpy as np
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from flowtask.components import DtComponent
from flowtask.exceptions import ComponentError, DataNotFound
# moving this outside of TranformRows
import flowtask.components.TransformRows.functions as dffunctions
from flowtask.utils.executor import getFunction
from flowtask.utils import AttrDict
from flowtask.utils.functions import check_empty


class TransformRows(DtComponent):
    """TransformRows.

    Tranform, add or modify rows based on some criteria
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        self.fields: dict = {}
        self.filter_conditions: dict = {}
        self.clean_notnull: bool = True
        self.replace_columns: bool = False
        self._applied: list = []
        if 'replace_columns' in kwargs:
            self.replace_columns = kwargs['replace_columns']
            del kwargs['replace_columns']
        # support for multiple dataframe transformations
        try:
            self.multi = bool(kwargs['multi'])
            del kwargs['multi']
        except KeyError:
            self.multi = False
        if self.multi is False:
            if 'fields' in kwargs:
                self.fields = kwargs['fields']
                del kwargs['fields']
        else:
            self.fields = {}
        super(TransformRows, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "a Previous Component was not found."
            )
        if check_empty(self.data):
            raise DataNotFound(
                "No data was found"
            )

    async def run(self):
        if self.data is None:
            return False
        if isinstance(self.data, pandas.DataFrame):
            self.add_metric('started_rows', self.data.shape[0])
            self.add_metric('started_columns', self.data.shape[1])
            df = await self.transform(self, self.data)
            self._result = df
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            return self._result
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    f'TransformRows: Invalid Result type for Multiple: {err}'
                ) from err
            self._result = {}
            for name, rs in result:
                try:
                    el = getattr(self, name)
                except AttributeError:
                    self._result[name] = rs
                    continue
                df = await self.transform(AttrDict(el), rs)
                self._result[name] = df
            return self._result
        else:
            raise NoDataFound(
                "TransformRows: Pandas Dataframe Empty or is not a Dataframe"
            )

    async def transform(self, elem, df):
        try:
            fields = copy.deepcopy(elem.fields)
        except KeyError:
            fields = {}
        if not isinstance(df, pandas.DataFrame):
            raise NoDataFound(
                "Pandas Dataframe Empty or is not a Dataframe"
            )
        if hasattr(elem, 'clean_dates'):
            u = df.select_dtypes(include=['datetime64[ns]'])
            df[u.columns] = df[u.columns].replace({np.nan: None})
        it = df.copy()
        for field, val in fields.items():
            # logging.debug(f'Transform: CALLING {field} for {val}')
            if isinstance(val, str):
                try:
                    it[field] = it[val]
                    if self.replace_columns is True:
                        it.drop(val, axis='columns', inplace=True)
                    continue
                except KeyError:
                    self._logger.error(f'Column doesn\'t exists: {val}')
                    continue
            try:
                if 'value' in val:
                    operation = val['value']
                else:
                    operation = val
                args = {}
                try:
                    fname = operation.pop(0)
                    self._applied.append(
                        f'Function: {fname!s} args: {operation}'
                    )
                    # fname is a field and len > 1
                    if fname in it.columns and len(operation) == 0:
                        # simple field replacement
                        it[field] = it[fname]
                        it = it.copy()
                        continue
                    # only calls functions on TransformRows scope:
                    # first, check if is a Pandas-based Function
                    try:
                        args = operation[0]
                    except IndexError:
                        args = {}
                    try:
                        func = getattr(dffunctions, fname)
                        logging.debug(
                            f'Calling Function: {fname!s} with args: {operation}'
                        )
                        if fname == 'fill_column':
                            args['variables'] = self._variables
                        if args:
                            it = func(df=it, field=field, **args)
                        else:
                            it = func(df=it, field=field)
                        it = it.copy()
                        continue
                    except AttributeError:
                        try:
                            func = getFunction(fname)
                            logging.debug(
                                f'Calling Scalar Function: {fname!s} with args: {args}'
                            )
                        except Exception as err:
                            self._logger.exception(err)
                            func = None
                        if callable(func):
                            # SCALAR FUNCTION
                            try:
                                tmp = operation[0]
                                for a, b in tmp.items():
                                    if isinstance(b, list):
                                        for idx, el in enumerate(b):
                                            if el in self._variables:
                                                b[idx] = el.replace(
                                                    str(el),
                                                    str(self._variables[str(el)])
                                                )
                                    if b in self._variables:
                                        args[a] = b.replace(
                                            str(b),
                                            str(self._variables[str(b)])
                                        )
                                result = func(**args)
                            except (KeyError, IndexError, ValueError):
                                result = func()
                            r = {
                                field: result
                            }
                            it = it.assign(**r)
                            it = it.copy()
                        else:
                            logging.warning(f'Function {func} is not callable.')
                            continue
                except Exception as err:
                    logging.warning(f'Error or missing DF Function: {err!s}')
                    # using scalar functions to set value in columns
                    func = getFunction(fname)
                    logging.debug(
                        f'Calling Scalar: {fname!s}: {func}'
                    )
                    if callable(func):
                        try:
                            try:
                                args = operation[0]
                                tmp = operation[0]
                                for a, b in tmp.items():
                                    if b in self._variables:
                                        args[a] = b.replace(
                                            str(b),
                                            str(self._variables[str(b)])
                                        )
                                result = func(**args)
                            except TypeError:
                                # result doesn't need keyword arguments
                                result = func()
                            except (KeyError, IndexError, ValueError):
                                result = func()
                            r = {
                                field: result
                            }
                            it = it.assign(**r)
                            it = it.copy()
                        except Exception as e:
                            print(func, fname, field, val)
                            self._logger.exception(
                                f'Error Running an Scalar Function {fname!s} \
                                to set Dataframe: {e}'
                            )
                    else:
                        self._logger.exception(
                            f"Error on Transform Function {fname}: {err}"
                        )
            except Exception as err:
                self._logger.exception(
                    f"Error on {field}: {err}"
                )
        # at the end
        df = it
        # starting changes:
        if hasattr(elem, 'clean_str'):
            df.is_copy = None
            u = df.select_dtypes(include=['object', 'string'])
            u = u.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df[u.columns] = df[u.columns].fillna('')
        if hasattr(elem, "drop_empty"):
            # First filter out those rows which
            # does not contain any data
            df.dropna(how='all')
            # removing empty cols
            df.is_copy = None
            df.dropna(axis=1, how='all')
            df.dropna(axis=0, how='all')
        if self._debug is True:
            print('TRANSFORM ===')
            print(df)
            print('::: Printing Column Information === ')
            for column, t in df.dtypes.items():
                print(column, '->', t, '->', df[column].iloc[0])
        # avoid threat the Dataframe as a Copy
        df.is_copy = None
        self._result = df
        try:
            self.add_metric('ended_rows', df.shape[0])
            self.add_metric('ended_columns', df.shape[1])
            self.add_metric('Transformations', self._applied)
        except Exception as err:
            logging.error(
                f'TransformRows: Error setting Metrics: {err}'
            )
        return self._result

    def close(self):
        pass
