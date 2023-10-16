import pandas as pd
import pyperclip as pc

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

def copy_to_clipboard(var: str):
    pc.copy(var)

def df_to_latex(df: pd.DataFrame, number_of_decimals: int | None = None, index: bool = False, copy_to_clipboard: bool = True):
    """
    Turns Pandas DataFrame into a LaTeX table, formatted as ||r|...|r|| for the given number of columns in the
    DataFrame (because I like the way it looks), automatically copies result into clipboard if copy_to_clipboard is not set to False
    """
    if number_of_decimals == None:
        float_format = None
    else:
        float_format = "%." + str(number_of_decimals) + "g"

    table_format = r"||"
    for i in range(len(df.columns)):
        table_format += r"r|"
    table_format += "|"
    basic_latex = df.to_latex(index=index, float_format=float_format, column_format=table_format)
    latex = basic_latex.replace(r"\toprule", r"\hline\hline").replace(r"\midrule", r"\hline\hline").replace(r"\bottomrule", r"\hline")
    latex = latex.replace(r"\\", r"\\\hline").replace(r"\\\hline", r"\\", 1)
    if copy_to_clipboard:
        pc.copy(latex)
    return latex
