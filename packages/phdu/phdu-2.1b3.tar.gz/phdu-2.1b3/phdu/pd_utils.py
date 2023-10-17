"""
pandas utils
"""
import pandas as pd
import numpy as np
from functools import reduce     
from .stats.rtopy import resample
from .stats.test import permutation

def latex_table(df, index=False, **kwargs):
    """Pandas DataFrame -> Latex table."""
    col_format = "c" if isinstance(df, pd.core.series.Series) else "c"*len(df.columns)
    if index:
        col_format += "c"
    table_replacements = (("\\toprule", "\\toprule "*2),
                          ("\\bottomrule", "\\bottomrule "*2)
    )
    text_replacements = (("\\textbackslash ", "\\"),
                         ("\{", "{"), 
                         ("\}", "}"),
                         ("\$", "$"),
                         ("\_", "_"),
                         ("\\textasciicircum ", "^")
    )
    table_formatter = lambda x:  reduce(lambda a, kv: a.replace(*kv), table_replacements, x)
    text_formatter = lambda x: reduce(lambda a, kv: a.replace(*kv), text_replacements, x)
    formatter = lambda x: text_formatter(table_formatter(x))
    print(formatter(df.to_latex(index=index, column_format=col_format, **kwargs)))
    return

def insert_level_sep(df, row_seps=1, col_seps=1):
    """
    Insert NaN rows and cols when the outer level of the MultiIndex changes.
    Example for three columns with col_seps=1:   c1, c2, c3    =>   c1, NANs, c2, NaNs, c3.
    
    This is useful when plotting a matrix and you want to visually separate different groups.
    """
    df_c = df.copy()
    col_levels = df.columns.get_level_values(0).unique() # respect the order
    row_levels = df.index.get_level_values(0).unique()
    for l in col_levels[:-1]:
        for k in range(col_seps):
            df_c[(l, " "*k)] = np.NaN 
    for l in row_levels[:-1]:
        for k in range(row_seps):
            df_c.loc[(l, " "*k), :] = np.NaN
    return df_c[col_levels].loc[row_levels]

def expand_sequences(df, dt=1, maxlen=None):
    """
    Input: DataFrame. Each element is an array and all arrays start at the same time and have the same time step dt.
    
    Returns: MultiColumn DataFrame: (df.index,  (df.columns, time_steps))
    """
    if df.isna().values.any():
        if maxlen is None:
            maxlen = int(df.applymap(lambda x: x.size if isinstance(x, np.ndarray) else np.NaN).max().max())
        df_padded = df.applymap(lambda x: np.hstack((x, np.NaN*np.empty((maxlen-x.size)))) if isinstance(x, np.ndarray) else np.NaN*np.empty((maxlen)))
    else:
        if maxlen is None:
            maxlen = int(df.applymap(lambda x: x.size).values.max())
        df_padded = df.applymap(lambda x: np.hstack((x, np.NaN*np.empty((maxlen-x.size)))))
    df_padded_arr = np.stack([np.vstack(x) for x in df_padded.values]) # shape (df.shape[0], df.shape[1], time_steps)
    return pd.DataFrame(df_padded_arr.reshape((df.shape[0], -1)), 
                        index = df.index, 
                        columns = pd.MultiIndex.from_product([df.columns, dt*np.arange(maxlen)]))

def tuple_wise(*dfs):
    """Returns dataframe where each element is a tuple containing the elements from other dataframes."""
    df = dfs[0]
    assert all(df.index.intersection(df2.index).size == df.shape[0] for df2 in dfs[1:])
    assert all(df.columns.intersection(df2.columns).size == df.shape[1] for df2 in dfs[1:])
    return pd.DataFrame(np.rec.fromarrays(tuple(df.values for df in dfs)).tolist(), 
                        columns=df.columns,
                        index=df.index)

def vstack_wise(*dfs):
    """
    Attributes: Dataframes where elements are arrays with equal length and have same indices and columns.
    
    Returns: DataFrame where df_ij = np.vstack((df1_ij, df2_ij, ...))
    """
    R = np.rec.fromarrays(tuple(df.values for df in dfs))
    df1_df2 = pd.Series([np.vstack(i) if all(isinstance(j, np.ndarray) for j in i) else np.NaN for i in R.flatten()], dtype=object,
                        index=dfs[0].stack(dropna=False).index).unstack()
    return df1_df2

def column_diffs(df, mode="to", mod_col=lambda x: "".join(np.array([*x])[[0, -1]])):
    """
    mode: '-'   (col2 - col1)
          'to' r'$col1 \to col2
    """
    N = df.shape[1]
    data = {}
    if mode == "-":
        label = lambda col1, col2: f"{col2} - {col1}"
    elif mode == "to":
        if callable(mod_col):
            label = lambda col1, col2: r"$\Huge {{{}}} \to {{{}}}$".format(mod_col(col1.replace(" ", "\ ")), mod_col(col2.replace(" ", "\ ")))            
        else:
            label = lambda col1, col2: r"$\Huge {{{}}} \to {{{}}}$".format(col1.replace(" ", "\ "), col2.replace(" ", "\ "))
    for i, col1 in enumerate(df.columns):
        if i < N:
            for col2 in df.columns[i+1:]:
                data[label(col1, col2)] = df[col2] - df[col1]
    return pd.DataFrame(data)

def CI_by_col(df, stat, return_sample_stat=True, fillna=None, **kwargs):
    CI = pd.Series({col: resample.CI_bootstrap(df[col].dropna().values, stat=stat, **kwargs) for col in df.columns})
    if fillna is not None:
        def aux(x):
            x[np.isnan(x)] = fillna
            return x
        CI = CI.apply(aux)
    if return_sample_stat:
        return CI, getattr(df, stat)()
    else:
        return CI
    
def permtest_by_col(df, alternative, stat="mean", paired=True, diff=True, label="c", **kwargs):
    """
    Test directionality accross columns. 
        col_i  (direction in [<, >, !=])  col_j     
        
    Attributes:
        alternative:    'less', 'greater', 'two-sided'.
    """
    P = {}
    N = df.shape[1]
    is_paired = "paired" if paired else "not_paired"
    is_diff = "diff" if diff else ""
    for i in range(N):
        for j in range(i+1, N):
            yi, yj = df.iloc[:, [i,j]].dropna().values.T
            P[r"$\Huge {}_{{{}{}}}$".format(label, i+1, j+1)] = getattr(permutation, f"permutation_test_2sample_{is_paired}_{is_diff}{stat}")(yi, yj, alternative=alternative, **kwargs)
    return pd.Series(P)