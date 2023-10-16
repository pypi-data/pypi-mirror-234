import pandas as pd

def df_switch_columns(df: pd.DataFrame, column1, column2):
    """
    Returns a new DataFrame with the required columns switched (DOES NOT MODIFY ORIGINAL DATAFRAME)
    """
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df

def df_switch_rows(df: pd.DataFrame, row1, row2):
    """
    Returns a new DataFrame with the required rows switched (DOES NOT MODIFY ORIGINAL DATAFRAME), not efficient for very large DataFrames (>1000 rows)
    """
    ids = df.index.tolist()
    a, b = ids.index(row1), ids.index(row2)
    ids[a], ids[b] = ids[b], ids[a]
    df = df.reindex(ids)
    return df

def df_create(columns, indices) -> pd.DataFrame:
    """
    Returns a new DataFrame with the specified columns and indexes, 
    these can be given as a list of names (columns -> ["Input 1", "Input 2"], rows -> ["Experiment 1", "Experiment 2"])
    or as a number of columns or indexes.
    It is valid to supply a list for the columns and a number for the indices, and vice versa.
    """
    if type(columns) == int and type(indices) == int:
        return pd.DataFrame(columns=range(columns), index=range(indices)).fillna(0)
    elif type(columns) == int and type(indices) == list:
        return pd.DataFrame(columns=range(columns), index=indices).fillna(0)
    elif type(columns) == list and type(indices) == int:
        return pd.DataFrame(columns=columns, index=range(indices)).fillna(0)
    elif type(columns) == list and type(indices) == list: 
        return pd.DataFrame(columns=columns, index=indices).fillna(0)
    else:
        raise TypeError("Only integers or lists are supported!")