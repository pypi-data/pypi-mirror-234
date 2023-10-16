# -*- coding: utf-8 -*-

from beartype.typing import Literal, NewType, Union

import numpy as np
import pandas as pd
from beartype import beartype
from beartype.typing import List
from joblib import Parallel, delayed

from dramkit.datsci.lr import lr_smf_df
from dramkit.gentools import (check_list_arg,
                              isna,
                              raise_warn,
                              raise_error)
from dramkit.const import WIN_SYS


def _get_new_literal_type(name, l):
    return NewType(name, eval('Literal[{}]'.format(', '.join(["'%s'"%x for x in l]))))

# 允许的模型评价指标
CRITERIA = ['bic', 'aic', 'r2', 'r2_adj', 'fvalue', 'mse']
CRI_ALIAS = {'r2': 'rsquared', 'r2_adj': 'rsquared_adj', 'mse': 'mse_resid'}
CriterionType = _get_new_literal_type('CriterionType',
                                      CRITERIA+list(CRI_ALIAS.values()))
SMALL_BETTER = ['bic', 'aic', 'mse_resid']
LARGE_BETTER = ['rsquared', 'rsquared_adj', 'fvalue']

# 允许的变量筛选方法
METHODS = ['backward', 'forward', 'both']
MethodType = _get_new_literal_type('MethodType', METHODS)


def joblib_parl(func, args_list, n_jobs, backend='loky',
                **kw_jb):
    jb = Parallel(n_jobs=n_jobs, backend=backend, **kw_jb)
    res = jb(delayed(func)(*args) for args in args_list)
    return res


def _fit_new(df, ycol, x_olds, x_new, intercept,
             criterion, add_or_del):
    '''增加或减少单个自变量，模型拟合'''
    assert add_or_del in ['add', 'del'], '`add_or_del`必须为`add`或`del`！'
    if add_or_del == 'add':
        x_mdl = list(x_olds) + [x_new]
    elif add_or_del == 'del':
        x_mdl = set(x_olds) - set([x_new])
    mdl = lr_smf_df(df, ycol, xcols=x_mdl, intercept=intercept)
    score = eval('mdl.'+criterion)
    return score, x_new, mdl


@beartype
def stepreg(df: pd.DataFrame,
            ycol: str,
            xcols: Union[str, List[str], None] = None,
            xcols_fixed: Union[List[str], str, None] = None,
            intercept: bool = True,
            criterion: CriterionType = 'bic',
            cri_tol_in: Union[float, int] = 0.0,
            cri_tol_out: Union[float, int] = 0.0,
            x_pvalue_out: float = 0.05,
            back_out_with_pvalue: bool = False,
            nx_min: Union[int, None] = None,
            nx_max: Union[int, None] = None,
            method: MethodType = 'both',
            max_iter: Union[int, None] = None,
            n_jobs: int = 1,
            jb_backend: str = 'threading',
            kw_jb: dict = {},
            **kwargs):

    '''
    逐步回归

    Parameters
    ----------
    df : pd.Dataframe
        回归用数据
    ycol : str
        回归分析因变量列名
    xcols : list, None
        指定自变量X的列名范围，不指定则默认为除ycol之外的所有列
    xcols_fixed : list, None
        回归模型中必须包含的自变量列名
    intercept : bool
        模型是否有截距项，默认有
    criterion : str
        模型优化评价标准指标，可选'bic', 'aic', 'r2', 'r2_adj', 'fvalue', 'mse'
    cri_tol_in : float
        | 准入时模型评价指标变化量阈值（应大于等于0）
        | 对于越小越好的指标，旧值-新值>cri_tol_in，则准入
        | 对于越大越好的指标，新值-旧值>cir_tol_in，则准入
    cri_tol_out : float
        | 准出时模型评价指标变化量阈值（应大于等于0）
        | 对于越小越好的指标，旧值-新值>cri_tol_out，则准出
        | 对于越大越好的指标，新值-旧值>cir_tol_out，则准出
    x_pvalue_out : float
        当设置`method`=`both`时，移除变量的pvalue阈值
    back_out_with_pvalue : bool
        当`method`=`backward`时，移除变量是否控制p值大于`x_pvalue_out`才移除，默认不控制
    nx_min : int, None
        纳入模型的自变量个数下限，默认0
    nx_max : int, None
        纳入模型的自变量个数上限，默认等于xcols的个数
    method : str
        逐步回归筛选变量过程方法，可选'backward', 'forward', 'both'
    max_iter : int, None
        最大迭代轮数
    n_jobs : int
        | joblib参数n_jobs，若为0则不适用joblib，直接用循环
        | 在自变量不是很多的情况下，不使用并行反而更快
    jb_backend : str
        | joblib参数backend
        | 除非要筛选的自变量特别多，否则不要用multiprocessing
    kw_jb: dict
        joblib接收的关键字参数
        
    Returns
    -------
    picks : list
        最终筛选保留的变量
    final_mdl : statsmodels.regression.linear_model
        最终线性回归模型
    step_data : pd.DataFrame
        迭代过程数据
    
    Note
    ----
    准入准出条件判断优先顺序：自变量个数限制 > 评价指标阈值条件&评价指标变化量阈值条件

    References
    ----------
    - https://www.cnblogs.com/lantingg/p/9535010.html
    - https://www.jianshu.com/p/bb1c6c319d9b
    '''
    
    if WIN_SYS and jb_backend == 'multiprocessing':
        raise_warn('WinMultiProcNotWarn', 'windows下使用多进程速度很慢很慢！', **kwargs)
        
    # 模型评价指标名称统一
    if criterion in CRI_ALIAS:
        criterion = CRI_ALIAS[criterion]
      
    def _get_mdl_info(mdl):
        mdl_info = {'fvalue': mdl.fvalue,
                    'f_pvalue': mdl.f_pvalue,
                    'r2': mdl.rsquared,
                    'r2_adj': mdl.rsquared_adj}
        return mdl_info
        
    def _is_better(cri_old, cri_new, add_or_del):
        '''判断cri_new是否比cri_old更优'''
        assert add_or_del in ['add', 'del'], '`add_or_del`必须为`add`或`del`！'
        if add_or_del == 'add':
            if criterion in SMALL_BETTER:
                return cri_old-cri_new > cri_tol_in
            else:
                return cri_new-cri_old > cri_tol_in
        else:
            if criterion in SMALL_BETTER:
                return cri_old-cri_new > cri_tol_out
            else:
                return cri_new-cri_old > cri_tol_out
    
    # 自变量可选范围
    xcols = check_list_arg(xcols, allow_none=True)
    xcols = [c for c in df.columns if c != ycol] if isna(xcols) else xcols
    
    # 无穷值检查
    if (df[xcols+[ycol]] == np.inf).sum().sum() > 0 or \
       (df[xcols+[ycol]] == -np.inf).sum().sum() > 0:
        raise_error('DataInfError', '数据中有无穷值！', **kwargs)
    
    # 有效样本量检查
    notna = (~df[xcols+[ycol]].isna()).sum(axis=1)
    notna = notna[notna == len(xcols+[ycol])]
    if len(notna) < len(xcols):
        raise_warn('DataTooLessWran', '数据完整的样本数量小于自变量个数！', **kwargs)
        
    # 无效值检查
    if df[xcols+[ycol]].isna().sum().sum() > 0:
        raise_warn('DataNaNWarning', '数据中存在无效值。', **kwargs)
    
    # 最大迭代轮数
    if isna(max_iter):
        max_iter = sum(range(1, len(xcols)+1))
    
    # 必选自变量
    xcols_fixed = check_list_arg(xcols_fixed, allow_none=True)
    xcols_fixed = [] if isna(xcols_fixed) else xcols_fixed
    
    # 自变量个数控制
    nx_min = 0 if isna(nx_min) else nx_min
    nx_max = len(xcols) if isna(nx_max) else nx_max
    assert nx_min <= nx_max, '自变量最小控制个数不能大于最大个数！'
    
    # 若必须全选，则直接返回全部变量回归模型
    if nx_min >= len(xcols):
        final_mdl = lr_smf_df(df, ycol, xcols=xcols, intercept=intercept)
        final_cri = eval('final_mdl.'+criterion)
        pvalues = final_mdl.pvalues.to_dict()
        params = final_mdl.params.to_dict()
        mdl_info = _get_mdl_info(final_mdl)
        step_data = [(final_cri, # 评价指标值
                      xcols, # 保留的变量列表
                      params, # 保留的变量系数
                      pvalues, # 变量P值,
                      mdl_info,
                      ('add', xcols)) # 变量筛选动作
                     ]
        step_data = pd.DataFrame(
                        step_data,
                        columns=[criterion, 'picks', 'param', 'pvalue', 'model_info', 'change'])
        return xcols, final_mdl, step_data
    
    if method in ['forward', 'both']:
        picks = xcols_fixed.copy()
        lefts = [x for x in xcols if x not in picks+[ycol]]
    else:
        picks = [x for x in xcols if x != ycol]
        lefts = [x for x in picks if x not in xcols_fixed]
      
    # 初始化评价指标值
    if picks:
        final_mdl = lr_smf_df(df, ycol, xcols=picks, intercept=intercept)
        final_cri = eval('final_mdl.'+criterion)
        cur_cri = final_cri
        pvalues = final_mdl.pvalues.to_dict()
        mdl_info = _get_mdl_info(final_mdl)
        params = final_mdl.params.to_dict()
        if (method == 'backward') and back_out_with_pvalue:
            lefts = [x for x in lefts if final_mdl.pvalues[x] > x_pvalue_out]
    else:
        if criterion in SMALL_BETTER:
            final_cri, cur_cri = np.inf, np.inf
        else:
            final_cri, cur_cri = -np.inf, -np.inf
        pvalues = {}
        mdl_info = {}
        params = {}
    need_imprv = True
    # 存放过程数据
    step_data = [(final_cri, # 评价指标值
                  picks.copy(), # 保留的变量列表
                  params, # 保留的变量系数
                  pvalues, # 变量P值
                  mdl_info,
                  () if len(picks) == 0 else ('add', picks.copy())) # 变量筛选动作
                 ]
    
    def _joblib_parl_reg(args_list):
        if n_jobs == 0:
            cri_xnew = [_fit_new(*args) for args in args_list]
        else:
            cri_xnew = joblib_parl(_fit_new, args_list, n_jobs, backend=jb_backend, **kw_jb)
        cri_xnew.sort(key=lambda x: x[0])
        return cri_xnew
    
    # 逐步准入
    if method in ['forward', 'both']:
        i = 0
        while lefts and need_imprv and i < max_iter:
            args_list = [[df, ycol, picks, new, intercept, criterion, 'add'] for new in lefts]
            cri_xnew = _joblib_parl_reg(args_list)
            if criterion in SMALL_BETTER:
                cur_cri, xbest, cur_mdl = cri_xnew[0]
            else:
                cur_cri, xbest, cur_mdl = cri_xnew[-1]
            better = _is_better(final_cri, cur_cri, 'add')
            if (len(picks) < nx_min) or \
               (len(picks) < nx_max and better):
                final_cri, final_mdl = cur_cri, cur_mdl
                picks.append(xbest)
                lefts.remove(xbest)
                mdl_info = _get_mdl_info(final_mdl)
                step_data.append((final_cri, picks.copy(),
                                  final_mdl.params.to_dict(),
                                  final_mdl.pvalues.to_dict(),
                                  mdl_info,
                                  ('add', [xbest])))
            else:
                need_imprv = False
                
            # 准入后剔除不显著变量
            if method == 'both':
                n_picks = len(picks)
                n_can_del = n_picks - nx_min
                if n_can_del > 0:
                    if intercept:
                        may_dels = final_mdl.pvalues.iloc[1:].copy()
                    else:
                        may_dels = final_mdl.pvalues.copy()
                    may_dels = may_dels.sort_values(ascending=False)
                    may_dels = may_dels[may_dels > x_pvalue_out]
                    to_dels = may_dels.index.tolist()[:n_can_del]
                    if len(to_dels) > 0:
                        for xcol in to_dels:
                            picks.remove(xcol)
                        if (not intercept) and (len(picks) == 0):
                            final_mdl = None
                            final_cri = np.inf if criterion in SMALL_BETTER else -np.inf
                            step_data.append((final_cri, picks.copy(),
                                              {}, {}, {},
                                              ('del', to_dels)))
                        else:
                            final_mdl = lr_smf_df(df, ycol, xcols=picks, intercept=intercept)
                            final_cri = eval('final_mdl.'+criterion)
                            mdl_info = _get_mdl_info(final_mdl)
                            step_data.append((final_cri, picks.copy(),
                                              final_mdl.params.to_dict(),
                                              final_mdl.pvalues.to_dict(),
                                              mdl_info,
                                              ('del', to_dels)))
                    
            i += 1
    
    # 逐步准出
    elif method == 'backward':
        i = 0
        while lefts and need_imprv and i < max_iter:
            args_list = [[df, ycol, picks, new, intercept, criterion, 'del'] for new in lefts]
            if (not intercept) and (picks == lefts) and (len(lefts) == 1):
                need_imprv = False
                if final_mdl.pvalues[lefts[0]] > x_pvalue_out:
                    final_mdl = None
                    final_cri = np.inf if criterion in SMALL_BETTER else -np.inf
                    picks = []
                    step_data.append((final_cri, picks.copy(),
                                      {}, {}, {},
                                      ('del', lefts)))
                    lefts = []
            else:
                cri_xnew = _joblib_parl_reg(args_list)
                if criterion in SMALL_BETTER:
                    cur_cri, xworst, cur_mdl = cri_xnew[0]
                else:
                    cur_cri, xworst, cur_mdl = cri_xnew[-1]
                better = _is_better(final_cri, cur_cri, 'del')
                if (len(picks) > nx_max) or \
                   (len(picks) > nx_min and better):
                    final_cri, final_mdl = cur_cri, cur_mdl
                    picks.remove(xworst)
                    lefts.remove(xworst)
                    mdl_info = _get_mdl_info(final_mdl)
                    step_data.append((final_cri, picks.copy(),
                                      final_mdl.params.to_dict(),
                                      final_mdl.pvalues.to_dict(),
                                      mdl_info,
                                      ('del', [xworst])))
                    if back_out_with_pvalue:
                        lefts = [x for x in lefts if final_mdl.pvalues[x] > x_pvalue_out]
                else:
                    need_imprv = False
            i += 1
    
    step_data = pd.DataFrame(
                    step_data,
                    columns=[criterion, 'picks', 'param', 'pvalue', 'model_info', 'change'])
    
    return picks, final_mdl, step_data


if __name__ == '__main__':
    import sklearn.datasets as datasets
    from dramkit import TimeRecoder
    
    # '''
    data = datasets.load_diabetes()
    xcols, y = data['feature_names'], data['target']
    df = pd.DataFrame(data['data'], columns=xcols)
    df['y'] = y


    ycol = 'y'
    xcols = None
    # xcols = [x for x in df.columns if x != ycol]
    xcols_fixed = None
    intercept = True
    criterion = 'bic'
    # criterion = 'rsquared'
    # criterion = 'r2'
    # criterion = 'r2_adj'
    # criterion = 'rsquared_adj'
    cri_tol_in = 0.0
    cri_tol_out = 0.0
    x_pvalue_out = 0.05
    back_out_with_pvalue = False
    nx_min = None
    # nx_min = 5
    # nx_min = df.shape[1]-1
    nx_max = None
    # method = 'forward'
    # method = 'both'
    method = 'backward'
    max_iter = None
    # max_iter = 2
    n_jobs = 0
    # n_jobs = 1
    jb_backend = 'threading'
    # jb_backend = 'loky'
    # jb_backend = 'multiprocessing'
    kw_jb = {}
    kwargs = {}
    # '''
    
    # # df = df.iloc[:4, :]
    # df.iloc[:2, :] = np.nan
    
    args = [df,
            ycol,
            xcols,
            xcols_fixed,
            intercept,
            criterion,
            cri_tol_in,
            cri_tol_out,
            x_pvalue_out,
            back_out_with_pvalue,
            nx_min,
            nx_max,
            method,            
            max_iter,
            n_jobs,
            jb_backend
            ]
    n = 100
    
    df = pd.concat([df]*5, axis=0)

    # '''
    tr = TimeRecoder()
    final_xcols, final_mdl, step_data = \
          stepreg(*args)
    print(final_xcols)

    tr.used()
    # '''

    '''
    from dramkit.gentools import func_runtime_test
    def test():
        t, res = func_runtime_test(
                          stepreg,
                          n=n,
                          return_all=True,
                          df=df,
                          ycol=ycol,
                          intercept=intercept,
                          criterion=criterion,
                          cri_tol_in=cri_tol_in,
                          cri_tol_out=cri_tol_out,
                          x_pvalue_out=x_pvalue_out,
                          nx_min=nx_min,
                          nx_max=nx_max,
                          method=method,
                          max_iter=max_iter,
                          n_jobs=n_jobs,
                          # jb_backend = 'loky'
                          jb_backend=jb_backend
                          )
        return t, res

    t, res = test()
    final_xcols, final_mdl, step_data = res[0]
    print(final_xcols)
    # '''
    
    '''
    tr = TimeRecoder()
    from dramkit.speedup.multi_thread import multi_thread_threading
    res = multi_thread_threading(stepreg,
                                 [args for _ in range(n)],
                                 # multi_line=5
                                 )
    tr.used()
    # '''
    
    '''
    tr = TimeRecoder()
    from dramkit.speedup.multi_thread import multi_thread_concurrent
    res = multi_thread_concurrent(stepreg,
                                  [args for _ in range(n)],
                                  multi_line=2
                                  )
    print(res[0][0])
    tr.used()
    # '''
    
    '''
    import multiprocessing
    tr = TimeRecoder()
    pool = multiprocessing.Pool(processes=5)
    for i in range(n):
        exec('task_%s = pool.apply_async(stepreg, args=args)'%i)
    pool.close()
    pool.join()
    results = [eval('task_%s.get()'%i) for i in range(n)]
    print(results[0][0])
    tr.used()
    # '''
    
    '''
    from dramkit.speedup.multi_process_concurrent import multi_process_concurrent
    tr = TimeRecoder()
    res = multi_process_concurrent(stepreg,
                                   [args for _ in range(n)],
                                   multi_line=5,
                                   keep_order=False)
    print(res[0][0])
    tr.used()
    # '''



