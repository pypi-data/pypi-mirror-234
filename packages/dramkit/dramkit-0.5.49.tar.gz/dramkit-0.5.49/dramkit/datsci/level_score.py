# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import logging
from beartype import beartype
from beartype.typing import List, Tuple, Union, Callable
import networkx as nx
from dramkit.iotools import load_df_pd
from dramkit.gentools import (check_l_allin_l0,
                              isna,
                              check_list_arg,
                              raise_warn,
                              raise_error,
                              link_lists)

#%%
class ScoreSystem(object):
    '''评分体系'''
    
    @beartype
    def __init__(self,
                 sys_excel_path: str,
                 logger: logging.Logger = None):
        self.sys_excel_path = sys_excel_path
        self.logger = logger
        self.load_sys()
        
    def load_sys(self):
        try:
            self.levels, self.inds_dirt = self.load_score_system(
                self.sys_excel_path)
        except:
            raise_error('ScoreSysInputError', '读取评价指标体系Excel设置失败，请检查文件内容！',
                        logger=self.logger)
    
    @staticmethod
    def load_score_system(excel_path: str) -> Tuple[List[dict], dict]:
        '''
        | 从Excel文件中读取评价指标体系
        | excel中列名顺序必须为：
        |   评价目标、一级指标、一级权重、二级指标、二级权重、三级指标、三级权重、··· 、指标方向
        |   同维度下级指标权重之和必须为1
        |   最后一列是最底层指标的方向
        '''
        df = load_df_pd(excel_path)
        dfcols = list(df.columns)
        assert len(dfcols) % 2 == 0, '按模板规则，Excel中列数量应是2的倍数！'
        
        inds, dirt = dfcols[-3], dfcols[-1]
        df[dirt] = df[dirt].apply(lambda x: x.lower().strip())
        dirt_map = {'正向': 'pos', '反向': 'neg'}
        df[dirt] = df[dirt].apply(lambda x: dirt_map[x] if x in dirt_map else x)
        assert check_l_allin_l0(df[dirt].unique(), ['pos', 'neg']), '指标方向取值必须为`pos`或`neg`！'
        inds_dirt = df.set_index(inds)[dirt].to_dict()
        
        if pd.__version__ < '2.1.0':
            df = df.fillna(method='ffill')
        else:
            df = df.ffill()
        dfcols = dfcols[:-1]
        def _gen_level(cols3):
            assert len(cols3) == 3
            res = {}
            parent = df[cols3[0]].unique()
            for p in parent:
                tmp = df[df[cols3[0]] == p][cols3[1:]]
                tmp[cols3[2]] = tmp[cols3[2]].astype(float)
                res[p] = tmp.set_index(cols3[1])[cols3[2]].to_dict()
                assert abs(sum(res[p].values()) - 1.0) <= 1e-6, '`%s`下级指标权重之和不为1！'%p
                assert all([0 <= x <= 1 for x in res[p].values()]), '权重值不能小于0或大于1！'
            return res
        levels = []
        cols3 = dfcols[:3]
        levels.append(_gen_level(cols3))
        for k in range(1, len(dfcols)-2, 2):
            cols3 = [dfcols[k]] + dfcols[k+2:k+4]
            levels.append(_gen_level(cols3))
            
        return levels, inds_dirt    
    
    @property
    def graph(self):
        g = nx.DiGraph()
        for level in self.levels:
            for parent, children in level.items():
                for child, weight in children.items():
                    g.add_edge(child, parent, weight=weight)
        for ind, dirt in self.inds_dirt.items():
            g.nodes[ind]['dirt'] = dirt
        return g

#%%
@beartype
def cal_score(df: pd.DataFrame,
              score_sys: ScoreSystem,
              val_nan: Union[str, int, float, None] = 'min',
              idcols: Union[str, list] = None,
              logger: logging.Logger = None,
              ) -> pd.DataFrame:
    '''
    | 计算综合评分
    | 注意：应保证df中所有指标值均标准化（统一量纲）且全部转为正向评价指标
    '''
    levels = score_sys.levels
    inds = link_lists([list(x.keys()) for x in levels[-1].values()])
    if not all([x in df.columns for x in inds]):
        raise_error('DataError', 'df须包含评价体系中的所有最底层指标！', logger=logger)
    df = df.copy()
    if (df[inds]==np.inf).sum().sum() > 0 or \
       (df[inds]==-np.inf).sum().sum() > 0:
        raise_warn('DataInfWarn', '数据中存在无穷值。', logger=logger)
    if df[inds].isna().sum().sum() > 0:
        if isinstance(val_nan, (int, float)):
            raise_warn('DataNaNWarn', '数据中无效值将被填充为%s。'%val_nan, logger=logger)
            for ind in inds:
                df[ind] = df[ind].fillna(val_nan)
        elif isinstance(val_nan, str):
            val_nan = val_nan.lower()
            if not (val_nan in ['min', 'max', 'mean', 'median'] \
                    or val_nan.startswith('quantile_')):
                raise_error(
                    'ValueError',
                    '`val_nan`只能为：`min`, `max`, `mean`, `median`或`quantile_x(x为分位点)`！',
                    logger=logger)
            raise_warn('DataNaNWarn', '数据中无效值将按`%s`处理。'%val_nan)
            for ind in inds:
                if val_nan in ['min', 'max', 'mean', 'median']:
                    fillval = eval('df[ind].%s()'%val_nan)
                else:
                    fillval = eval('df[ind].quantile(%s)'%float(val_nan.replace('quantile_', '')))
                df[ind] = df[ind].fillna(fillval)
        else:
            raise_warn('DataNaNWarn', '数据中发现无效值。', logger=logger)
    idcols = check_list_arg(idcols, allow_none=True)
    if isna(idcols):
        idcols = []
    else:
        if df[idcols].isna().sum().sum() > 0:
            raise_warn('DataIdNaNWarn', '数据标识列发现无效值。', logger=logger)
    res = df[idcols+inds].copy()
    cols_ = []
    for level in levels[::-1]:
        for p, chlds in level.items():
            cols_.append(p)
            res[p] = eval('+'.join(['res["%s"]*%s'%(c, w) 
                     for c, w in chlds.items()]))
    res = res[idcols+cols_[::-1]]
    return res

#%%
def get_quantiles(dirt, series, logger=None, **kw_rank):
    '''计算百分位数'''
    if not dirt in ['pos', 'neg']:
        raise_error('ValueError', '指标方向取值必须为`pos`或`neg`！', logger=logger)
    series = pd.Series(series)
    if len(series) < 3:
        raise_warn('DataTooLessWarn', '数据量小于3条！', logger=logger)
    if 'method' in kw_rank:
        method = kw_rank.pop('method')
    else:
        method = 'dense'
    if 'ascending' in kw_rank:
        kw_rank.pop('ascending')
    ascending = True if dirt == 'pos' else False
    # res = series.rank(method=method, pct=True,
    #                   ascending=ascending, **kw_rank)
    res = series.rank(method=method, pct=False,
                      ascending=ascending, **kw_rank)
    res = res - 1
    res = res / res.max()
    return res


def inds_normal(df: pd.DataFrame,
                score_sys: ScoreSystem,
                group_cols: Union[str, list, tuple] = None,
                func_norm: Union[bool, None, Callable] = None,
                kw_norm: dict = {},
                logger: logging.Logger = None):
    '''
    | 指标标准化（统一量纲）
    | func_norm形式须为func_norm(dirt, series, **kw_norm)
    '''
    group_cols = check_list_arg(group_cols, allow_none=True)
    if (not isna(group_cols)) and (df[group_cols].isna().sum().sum() > 0):
        raise_error('DataNaNError', '分组列不能有无效值！', logger=logger)
    if isna(func_norm):
        func_norm = get_quantiles
    if not func_norm:
        return df
    else:
        inds_dirt = score_sys.inds_dirt
        inds = list(inds_dirt.keys())
        res = df.copy()
        if res[inds].isna().sum().sum() > 0:
            raise_warn('DataNaNWarn', '数据中发现无效值。', logger=logger)
        if (res[inds]==np.inf).sum().sum() > 0 or \
           (res[inds]==-np.inf).sum().sum() > 0:
            raise_warn('DataInfWarn', '数据中存在无穷值。', logger=logger)
        if not isna(group_cols):
            n_ids = res[group_cols].drop_duplicates().shape[0]
        for ind, dirt in inds_dirt.items():
            if isna(group_cols) or n_ids == 1:
                res[ind] = func_norm(dirt, res[ind], **kw_norm)
            else:
                res[ind] = res.groupby(group_cols, as_index=False, group_keys=False)[ind].apply(
                    lambda x: func_norm(dirt, x, logger=logger, **kw_norm))
        return res
    
    
    
    
    
    
    
    
    
    
    