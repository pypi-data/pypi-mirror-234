import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from navconfig.logging import logging
from flowtask.exceptions import ComponentError
from .abstract import DtComponent


class TransposeRows(DtComponent):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ):
        """Init Method."""
        self._pivot: list = kwargs.pop('pivot')
        self.preserve: bool = kwargs.pop('preserve_original', False)
        self.allow_empty: bool = kwargs.pop('allow_empty', False)
        if not self._pivot:
            raise ComponentError(
                "Missing List of Pivot Columns"
            )
        # columns to be transposed:
        # TODO: if not, then all columns not in Pivot list.
        self._columns = kwargs.pop('columns')
        super(TransposeRows, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", code=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Transpose: Incompatible Pandas Dataframe",
                code=404
            )
        if not hasattr(self, 'column'):
            raise ComponentError(
                "Transpose: Missing Column name for extracting row values"
            )
        if not hasattr(self, 'value'):
            raise ComponentError(
                "Transpose: Missing Column for Values"
            )
        return True

    async def close(self):
        pass

    def row_to_column(
        self,
        df: pd.DataFrame,
        row_to_pivot: str,
        new_name: str
    ):
        """
        Add a pivoted column to the dataframe based on the given column name.

        Parameters:
        - df: The input dataframe.
        - row_to_pivot: The column name to be pivoted.
        - new_name: The name of the column to be transposed.

        Returns:
        - Dataframe with the new pivoted column.
        """
        # Filter the dataframe to only include rows with the desired column_name
        df_filtered = df[df[self.column] == row_to_pivot]
        if df_filtered.empty is True:
            # there is no data to be filtered:
            if self.allow_empty is True:
                df[new_name] = np.nan
            return df
        # Pivot the filtered dataframe
        df_pivot = df_filtered.pivot_table(
            index=self._pivot,
            columns=self.column,
            values=self.value,
            aggfunc='first',
            dropna=False  # Preserve NaN values
        ).reset_index()
        df_pivot = df_pivot.rename(columns={row_to_pivot: new_name})
        # Merge the pivoted dataframe with the original dataframe
        df_merged = pd.merge(
            df,
            df_pivot,
            on=self._pivot,
            how='left'
        )
        if self.preserve is False:
            # Drop the original column_name and value columns for the pivoted rows
            df_merged = df_merged.drop(
                df_merged[(df_merged[self.column] == row_to_pivot)].index
            )
        return df_merged

    async def run(self):
        try:
            df = self.data
            for column, value in self._columns.items():
                try:
                    df_pivot = self.row_to_column(
                        df, column, value
                    )
                except Exception as err:
                    print(err)
                df = df_pivot
            if self._debug is True:
                print('=== TRANSPOSE ===')
                print(' = Data Types: = ')
                print(df.dtypes)
                print('::: Printing Column Information === ')
                for column, t in df.dtypes.items():
                    print(column, '->', t, '->', df[column].iloc[0])
            self._result = df
            return self._result
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f'Crosstab Error: {err!s}'
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Unknown error {err!s}"
            ) from err
