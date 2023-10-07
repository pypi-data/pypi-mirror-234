import asyncio
from collections.abc import Callable
# logging system
import numpy as np
import pandas
from flowtask.components import DtComponent
from flowtask.exceptions import ComponentError, DataNotFound
import flowtask.components.FilterRows.functions as dffunctions
from flowtask.utils.functions import check_empty


class FilterRows(DtComponent):
    """
    FilterRows.

    Removing or cleaning rows based on some criteria.
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
        self._applied: list = []
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
        super(FilterRows, self).__init__(
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
            raise ComponentError("a Previous Component was not found.")
        if check_empty(self.data):
            raise DataNotFound(
                "No data was found"
            )

    async def run(self):
        if self.data is None:
            return False
        if isinstance(self.data, pandas.DataFrame):
            # add first metrics
            self.add_metric('started_rows', self.data.shape[0])
            self.add_metric('started_columns', self.data.shape[1])
            # start filtering
            if hasattr(self, "clean_strings"):
                u = self.data.select_dtypes(include=['object', 'string'])
                self.data[u.columns] = self.data[u.columns].fillna('')
            if hasattr(self, 'clean_numbers'):
                u = self.data.select_dtypes(include=['Int64'])
                #self.data[u.columns] = self.data[u.columns].fillna('')
                self.data[u.columns] = self.data[u.columns].replace(
                    ['nan', np.nan], 0, regex=True)
                u = self.data.select_dtypes(include=['float64'])
                self.data[u.columns] = self.data[u.columns].replace(
                    ['nan', np.nan], 0, regex=True)
            if hasattr(self, 'clean_dates'):
                u = self.data.select_dtypes(include=['datetime64[ns]'])
                self.data[u.columns] = self.data[u.columns].replace(
                    {np.nan: None})
                #df[u.columns] = df[u.columns].astype('datetime64[ns]')
            if hasattr(self, "drop_empty"):
                # First filter out those rows which
                # does not contain any data
                self.data.dropna(how='all')
                # removing empty cols
                self.data.is_copy = None
                self.data.dropna(axis=1, how='all')
                self.data.dropna(axis=0, how='all')
            if hasattr(self, 'dropna'):
                self.data.dropna(subset=self.dropna, how='all')
            # iterate over all filtering conditions:
            df = self.data
            it = df.copy()
            for ft, args in self.filter_conditions.items():
                self._applied.append(
                    f'Filter: {ft!s} args: {args}'
                )
                # TODO: create an expression builder
                # condition = dataframe[(dataframe[column].empty) & (dataframe[column]=='')].index
                # check if is a function
                try:
                    try:
                        func = getattr(dffunctions, ft)
                    except AttributeError:
                        func = globals()[ft]
                    if callable(func):
                        it = func(it, **args)
                except Exception as err:
                    print(f"Error on {ft}: {err}")
            else:
                df = it
            self._result = df
            passed = len(self._result.index)
            rejected = (len(self.data.index) - len(self._result.index))
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            self.add_metric('ended_rows', df.shape[0])
            self.add_metric('ended_columns', df.shape[1])
            self.add_metric('PASSED', passed)
            self.add_metric('REJECTED', rejected)
            self.add_metric('FILTERS', self._applied)
            self._variables[f'{self.TaskName}_PASSED'] = passed
            self._variables[f'{self.TaskName}_REJECTED'] = rejected
            if self._debug:
                self._logger.verbose(
                    f'PASSED: {passed}, REJECTED: {rejected}',
                )
                print('FILTERED ===')
                print(df)
                print('::: Printing Column Information === ')
                for column, t in df.dtypes.items():
                    print(column, '->', t, '->', df[column].iloc[0])
            return self._result
        else:
            return self._result

    def close(self):
        pass
