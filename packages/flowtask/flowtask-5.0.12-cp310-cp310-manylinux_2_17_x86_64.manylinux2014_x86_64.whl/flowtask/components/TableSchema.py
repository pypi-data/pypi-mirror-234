"""
TableSchema.

 Overview

        Read a CSV file and create the table schema using Data-Models.
        TODO: create an "alter table" if table exists but changed.

    .. table:: Properties
       :widths: auto


    +----------------+----------+-----------+-------------------------------------------------------+
    | Name           | Required | Summary                                                           |
    +----------------+----------+-----------+-------------------------------------------------------+
    |  start         |   Yes    | We initialize the component obtaining the data through the        |
    |                |          | through the parameter type                                        |
    +----------------+----------+-----------+-------------------------------------------------------+
    |  close         |   Yes    | The close method of a file object flushes any unwritten data and  |
    |                |          | closes the file object                                            |
    +----------------+----------+-----------+-------------------------------------------------------+
    |rename_repeated |   Yes    | Rename repeated columns and format them                           |
    |  _col          |          |                                                                   |
    +----------------+----------+-----------+-------------------------------------------------------+
    |  run           |   Yes    | This method executes the function                                 |
    +----------------+----------+-----------+-------------------------------------------------------+
    |  hasattr       |   Yes    | The hasattr function returns True  data and if the specified      |
    |                |          | object has the specified attribute, otherwise False               |
    +----------------+----------+-----------+-------------------------------------------------------+



    Return the list of arbitrary days

"""
import asyncio
from typing import (
    Dict,
    Any
)
from collections.abc import Callable
from pathlib import PosixPath, Path
import re
from decimal import Decimal
import datetime
import numpy as np
import pandas as pd
import dask.dataframe as dd
from asyncdb.models import Model
import dateparser
from navconfig.logging import logging
from flowtask.exceptions import (
    FileError,
    ComponentError,
    DataNotFound
)
from .abstract import DtComponent


logging.getLogger('fsspec').setLevel(logging.CRITICAL)


dtypes = {
    "varchar": str,
    "character varying": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "integer": int,
    "bigint": np.int64,
    "int64": np.int64,
    "uint64": np.int64,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "date": datetime.date
}


excel_based = [
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "text/xml"
]


# adding support for primary keys on raw tables
pk_sentence = """ALTER TABLE {schema}.{table}
ADD CONSTRAINT {schema}_{table}_pkey PRIMARY KEY({fields});"""

def datetime_to_name(value: datetime.datetime, mask: str):
    return value.strftime(mask)

def is_snakecase(value):
    ## already in snake case:
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]+_[a-zA-Z0-9]*$', value.strip()) is not None

def is_camelcase(value):
    return re.match(r'^[A-Za-z0-9]+\s?(?:[A-Za-z0-9])*$', value.strip()) is not None

def camelCase_split(value):
    if bool(re.match(r'[A-Z]+$', value)):
        return re.findall(r'[A-Z]+$', value)
    elif bool(re.search(r'\d', value)):
        return re.findall(r'[A-Z](?:[a-z]+[1-9]?|[A-Z]*(?=[A-Z])|$)', value)
    elif value[0].isupper():
        return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', value)
    else:
        # value = value.capitalize()
        return re.findall(r'^[a-z]+|[A-Z][^A-Z]*', value)

def remove_illegal_chars(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9_\s]+', '', value)

class TableSchema(DtComponent):
    """
        TableSchema.
        Open a CSV-file, create a DataModel and normalize field names.
    """
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop = None,
            job: Callable = None,
            stat: Callable = None,
            **kwargs
    ) -> None:
        """Init Method."""
        self.separator: str = ','
        self.params: Dict = {}
        self.fields: Dict = {}
        self.replace_names: Dict = {}
        self.drop: bool = False
        self.data: Any = None
        self.filename: str = None
        # info about table:
        self.tablename: str = None
        self.schema: str = None
        super(TableSchema, self).__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = PosixPath(self.input[0])
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            elif isinstance(self.input, dict):
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = PosixPath(filenames[0])
                    except IndexError as err:
                        raise FileError(
                            f"File doesnt exists: {filenames}"
                        ) from err
            elif isinstance(self.input, dd.DataFrame) or isinstance(self.input, pd.DataFrame):
                self.filename = None
                self.data = self.input
            else:
                raise FileError(
                    f"File doesnt exists: {self.input}"
                )
        elif hasattr(self, 'filename'):
            self.filename = Path(self.filename)
        else:
            raise ComponentError(
                "TableSchema: This Component requires a File or Dataframe from input."
            )

    async def close(self):
        pass

    def rename_repeated_col(self, col, cols):
        renamed = False
        count = 1
        for c, t in cols:
            if c == col:
                if not renamed:
                    col = f'{col}_{count}'
                    count += 1
                    renamed = True
                else:
                    col = col.split('_', 1)[0]
                    col = f'{col}_{count}'
                    count += 1
        return col

    async def run(self):
        self.result = None
        if not hasattr(self, 'mime'):
            self.mime = 'text/csv'
        if self.filename:
            if self.mime in excel_based:
                if self.mime == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    # xlsx or any openxml based document
                    file_engine = self.params.get('file_engine', 'openpyxl')
                elif self.mime == 'application/vnd.ms-excel.sheet.binary.macroEnabled.12':
                    file_engine = self.params.get('file_engine', 'pyxlsb')
                else:
                    try:
                        ext = self.filename.suffix
                    except (AttributeError, ValueError):
                        ext = '.xls'
                    if ext == '.xls':
                        file_engine = self.params.get('file_engine', 'xlrd')
                    else:
                        file_engine = self.params.get(
                            'file_engine', 'openpyxl')
                # passed arguments to Pandas directly
                arguments = {**self.params}
                if hasattr(self, 'pd_args') and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                print('>>>> ARGS: ', arguments)
                df = pd.read_excel(
                    self.filename,
                    engine=file_engine,
                    keep_default_na=True,
                    na_filter=False,
                    **arguments
                )
            else:
                self.params = {
                    "infer_datetime_format": True
                }
                arguments = {**self.params}
                if hasattr(self, 'pd_args') and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                print('>>>> ARGS: ', arguments)
                try:
                    # can we use pyarrow.
                    engine = arguments['engine']
                    del arguments['engine']
                except KeyError:
                    engine = 'c'
                tp = pd.read_csv(
                    self.filename,
                    sep=self.separator,
                    decimal=',',
                    engine=engine,
                    keep_default_na=False,
                    na_values=['TBD', 'NULL', 'null'],
                    na_filter=True,
                    skipinitialspace=True,
                    iterator=True,
                    chunksize=1000,
                    **arguments
                )
                df = pd.concat(tp, ignore_index=True)
            # read filename from self.filename
            self._result = self.filename
        elif self.data is not None:
            # is already a dataframe:
            df = self.data
            self._result = self.data
        else:
            return False
        if df is None or df.empty:
            raise DataNotFound(
                f"Empty File or Data: {self.filename}"
            )
        # adding stat from dataframe:
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        self.add_metric('COLUMNS', df.columns)
        self.add_metric('ROWS', len(df.index))
        # removing empty cols
        if hasattr(self, "drop_empty"):
            df.dropna(axis='columns', how='all', inplace=True)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        if hasattr(self, 'dropna'):
            df.dropna(subset=self.dropna, how='all', inplace=True)
        if hasattr(self, "trim"):
            cols = list(df.columns)
            for col in cols:
                df[col] = df[col].astype(str).str.strip()
        if self._debug:
            print(df)
            # print('COLS: >> ', df.columns)
        columns = df.columns
        cols = []
        replaced_columns = list(self.replace_names.keys())
        if hasattr(self, 'pre_rename'):
            ### can rename columns PREVIOUS TO normalize
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                if col in self.pre_rename:
                    col = self.pre_rename[col]
                col = self.rename_repeated_col(col, cols)
                f = (col, t)
                cols.append(f)
        elif hasattr(self, 'normalize_names'):
            # TODO: avoid SQL-reserved words like SELECT, WITH, etc.
            for col in columns:
                datatypes = str(df.dtypes[col])
                t = str
                tmp_col = col
                try:
                    t = dtypes[datatypes]
                    data = df[col].iloc[0]
                    if datatypes == 'object':
                        # try to infer datatype:
                        if isinstance(data, str) and data != np.nan:
                            if data.isalpha():
                                t = str
                            else:
                                try:
                                    dt = dateparser.parse(
                                        str(data),
                                        settings={'TIMEZONE': 'UTC'}
                                    )
                                    if isinstance(dt, datetime.datetime):
                                        t = datetime.datetime
                                except (ValueError, TypeError):
                                    pass
                except KeyError:
                    t = str

                if isinstance(col, (datetime.datetime, datetime.date)):
                    mask = getattr(self, 'mask_datetime', '%b_%d_%Y')
                    new_name = datetime_to_name(col, mask)
                elif is_snakecase(col):
                    new_name = col.strip().lower()
                elif is_camelcase(col):
                    new_name = '_'.join(
                        [x.lower().strip() for x in camelCase_split(col)]
                    )
                else:
                    new_name = re.sub(r'[^a-zA-Z0-9_]', '', col).strip()
                    if hasattr(self, 'normalize'):
                        ## making some changes on col_name:
                        if 'remove_prefix' in self.normalize and self.normalize['remove_prefix']:
                            prefix = self.normalize['remove_prefix']
                            new_name = new_name.removeprefix(prefix)
                        if 'trim' in self.normalize and self.normalize['trim'] is True:
                            new_name = new_name.strip()
                        ### remove any illegal character
                        new_name = remove_illegal_chars(new_name)
                        # re-covert again from camelCase:
                        if 'camelcase' in self.normalize and self.normalize['camelcase'] is True:
                            new_name = new_name.replace(" ", "").translate(str.maketrans("", "", "/:."))
                            new_name = re.sub(r'\([^)]*\)', '', new_name)
                        else:
                            new_name = '_'.join(
                                [x.lower().strip() for x in camelCase_split(new_name)]
                            )
                # RENAMING THE COLUMN WITH A NEW NAME:
                if new_name in replaced_columns:
                    replace = self.replace_names[new_name]
                    if isinstance(replace, str):
                        new_name = self.replace_names[new_name]
                    elif isinstance(replace, dict):
                        if 'name' in replace:
                            new_name = replace['name']
                        if 'type' in replace:
                            t = dtypes[replace['type']]
                    else:
                        # wrong arguments for Replace Names
                        pass
                if new_name in self.fields:
                    t = dtypes[self.fields[new_name]]
                new_name = self.rename_repeated_col(new_name, cols)
                f = (new_name, t)
                cols.append(f)
                if tmp_col == new_name:
                    self._logger.warning(f'The Column \'{new_name}\' has not normalized')
                else:
                    self._logger.debug(
                        f' - Normalized Name: {new_name}'
                    )
        else:
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                col = self.rename_repeated_col(col, cols)
                f = (col, t)
                cols.append(f)
        try:
            cls = Model.make_model(
                name=self.tablename,
                schema=self.schema,
                fields=cols
            )
        except Exception as err:
            print('ERROR:', err)
            raise ComponentError(
                str(err)
            ) from err
        if cls:
            mdl = cls()  # empty model, I only need the schema
            # TODO: open the metadata table and compare with model
            if sql := mdl.model(dialect='sql'):
                print('SQL IS ', sql)
                db = self.get_connection()
                async with await db.connection() as conn:
                    if self.drop is True:
                        result, error = await conn.execute(
                            sentence=f"DROP TABLE IF EXISTS {self.schema}.{self.tablename};"
                        )
                        logging.debug(f'TableSchema: {result}, {error}')
                    result, error = await conn.execute(
                        sentence=sql
                    )
                    if error:
                        raise ComponentError(
                            f'Error on Table creation: {error}'
                        )
                    else:
                        self.add_metric('Table', result)
                        if self._debug is True:
                            logging.debug(
                                f'TableSchema: {result!s}'
                            )
                    # add Primary Key to table:
                    if hasattr(self, 'pk'):
                        pk = pk_sentence.format(
                            schema=self.schema,
                            table=self.tablename,
                            fields=','.join(self.pk)
                        )
                        _primary, error = await conn.execute(
                            sentence=pk
                        )
                        logging.debug(f'TableSchema: PK creation: {_primary}, {error}')
        # passthrough the previous component value:
        self._result = self.input
        return self.input
