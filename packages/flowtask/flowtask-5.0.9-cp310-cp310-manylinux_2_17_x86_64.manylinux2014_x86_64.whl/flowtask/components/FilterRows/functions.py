"""Functions for FilterRows."""
import re
import numpy as np

def drop_columns(dataframe, columns=[]):
    if columns and isinstance(columns, list):
        dataframe.drop(axis=1, columns=columns, inplace=True, errors='ignore')
    return dataframe

def drop_rows(df, **kwargs):
    for column, expression in kwargs.items():
        if isinstance(expression, list):
            mask = df[column].isin(expression)
            df = df[~mask]
            df.head()
    return df

def drop_duplicates(dataframe, columns=[], **kwargs):
    if columns and isinstance(columns, list):
        dataframe.set_index(columns, inplace=True, drop=False)
        dataframe.sort_values(by=columns, inplace=True)
        dataframe.drop_duplicates(
             subset=columns,
             inplace=True,
             **kwargs
        )
    return dataframe

def clean_empty(dataframe, columns=[]):
    if columns and isinstance(columns, list):
        for column in columns:
            condition = dataframe[(dataframe[column].empty) | (dataframe[column]=='') | (dataframe[column].isna())].index
            dataframe.drop(condition, inplace=True)
    return dataframe

def suppress(dataframe, columns=[], **kwargs):
    if 'pattern' in kwargs:
        pattern = kwargs['pattern']
    def clean_chars(field):
        name = str(field)
        if re.search(pattern, name):
            pos = re.search(pattern, name).start()
            return str(name)[:pos]
        else:
            return name
    if columns and isinstance(columns, list):
        for column in columns:
            dataframe[column] = dataframe[column].astype(str)
            dataframe[column] = dataframe[column].apply(clean_chars)
    return dataframe


def fill_na(df, columns:list = [], fill_value='', **kwargs):
    #df[columns].fillna(fill_value, inplace=True)
    df[columns] = df[columns].astype(str).replace(['nan', np.nan], fill_value, regex=True)
    #self.data[u.columns].replace({pandas.NaT: None})
    return df
