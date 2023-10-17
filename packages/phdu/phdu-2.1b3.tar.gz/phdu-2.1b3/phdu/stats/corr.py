"""
Correlation metrics
"""
import pandas as pd
import numpy as np

def corr_pruned(df, method='spearman', alpha=0.05):
    """
    Returns correlation between DataFrame features with pvalue < alpha.
    """
    import scipy.stats as ss
    corr_func = getattr(ss, f"{method}r")
    c = {}
    p = {}
    for col1 in df.columns:
        for col2 in df.columns:
            corr, pval = corr_func(*(df[[col1, col2]].dropna().values.T))
            c[(col1, col2)] = corr
            p[(col1, col2)] = pval
    c = pd.Series(c).unstack()
    p = pd.Series(p).unstack()
    c_pruned = c.copy()
    c_pruned[p > alpha] = np.NaN
    return c_pruned