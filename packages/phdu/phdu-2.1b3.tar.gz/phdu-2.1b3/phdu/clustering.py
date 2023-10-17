"""
Hierarchical clustering. In the future will include more algorithms
"""
import pandas as pd
import numpy as np
from .stats import corr
try:
    from scipy.cluster import hierarchy
    import matplotlib.pyplot as plt
except:
    pass
try:
    import plotly.express as px
    from .plots.plotly_utils import get_figure, set_multicategory_from_df
except:
    pass


def hierarchy_dendrogram(X, fontsize=30, out='data'):
    """
    Notes on the linkage matrix:
    This matrix represents a dendrogram, where elements
        1, 2: two clusters merged at each step,
        3: distance between these clusters,
        4: size of the new cluster - the number of original data points included.
    """
    is_df = isinstance(X, pd.core.frame.DataFrame)
    if is_df:
        labels = X.columns.to_list()
    else:
        labels = [*range(X.shape[1])] if len(X.shape) > 1 else None #int(-1 + np.sqrt(1 + 8*X.size)/2))]

    fig = plt.figure(figsize=(8, 12))
    ax = plt.subplot(111)

    corr_linkage = hierarchy.ward(X.values if is_df else X)
    dendro = hierarchy.dendrogram(
        corr_linkage, labels=labels, ax=ax, leaf_rotation=90 #orientation="left"
    )
    if out == 'data':
        plt.close()
        return corr_linkage, dendro
    elif out == 'fig':
        if not is_df:
            plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        else:
            plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        return fig
    else:
        raise ValueError(f"out '{out}' not valid. Available: 'data', 'fig'.")

def dendrogram_sort(df, to_distance = lambda x: 1 - x):
    """
    Attempts to sort the rows and columns of a matrix according to the dendrogram.

    Attributes:
        df: pandas DataFrame or numpy array
        to_distance: function to convert the input df to a distance matrix

        lambda x: 1 - x is useful when dealing with probabilities in a confusion matrix.

    Returns a pandas DataFrame or numpy array with the rows and columns ordered according to the dendrogram
    """
    _, dendro = hierarchy_dendrogram(to_distance(df))
    order = dendro["leaves"]
    if isinstance(df, pd.core.frame.DataFrame):
        df = df.iloc[order,:].iloc[:, order]
    elif isinstance(df, np.ndarray):
        df = df[order,:][:, order]
    else:
        raise ValueError("df must be a pandas DataFrame or a numpy array")
    return df


def hierarchical_cluster_matrix(df, title, colorbar_x=0.9, ticksize=16, cmin=-1, cmax=1, cmap='inferno'):
    _, dendro = hierarchy_dendrogram(df)
    order = dendro["leaves"]
    #corr = X.corr() if isinstance(X, pd.core.frame.DataFrame) else np.corrcoef(X)
    df_ordered = df.iloc[order,:].iloc[:, order]
    fig = px.imshow(df_ordered, color_continuous_scale=cmap)
    fig.update_layout(margin=dict(l=0, b=30, r=60, t=10, pad=1), xaxis_tickfont_size=ticksize, yaxis_tickfont_size=ticksize,
                      coloraxis=dict(cmin=cmin, cmax=cmax, colorbar=dict(title_text=title, tickfont_size=16, title_font_size=20, x=colorbar_x)),
                      height=800, width=1000, font_size=20, hovermode=False)
    if isinstance(df.index, pd.core.indexes.multi.MultiIndex):
        set_multicategory_from_df(fig, df_ordered)
    return fig

def corr_cluster_matrix(df, method='spearman', alpha=0.05, absolute_value=False, **kwargs):
    """"
    corr:  spearman, pearson.
    """
    df_corr = corr.corr_pruned(df, method=method, alpha=alpha).fillna(0)
    title = method.capitalize()
    if absolute_value:
        df_corr = df_corr.abs()
        title = f"|{title}|"
    return hierarchical_cluster_matrix(df_corr, title, **kwargs)
