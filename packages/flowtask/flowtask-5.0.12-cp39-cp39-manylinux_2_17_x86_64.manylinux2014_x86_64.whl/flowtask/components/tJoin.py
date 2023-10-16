import asyncio
from collections.abc import Callable
import pandas
from asyncdb.exceptions import (
    NoDataFound
)
from flowtask.exceptions import (
    ComponentError,
    DataNotFound
)
from .abstract import DtComponent


class tJoin(DtComponent):
    """tJoin.

    Join two Dataframes in one, using SQL-like syntax
    """
    df1 = None
    df2 = None

    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self.type: str = 'left'
        super(tJoin, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if not hasattr(self, 'depends'):
            raise ComponentError(
                "Missing Dependency (depends) Attribute for declaring Sources."
            )
        if self._multi:
            try:
                self.df1 = self.previous[0].output()
            except IndexError as ex:
                name = self.depends[0]
                raise ComponentError(
                    f"Missing LEFT Dataframe: {name}"
                ) from ex
            try:
                self.df2 = self.previous[1].output()
            except IndexError as ex:
                name = self.depends[1]
                raise ComponentError(
                    "Missing RIGHT Dataframe"
                ) from ex
        elif hasattr(self, 'left'):
            # TODO: this not work:
            # think in a persistent structure to save every component after
            # execution, to get later
            # discover the "Left" Table
            try:
                _, num = self.left.split('_')
                left = self.JobTask.getJobByID(int(num)-1)
                self.df1 = left['component'].output()
            except KeyError as ex:
                raise DataNotFound(
                    f'Failed Left Task name: {self.left}'
                ) from ex
        elif hasattr(self, 'right'):
            # discover the "Left" Table
            try:
                _, num = self.right.split('_')
                right = self.JobTask.getJobByID(int(num)-1)
                self.df2 = right['component'].output()
            except KeyError as ex:
                raise DataNotFound(
                    f'Failed Right Task name: {self.right}'
                ) from ex
        else:
            raise DataNotFound(
                "Data Was Not Found for Join", status=404
            )
        return True

    async def run(self):
        args = {}
        if self.df1 is None:
            raise DataNotFound(
                "Main data Not Found for Join", status=404
            )
        if self.df1.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1", code=404)
        if self.type == 'left' and (self.df2 is None or self.df2.empty):
            self._result = self.df1
            return True
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 2", code=404)
        if hasattr(self, 'no_copy'):
            args['copy'] = self.no_copy
        if not self.type:
            self.type = 'inner'
            args['left_index'] = True
        if hasattr(self, 'args') and isinstance(self.args, dict):
            args = {**args, **self.args}
        if hasattr(self, 'operator'):
            operator = self.operator
        else:
            operator = 'and'
            if hasattr(self, 'fk'):
                args['on'] = self.fk
            else:
                args['left_index'] = True
        # making a Join between 2 dataframes
        try:
            if operator == 'and':
                df = pandas.merge(
                    self.df1,
                    self.df2,
                    how=self.type,
                    suffixes=('_left', '_right'),
                    **args
                )
            else:
                if hasattr(self, 'fk'):
                    args['left_on'] = self.fk
                else:
                    args['left_index'] = True
                ndf = self.df1
                sdf = self.df2.copy()
                merge = []
                for key in self.join_with:
                    d = pandas.merge(
                        ndf,
                        sdf,
                        right_on=key,
                        how=self.type,
                        suffixes=('_left', None),
                        **args
                    )
                    ndf = d[d[key].isnull()]
                    ndf.drop(ndf.columns[ndf.columns.str.contains(
                        '_left')], axis=1, inplace=True)
                    ddf = d[d[key].notnull()]
                    ddf.drop(ddf.columns[ddf.columns.str.contains(
                        '_left')], axis=1, inplace=True)
                    merge.append(ddf)
                # merge the last (not matched) rows
                merge.append(ndf)
                df = pandas.concat(merge, axis=0)
                df.reset_index(drop=True)
                df.is_copy = None
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f'Cannot Join with missing Column: {err!s}'
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Unknown JOIN error {err!s}"
            ) from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound(
                "Cannot make any JOIN, returns zero coincidences"
            )
        self._variables[f'{self.TaskName}_NUMROWS'] = numrows
        print('ON END> ', numrows)
        self.add_metric('JOINED_ROWS', numrows)
        if self._debug is True:
            print('::: Printing Column Information === ')
            for column, t in df.dtypes.items():
                print(column, '->', t, '->', df[column].iloc[0])
        # helping some transformations
        df.is_copy = None
        self._result = df
        return True

    async def close(self):
        pass
