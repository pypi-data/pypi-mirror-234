# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from beartype import beartype
from beartype.typing import Union, List
import pandas as pd
import networkx as nx
from dramkit.iotools import load_df_pd
from dramkit.gentools import check_list_arg, isna


@beartype
def gen_digraph_edge_list(edge_list: List[tuple]):
    '''
    | 生成有向图，edge_list为有向边属性，格式如: 
    |     [(from, to, {attr1: v1, attr2: v2, ...}), ...]
    '''
    g = nx.DiGraph()
    g.add_edges_from(edge_list)
    return g


def gen_digraph_df(df: Union[pd.DataFrame, str], 
                   col_from: str,
                   col_to: str,
                   cols_edge_attr: Union[str, list] = None):
    '''
    由pd.DataFrame生成有向图
    
    References
    ----------
    - https://zhuanlan.zhihu.com/p/444911684
    
    Examples
    --------
    >>> df = load_df_pd('./_test/test_graph1.csv')
    # >>> df = './_test/test_graph2.xlsx'
    >>> g = gen_digraph_df(df, 'from', 'to')
    '''
    df = load_df_pd(df) if isinstance(df, str) else df
    cols_edge_attr = check_list_arg(cols_edge_attr, allow_none=True)
    if isna(cols_edge_attr):
        cols_edge_attr = [x for x in df.columns if x not in [col_from, col_to]]
    df = df[[col_from, col_to]+cols_edge_attr]
    data = df.set_index([col_from, col_to]).to_dict(orient='index')
    # data_ = []
    # for (from_, to_), edge_attrs in data.items():
    #     data_.append((from_, to_, edge_attrs))
    # g = gen_digraph_edge_list(data_)
    g = nx.DiGraph()
    for (from_, to_), edge_attrs in data.items():
        g.add_edge(from_, to_, **edge_attrs)
    return g


# namespace = globals()

# def directed_graph(Source, FromCol, ToCol, WeightCol):
    
#     # graph type
#     G1 = nx.DiGraph()
#     source = Source.reset_index(drop=True)
    
#     # load
#     for i in range(len(source)):
#         code1 = source.loc[i, FromCol]
#         code2 = source.loc[i, ToCol]
#         w     = source.loc[i, WeightCol]
#         G1.add_edge(str(code1), str(code2),weight=w)
    
#     # weight classify
#     for i in [0,20,40,60,80]:
#         ii = i / 100
#         namespace['E%d' % (i)] = [
#             (u, v) for (u, v, d) in G1.edges(df=True
#             ) if (d['weight'] >= ii)&(d['weight'] < ii + 0.2)]
    
#     # position
#     pos = nx.shell_layout(G1)
#     plt.rcParams['figure.figsize']= (10, 10)
    
#     # nodes
#     nx.draw_networkx_nodes(G1, pos, node_size=1000,alpha=0.4,
#                             node_color='dodgerblue',node_shape='o')
    
#     # lines
#     for i in [0,20,40,60,80]:
#         ii = i / 100 + 0.05
#         nx.draw_networkx_edges(G1, pos, 
#                               edgelist=namespace['E%d' % (i)],
#                             width=5,edge_color='dodgerblue', alpha=ii, 
#                             arrowstyle="->",arrowsize=50)
    
#     # texts
#     nx.draw_networkx_labels(G1, pos, font_size=25, 
#                             font_family='sans-serif', 
#                             font_color = 'k')
    
#     # show and save
#     plt.axis('off')
#     plt.savefig(WeightCol+".jpg")
#     plt.show()
    
#     return G1
    
    
# G = directed_graph(df,'from','to','weight')















