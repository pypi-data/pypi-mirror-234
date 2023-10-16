# -*- coding: utf-8 -*-

import math
from tqdm import tqdm
from beartype.typing import Callable

import numpy as np
import pandas as pd

from scipy.stats import norm, lognorm, weibull_min, kstest
from scipy.stats import t, f, chi2

from statsmodels.tools.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.linear_model import LinearRegression as lr

from dramkit.gentools import isnull
from dramkit.sorts.insert_sort import rank_of_insert
from dramkit.sorts.insert_sort_bin import rank_of_insert_bin


def fpdf(x, df1, df2, loc=0, scale=1):
    '''
    | 计算符合自由度为df1和df2的F分布的随机变量取x时的概率密度函数值
    | loc和scale为scipy.stats中f分布参数
    '''
    p = f(df1, df2, loc=loc, scale=scale).pdf(x)
    return p


def fcdf(x, df1, df2, loc=0, scale=1):
    '''
    | 计算符合自由度为df1和df2的F分布的随机变量取x时的概率分布函数值
    | loc和scale为scipy.stats中f分布参数
    '''
    p = f(df1, df2, loc=loc, scale=scale).cdf(x)
    return p


def ffit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行F分布参数估计
    | 返回顺序: df1, df2, loc, scale
    '''
    df1, df2, loc, scale = f.fit(series)
    return df1, df2, loc, scale


def fit_f_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个F分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    df1, df2, loc, scale = ffit(series)
    return fpdf(x, df1, df2, loc, scale)


def fit_f_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个F分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    df1, df2, loc, scale = ffit(series)
    return fcdf(x, df1, df2, loc, scale)


def ftest(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行F分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (df1, df2, loc, scale)
    '''
    df1, df2, loc, scale = f.fit(series)
    Stat, P = kstest(series, 'f', args=(df1, df2, loc, scale))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'f': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (df1, df2, loc, scale)


def tpdf(x, df, loc=0, scale=1):
    '''
    | 计算符合自由度为df的T分布的随机变量取x时的概率密度函数值
    | loc和scale为scipy.stats中t分布参数
    '''
    # if loc == 0 and scale == 1:
    #     p = math.gamma((df+1)/2) / (math.gamma(df/2) * math.sqrt(df*np.pi)) * \
    #         math.pow(1+math.pow(x, 2)/df, -(df+1)/2)
    p = t(df, loc=loc, scale=scale).pdf(x)
    return p


def tcdf(x, df, loc=0, scale=1):
    '''
    | 计算符合自由度为df的T分布的随机变量取x时的概率分布函数值
    | loc和scale为scipy.stats中t分布参数
    '''
    p = t(df, loc=loc, scale=scale).cdf(x)
    return p


def tfit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行T分布参数估计
    | 返回顺序: df, loc, scale
    '''
    df, loc, scale = t.fit(series)
    return df, loc, scale


def fit_t_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个T分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    df, loc, scale = tfit(series)
    return tpdf(x, df, loc, scale)


def fit_t_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个T分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    df, loc, scale = tfit(series)
    return tcdf(x, df, loc, scale)


def ttest(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行T分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (df, loc, scale)
    '''
    df, loc, scale = t.fit(series)
    Stat, P = kstest(series, 't', args=(df, loc, scale))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'t': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (df, loc, scale)


def chi2pdf(x, df, loc=0, scale=1):
    '''
    | 计算符合自由度为df的卡方分布的随机变量取x时的概率密度函数值
    | loc和scale为scipy.stats中卡方分布参数
    '''
    p = chi2(df, loc=loc, scale=scale).pdf(x)
    return p


def chi2cdf(x, df, loc=0, scale=1):
    '''
    | 计算符合自由度为df的卡方分布的随机变量取x时的概率分布函数值
    | loc和scale为scipy.stats中卡方分布参数
    '''
    p = chi2(df, loc=loc, scale=scale).cdf(x)
    return p


def chi2fit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行卡方分布参数估计
    | 返回顺序: df, loc, scale
    '''
    df, loc, scale = chi2.fit(series)
    return df, loc, scale


def fit_chi2_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个卡方分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    df, loc, scale = chi2fit(series)
    return chi2pdf(x, df, loc, scale)


def fit_chi2_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个卡方分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    df, loc, scale = chi2fit(series)
    return chi2cdf(x, df, loc, scale)


def chi2test(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行卡方分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (df, loc, scale)
    '''
    df, loc, scale = chi2.fit(series)
    Stat, P = kstest(series, 'chi2', args=(df, loc, scale))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'chi2': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (df, loc, scale)


def normpdf(mu, sigma, x):
    '''计算符合正态分布N(mu, sigma)的随机变量取x时的概率密度函数值'''
    p = norm(mu, sigma).pdf(x)
    # p = np.exp(-((x - mu)**2)/(2*sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return p


def normcdf(mu, sigma, x):
    '''计算符合正态分布N(mu, sigma)的随机变量取x时的概率密分布数值'''
    p = norm(mu, sigma).cdf(x)
    return p


def normfit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行正态分布参数估计
    | 返回顺序: mu, sigma
    '''
    # mu = series.mean()
    # sigma = series.std(ddof=0)
    mu, sigma = norm.fit(series)
    return mu, sigma


def fit_norm_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个正态分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    mu, sigma = normfit(series)
    return normpdf(mu, sigma, x)


def fit_norm_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个正态分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    mu, sigma = normfit(series)
    return normcdf(mu, sigma, x)


def normtest(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行正态分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (mu, sigma)
    '''
    mu, sigma = normfit(series)
    Stat, P = kstest(series, 'norm', args=(mu, sigma))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'norm': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (mu, sigma)


def lognormpdf(mu, sigma, x):
    '''计算符合参数为mu, sigma的对数正态分布的随机变量取x时的概率密度函数值'''
    p = lognorm(s=sigma, loc=0, scale=np.exp(mu)).pdf(x)
    # p = np.exp(-((np.log(x) - mu)**2)/(2 * sigma**2)) / \
    #     (x * sigma * np.sqrt(2*np.pi))
    return p


def lognormcdf(mu, sigma, x):
    '''计算符合参数为mu, sigma的对数正态分布的随机变量取x时的概率分布函数值'''
    p = lognorm(s=sigma, loc=0, scale=np.exp(mu)).cdf(x)
    return p


def lognormfit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行对数正态分布参数估计
    | 返回顺序: mu, sigma
    
    .. hint::
        | scipy.stats中lognorm分布参数估计和 :func:`lognormpdf` 中参数关系：
        | 若设置floc=0（即始终loc=0），则有s = sigma，scale = e ^ mu
    '''

    # mu = np.log(series).mean()
    # sigma = np.log(series).std(ddof=0)

    s, loc, scale = lognorm.fit(series, floc=0)
    sigma, mu = s, np.log(scale)

    return mu, sigma


def fit_lognorm_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个对数正态分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    mu, sigma = lognormfit(series)
    return lognormpdf(mu, sigma, x)


def fit_lognorm_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个对数正态分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    mu, sigma = lognormfit(series)
    return lognormcdf(mu, sigma, x)


def lognormtest(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行对数正态分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (mu, sigma)
    '''
    mu, sigma = lognormfit(series)
    s, loc, scale = sigma, 0, np.exp(mu)
    Stat, P = kstest(series, 'lognorm', args=(s, loc, scale))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'lognorm': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (mu, sigma)


def weibullpdf(k, lmd, x):
    '''计算符合参数为k, lmd的威布尔分布的随机变量取x时的概率密度函数值'''
    p = weibull_min(c=k, loc=0, scale=lmd).pdf(x)
    # p = (k/lmd) * (x/lmd)**(k-1) * np.exp(-(x/lmd)**k)
    return p


def weibullcdf(k, lmd, x):
    '''计算符合参数为k, lmd的威布尔分布的随机变量取x时的概率分布函数值'''
    p = weibull_min(c=k, loc=0, scale=lmd).cdf(x)
    return p


def weibullfit(series):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行威布尔分布参数估计
    | 返回顺序: k, lmd
    
    .. hint::
        | scipy.stats中weibull_min分布参数估计和 :func:`weibullpdf` 中
          weibull分布参数关系：
        | 若设置floc=0（即始终loc=0），则有c = k，scale = lmd
        | scipy.stats中weibull_min分布参数估计和 ``np.random.weibull``
          分布参数关系：
        | 若设置floc=0（即始终loc=0），则有c = a，scale = 1
    '''

    c, loc, scale = weibull_min.fit(series, floc=0)
    k, lmd = c, scale

    return k, lmd


def fit_weibull_pdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个威布尔分布，
    | 并计算随机变量在该分布下取值为x时的概率密度函数值
    '''
    k, lmd = weibullfit(series)
    return weibullpdf(k, lmd, x)


def fit_weibull_cdf(series, x):
    '''
    | 用series (`pd.Series` 或 `np.array`)拟合一个威布尔分布，
    | 并计算随机变量在该分布下取值为x时的概率分布函数值
    '''
    k, lmd = weibullfit(series)
    return weibullcdf(k, lmd, x)


def weibulltest(series, plot=False, **kwargs_plot):
    '''
    | 对series (`pd.Series` 或 `np.array`)进行威布尔分布检验(采用KS检验)
    | 返回顺序: (统计量, P值), (k, lmd)
    '''
    k, lmd = weibullfit(series)
    c, loc, scale = k, 0, lmd
    Stat, P = kstest(np.log(series), 'weibull_min', args=(c, loc, scale))
    if plot:
        from dramkit.plottools.plot_histdist import plot_histdist
        plot_histdist(series, dists={'weibull': ('-r', None)}, **kwargs_plot)
    return (Stat, P), (k, lmd)


def mc_important_sample(smp_gener: Callable,
                        gener_pdf: Callable,
                        tgt_func: Callable,
                        tgt_pdf: Callable = None,
                        n_mc: int = 100000,
                        cumsum: bool = False):
    '''
    | 重要性采样
    | https://zhuanlan.zhihu.com/p/250282313
    | https://zhuanlan.zhihu.com/p/629016302
    | https://zhuanlan.zhihu.com/p/258384070
    | https://zhuanlan.zhihu.com/p/259389498
    | https://blog.csdn.net/bigheadyushan/article/details/80623249
    | https://zhuanlan.zhihu.com/p/41217212
    | https://www.jianshu.com/p/5648c7321868
    
    TODO
    ----
    加权重要性采样？
    
    Parameters
    ----------
    smp_gener : Callable
        采样器，用于根据给定的概率分布生成样本，调用方式为smps = smp_gener(n_mc)
    gener_pdf : Callable
        采样器采样用的分布的概率密度函数，必须保证在采样范围内该函数积分为1（符合概率分布函数特征）
    tgt_func : Callable
        目标函数，调用方式为tgts = tgt_func(smps)
    tgt_pdf : Callable
        目标变量真实分布的概率密度函数，若是已知的，可以设置
    n_mc : int
        采样数量 
    cumsum : bool
        若为True, 则对采样样本累计进行蒙特卡洛估计，即返回收敛过程
        
    Returns
    --------
    mc_res : np.ndarray
        蒙特卡洛估计结果
    smps : np.ndarray
        采样取得的样本
        
    Examples
    --------
    >>> # 估计y=4-x^2在[-2, 2]区间上的面积（真实值为32/3=10.6666...）
    >>> # 用均匀分布采样:
    >>> n_mc = 10000
    >>> smp_gener = lambda n: np.random.uniform(-2, 2, n)
    >>> gener_pdf = lambda x: 1 / 4
    >>> tgt_func = lambda x: 4 - x**2
    >>> print(mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc))
    10.672217965691754
    >>> from dramkit import plot_series
    >>> df = pd.DataFrame({'v_u': mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc, cumsum=True)})
    >>> plot_series(df, {'v_u': None}, figsize=(8, 5))
    >>> # 用标准正态分布采样：
    >>> smp_gener = lambda n: np.clip(np.random.randn(n), -2, 2)
    >>> gener_pdf = lambda x: normpdf(0, 1, x)
    >>> print(mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc))
    10.667448905107554
    >>> df['v_n'] = mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc, cumsum=True)
    >>> plot_series(df, {'v_u': ('-b', None), 'v_n': '-r'}, figsize=(8, 5))
    >>> # 用概率密度函数为f=(4-x^2)/(32/3)的分布（即使将tgt_func按概率积分为1进行了缩放）进行采样:
    >>> C = 32/3
    >>> # C = 16/3
    >>> # 均匀分布和其他分布转化，参考：
    >>> # https://blog.csdn.net/Hoooo_233/article/details/107010480
    >>> # Python求反函数，参考：https://blog.csdn.net/jacke121/article/details/120493603
    >>> tgt_cdf = lambda x: (4*x - (x**3)/3) / C
    >>> from pynverse import inversefunc
    >>> invtrans_func = lambda p: inversefunc(tgt_cdf, y_values=p, domain=[-2, 2])
    >>> smp_gener = lambda n: invtrans_func(np.random.uniform(-0.5, 0.5, n))
    >>> gener_pdf = lambda x: (4-x**2) / C
    >>> print(mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc))
    10.666666666666664
    >>> df['v_self'] = mc_important_sample(smp_gener, gener_pdf, tgt_func, n_mc=n_mc, cumsum=True)
    >>> plot_series(df, {'v_u': '-b', 'v_n': '-r', 'v_self': '-g'}, figsize=(8, 5))
    '''
    smps = smp_gener(n_mc)
    gen_pdf = gener_pdf(smps)
    tgt_pdf = tgt_pdf(smps) if not isnull(tgt_pdf) else 1.0
    weights = tgt_pdf / gen_pdf
    tgts = tgt_func(smps) * weights
    if not cumsum:
        mc_res = np.sum(tgts) / float(n_mc)
    else:
        mc_res = np.cumsum(tgts) / np.arange(1, n_mc+1)
    return mc_res


def get_at_range_prob_norm(mu, sigma, low, high):
    '''获取正态分布N(mu,sigma)取值范围在low和high之间的概率'''
    # 计算标准化的z_score值
    z_low = (low - mu) / sigma
    z_high = (high - mu) / sigma
    # 计算在z-score范围内的概率
    prob = norm.cdf(z_high) - norm.cdf(z_low)
    return prob


def mse(y_true, y_predict):
    '''
    计算均方误差MSE

    Parameters
    ----------
    y_true : np.array, pd.Series
        真实值
    y_predict : np.array, pd.Series
        预测值


    :returns: `float` - MSE值
    '''
    if y_predict.shape != y_true.shape:
        raise ValueError('y_true和y_predict的值必须一一对应！')
    yTrue = pd.Series(y_true).reset_index(drop=True)
    yPred = pd.Series(y_predict).reset_index(drop=True)
    return ((yTrue - yPred) ** 2).mean()


def r2(y_true, y_predict, is_linear=False):
    '''
    计算拟合优度R^2
    
    Parameters
    ----------
    y_true : np.array, pd.Series
        真实值
    y_predict : np.array, pd.Series
        预测值
    is_linear : bool
        预测值是否为线性回归结果


    :returns: `float` - R^2值

    .. hint:: 
        | 在线性回归情况下（y_predict是由y_true与自变量X进行线性拟合的预测值），有:
        |   R2 = 1 - SSres / SStot = SSreg / SStot，
        |   且此时R2与y_true和y_predict相关系数的平方相等
        | 非线性回归情况下，1 - SSres / SStot != SSreg / SStot，R2与两者相关系数平方也不相等
        | 可设置is_linear为True和False进行比较验证
    
    References
    ----------
    https://blog.csdn.net/wade1203/article/details/98477034
    https://blog.csdn.net/liangyihuai/article/details/88560859
    https://wenku.baidu.com/view/893b22d66bec0975f465e2b8.html
    '''
    if y_predict.shape != y_true.shape:
        raise ValueError('y_true和y_predict的值必须一一对应！')
    yTrue = pd.Series(y_true).reset_index(drop=True)
    yPred = pd.Series(y_predict).reset_index(drop=True)
    SStot = sum((yTrue - yTrue.mean()) ** 2)
    if not is_linear:
        SSres = sum((yTrue - yPred) ** 2)
        return 1 - SSres / SStot
    else:
        SSreg = sum((yPred - yTrue.mean()) ** 2)
        return SSreg / SStot


def r2adj(y_true, y_predict, k):
    '''
    计算调整R^2

    Parameters
    ----------
    y_true : np.array, pd.Series
        真实值
    y_predict : np.array, pd.Series
        预测值
    k : int
        预测y所用自变量个数

        .. note::
            线性回归中常量也算一个变量，例如y=ax+b，则k为2


    :returns: `float` - 调整R^2值

    References
    ----------
    http://blog.sciencenet.cn/blog-651374-975670.html
    '''
    vR2 = r2(y_true, y_predict)
    n = len(y_true)
    return 1 - (1-vR2) * ((n-1) / (n-k))


def r2adj_by_r2(r2, n, k):
    '''
    | 通过R^2计算调整R^2, n为样本量, k为自变量个数
    | 注：线性回归中常量也算一个变量，例如y=ax+b，则k为2
    '''
    return 1 - (1-r2) * ((n-1) / (n-k))


def r2_by_mse(mse, y_true):
    '''
    根据MSE和真实值y_true(`pd.Series, np.array`)计算拟合优度R^2
    
    References
    ----------
    https://blog.csdn.net/wade1203/article/details/98477034
    https://blog.csdn.net/liangyihuai/article/details/88560859
    '''
    y_true_var = pd.Series(y_true).var(ddof=0)
    return 1 - mse / y_true_var


def r2adj_by_mse(mse, y_true, k):
    '''
    | 通过MSE计算调整R^2, y_true为真实值(`pd.Series, np.array`), n为样本量, k为自变量个数
    | 注：线性回归中常量也算一个变量，例如y=ax+b，则k为2
    '''
    n = len(y_true)
    vR2 = r2_by_mse(mse, y_true)
    return 1 - (1-vR2) * ((n-1) / (n-k))


def r2_by_r2adj(r2adj, n, k):
    '''
    | 通过调整R^2计算R^2, n为样本量, k为自变量个数
    | 注：线性回归中常量也算一个变量，例如y=ax+b，则k为2
    '''
    return 1 - (1-r2adj) * ((n-k) / (n-1))


def mse_by_r2(r2, y_true):
    '''
    根据R^2和真实值y_true(`pd.Series, np.array`)计算MSE
    '''
    y_true_var = pd.Series(y_true).var(ddof=0)
    return (1-r2) * y_true_var


def _r2_deprecated(y_true, y_predict):
    '''
    拟合优度R^2计算, y_true, y_predict为 `pd.Series` 或 `np.array`

    References
    ----------
    https://blog.csdn.net/wade1203/article/details/98477034
    https://blog.csdn.net/liangyihuai/article/details/88560859
    '''
    vMSE = mse(y_true, y_predict)
    y_true_var = pd.Series(y_true).var(ddof=0)
    return 1 - vMSE / y_true_var


def rmse(y_true, y_predict):
    '''
    计算RMSE, y_true, y_predict为 `pd.Series` 或 `np.array`
    '''
    return mse(y_true, y_predict) ** 0.5


def mae(y_true, y_predict):
    '''
    计算MAE, y_true, y_predict为 `pd.Series` 或 `np.array`
    '''
    if y_predict.shape != y_true.shape:
        raise ValueError('y_true和y_predict的值必须一一对应！')
    yTrue = pd.Series(y_true).reset_index(drop=True)
    yPred = pd.Series(y_predict).reset_index(drop=True)
    return (abs(yTrue-yPred)).mean()


def mape(y_true, y_predict):
    '''
    计算MAPE, y_true, y_predict为 `pd.Series` 或 `np.array`

    Note
    ----
    当y_true存在0值时MAPE不可用
    '''
    if y_predict.shape != y_true.shape:
        raise ValueError('y_true和y_predict的值必须一一对应！')
    yTrue = pd.Series(y_true).reset_index(drop=True)
    yPred = pd.Series(y_predict).reset_index(drop=True)
    return (abs((yPred-yTrue) / yTrue)).mean()


def smape(y_true, y_predict):
    '''
    计算SMAPE，y_true, y_predict为 `pd.Series` 或 `np.array`

    Note
    ----
    当y_true和y_predict均为0值时SMAPE不可用

    References
    ----------
    https://blog.csdn.net/guolindonggld/article/details/87856780
    '''
    if y_predict.shape != y_true.shape:
        raise ValueError('y_true和y_predict的值必须一一对应！')
    yTrue = pd.Series(y_true).reset_index(drop=True)
    yPred = pd.Series(y_predict).reset_index(drop=True)
    return (abs(yPred-yTrue) / ((abs(yPred)+abs(yTrue)) / 2)).mean()


def avedev(arr):
    '''
    AVEDEV函数，arr为 `np.array` 或 `pd.Series`

    References
    ----------
    https://support.microsoft.com/en-us/office/avedev-function-58fe8d65-2a84-4dc7-8052-f3f87b5c6639?ui=en-us&rs=en-us&ad=us
    '''

    return (abs(arr-arr.mean())).mean()


def cal_linear_reg_r(y, x=None, fit_intercept=True):
    '''
    | 简单计算一元线性回归斜率
    | y和x为 `list` 或 `pd.Series` 或 `np.array` (x和y均为一维)
    | 若x为None，则回归自变量取range(0, len(y))
    | fit_intercept=True时返回斜率和截距，否则只返回斜率
    '''
    if isnull(x):
        X = pd.DataFrame({'X': range(0, len(y))})
    else:
        X = pd.DataFrame({'X': x})
    y = pd.Series(y)
    mdl = lr(fit_intercept=fit_intercept).fit(X, y)
    if fit_intercept:
        return mdl.coef_[0], mdl.intercept_
    else:
        return mdl.coef_[0]


def cummean(series, skipna=True):
    '''
    | 滚动计算序列series(`list, np.array, pd.Series`)累计均值
    | skip设置是否忽略无效值记录
    '''
    df = pd.DataFrame({'series': series})
    df['cumsum'] = df['series'].cumsum(skipna=skipna)
    df['N'] = range(1, df.shape[0]+1)
    if skipna:
        df['N'] = df['series'].notna().cumsum()
    df['cummean'] = df['cumsum'] / df['N']
    return df['cummean']


def delta_var_d0(n0, mean0, var0, n1, mean1, var1):
    '''
    | 自由度为0情况下的增量方差计算
    | n, mean, var分别为第一组和第二组(增量)样本的样本量、均值和自由度为0的方差

    References
    ----------
    https://www.cnblogs.com/yoyaprogrammer/p/delta_variance.html
    https://blog.csdn.net/u013337691/article/details/119326155
    '''
    if n0 < 1 or n1 < 1:
        raise ValueError('样本量必须大于1！')
    fm = n0 + n1
    mean = (n0 * mean0 + n1 * mean1) / fm
    fz1 = n0 * (var0 + (mean - mean0) ** 2)
    fz2 = n1 * (var1 + (mean - mean1) ** 2)
    var = (fz1 + fz2) / fm
    return var


def delta_var_d(n0, mean0, var0, n1, mean1, var1, ddof=1):
    '''
    | 增量方差算法：根据已经算好的两组样本的方差、均值和样本量计算两组数合并之后的方差
    | n, mean, var分别为两组样本的样本量、均值和自由度为ddof的方差
    | 注：跟 :func:`delta_var` 的区别在于本函数调用了 :func:`delta_var_d0`
    
    References
    ----------
    https://www.cnblogs.com/yoyaprogrammer/p/delta_variance.html
    https://blog.csdn.net/u013337691/article/details/119326155
    '''
    fm = n0 + n1
    if n0 <= ddof or n1 <= ddof or fm <= ddof: # 样本量必须大于自由度
        return np.nan
    # 自由度还原为0
    var0_0, var1_0 = ((n0-ddof) / n0) * var0, ((n1-ddof) / n1) * var1
    var_0 = delta_var_d0(n0, mean0, var0_0, n1, mean1, var1_0)
    var = (fm / (fm-ddof)) * var_0 # 自由度转换
    return var


def delta_var(n0, mean0, var0, n1, mean1, var1, ddof=1):
    '''
    | 增量方差算法：根据已经算好的两组样本的方差、均值和样本量计算两组数合并之后的方差
    | n, mean, var分别为两组样本的样本量、均值和自由度为ddof的方差
    | 注：跟 :func:`delta_var_d` 的区别在于本函数没调用 :func:`delta_var_d0`
    
    References
    ----------
    https://www.cnblogs.com/yoyaprogrammer/p/delta_variance.html
    https://blog.csdn.net/u013337691/article/details/119326155
    '''
    n = n0+n1
    if n0 <= ddof or n1 <= ddof or n <= ddof: # 样本量必须大于自由度
        return np.nan
    fm = n - ddof
    mean = (n0 * mean0 + n1 * mean1) / n
    fz1 = (n0-ddof) * var0 + n0 * (mean - mean0) ** 2
    fz2 = (n1-ddof) * var1 + n1 * (mean - mean1) ** 2
    var = (fz1 + fz2) / fm
    return var


def cumvar_nonan(series, ddof=1):
    '''
    滚动累计方差算法

    Parameters
    ----------
    series : pd.Series, np.array
        目标序列，不应有无效值
    ddof : int
        自由度


    :returns: `np.array` - 滚动累计方差计算结果
    
    Note
    ----
    series会被当成没有无效值处理

    See Also
    --------
    :func:`dramkit.datsci.stats.delta_var`
    '''

    # 数据格式检查
    series = np.array(series)
    assert len(series.shape) == 1, 'series必须为1维！'
    # assert sum(np.isnan(series)) == 0, 'series中不能有无效值！'

    # 累计均值
    cummean = np.cumsum(series) / np.arange(1, len(series)+1)

    # 累计方差
    cumvar = np.nan * np.ones(len(series),)
    if ddof == 0:
        cumvar[0] = 0
    else:
        for k in range(ddof, ddof+ddof+1):
            cumvar[k] = np.var(series[:k+1], ddof=ddof)
    for k in range(ddof+ddof+1, len(series)):
        var0, mean0, n0 = cumvar[k-ddof-1], cummean[k-ddof-1], k-ddof
        var1 = np.var(series[k-ddof:k+1], ddof=ddof)
        mean1 = np.mean(series[k-ddof:k+1])
        # 增量方差
        cumvar[k] = delta_var(n0, mean0, var0, ddof+1, mean1, var1, ddof=ddof)
    
    return cumvar


def cumvar(series, ddof=1, skipna=True):
    '''
    滚动累计方差算法

    Parameters
    ----------
    series : np.array, pd.Series
        目标序列，不应有无效值
    ddof : int
        自由度
    skipna : bool
        是否忽略无效值


    :returns: `pd.Series` - 滚动累计方差计算结果

    See Also
    --------
    :func:`dramkit.datsci.stats.cumvar_nonan`
    '''
    df = pd.DataFrame({'v': series})
    if not skipna:
        df['cumvar'] = cumvar_nonan(df['v'], ddof=ddof)
        return df['cumvar']
    else:
        df_ = df.dropna(subset=['v'], how='any').copy()
        df_['cumvar'] = cumvar(df_['v'], ddof=ddof, skipna=False)
        df['cumvar'] = df_['cumvar']
        return df['cumvar']


def _cumvar1(series, ddof=1, skipna=True):
    '''
    | 滚动计算序列累计方差， 调用 :func:`delta_var` 函数
    | 参考：https://www.cnblogs.com/yoyaprogrammer/p/delta_variance.html
    '''

    df = pd.DataFrame({'v': series})
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)

    df['cummean'] = cummean(df['v'], skipna=skipna)

    if skipna:
        df_var = df.dropna(subset=['v'], how='any').copy()
    else:
        df_var = df.copy()

    if ddof == 0:
        df_var['cumvar'] = 0
        for k in range(1, df_var.shape[0]):
            var0 = df_var.loc[df_var.index[k-1], 'cumvar']
            mean0 = df_var.loc[df_var.index[k-1], 'cummean']
            mean1 = df_var.loc[df_var.index[k], 'v']
            var = delta_var(k, mean0, var0, 1, mean1, 0, ddof=0)
            df_var.loc[df_var.index[k], 'cumvar'] = var
    else:
        df_var['roll_var'] = df_var['v'].rolling(ddof+1).var(skipna=skipna,
                                                             ddof=ddof)
        df_var['roll_mean'] = df_var['v'].rolling(ddof+1).mean(skipna=skipna)
        df_var['cumvar'] = np.nan
        for k in range(ddof, ddof+ddof+1):
            df_var.loc[df_var.index[k], 'cumvar'] = \
                        df_var['v'].iloc[:k+1].var(skipna=skipna, ddof=ddof)
        for k in range(ddof+ddof+1, df_var.shape[0]):
            var0 = df_var.loc[df_var.index[k-ddof-1], 'cumvar']
            mean0 = df_var.loc[df_var.index[k-ddof-1], 'cummean']
            n0 = k - ddof
            var1 = df_var.loc[df_var.index[k], 'roll_var']
            mean1 = df_var.loc[df_var.index[k], 'roll_mean']
            n1 = ddof + 1
            var = delta_var(n0, mean0, var0, n1, mean1, var1, ddof=ddof)
            df_var.loc[df_var.index[k], 'cumvar'] = var

    df['cumvar'] = df_var['cumvar']

    df.index = ori_idx

    return df['cumvar']


def _cumvar2(series, ddof=1, skipna=True):
    '''
    | 滚动计算序列累计方差，调用 :func:`delta_var_d` 函数
    | https://www.cnblogs.com/yoyaprogrammer/p/delta_variance.html
    '''

    df = pd.DataFrame({'v': series})
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)

    df['cumsum'] = df['v'].cumsum(skipna=skipna)
    df['N'] = range(1, df.shape[0]+1)
    if skipna:
        df['N'] = df['v'].notna().cumsum()
    df['cummean'] = df['cumsum'] / df['N']

    if skipna:
        df_var = df.dropna(subset=['v'], how='any').copy()
    else:
        df_var = df.copy()

    if ddof == 0:
        df_var['cumvar'] = 0
        for k in range(1, df_var.shape[0]):
            var0 = df_var.loc[df_var.index[k-1], 'cumvar']
            mean0 = df_var.loc[df_var.index[k-1], 'cummean']
            mean1 = df_var.loc[df_var.index[k], 'v']
            var = delta_var_d0(k, mean0, var0, 1, mean1, 0)
            df_var.loc[df_var.index[k], 'cumvar'] = var
    else:
        df_var['roll_var'] = df_var['v'].rolling(ddof+1).var(skipna=skipna,
                                                             ddof=ddof)
        df_var['roll_mean'] = df_var['v'].rolling(ddof+1).mean(skipna=skipna)
        df_var['cumvar'] = np.nan
        for k in range(ddof, ddof+ddof+1):
            df_var.loc[df_var.index[k], 'cumvar'] = \
                        df_var['v'].iloc[:k+1].var(skipna=skipna, ddof=ddof)
        for k in range(ddof+ddof+1, df_var.shape[0]):
            var0 = df_var.loc[df_var.index[k-ddof-1], 'cumvar']
            mean0 = df_var.loc[df_var.index[k-ddof-1], 'cummean']
            n0 = k - ddof
            var1 = df_var.loc[df_var.index[k], 'roll_var']
            mean1 = df_var.loc[df_var.index[k], 'roll_mean']
            n1 = ddof + 1
            var = delta_var_d(n0, mean0, var0, n1, mean1, var1, ddof=ddof)
            df_var.loc[df_var.index[k], 'cumvar'] = var

    df['cumvar'] = df_var['cumvar']

    df.index = ori_idx

    return df['cumvar']


def cumstd(series, ddof=1, skipna=True):
    '''滚动计算序列累计标准差，参数意义同 :func:`cumvar`'''
    return np.sqrt(cumvar(series, ddof=ddof, skipna=skipna))


def _cumvar_deprecated(series, **kwargs):
    '''
    滚动计算序列累计方差，原始方法，kwargs为pd中var函数接受的参数
    '''
    df = pd.DataFrame({'v': series})
    df['cumvar'] = np.nan
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)
    for k in range(df.shape[0]):
        df.loc[df.index[k], 'cumvar'] = \
                                df.loc[df.index[:k+1], 'v'].var(**kwargs)
    df.index = ori_idx
    return df['cumvar']


def _cumstd_deprecated(series, **kwargs):
    '''
    滚动计算序列累计标准差，原始方法，kwargs为pd中std函数接受的参数
    '''
    df = pd.DataFrame({'series': series})
    df['cumstd'] = np.nan
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)
    for k in range(df.shape[0]):
        df.loc[df.index[k], 'cumstd'] = \
                                df.loc[df.index[:k+1], 'series'].std(**kwargs)
    df.index = ori_idx
    return df['cumstd']


def cum_scale(series, scale_type=('maxmin', 0, 1)):
    '''
    序列累计标准化

    Parameters
    ----------
    series : np.array, pd.Series
        待计算目标序列
    scale_type : tuple
        标准化设置，可选：

        - 最大最小标准化：('maxmin', Nmin, Nmax)
        - 标准偏差法/Z-Score：('std', ) 或 'std'


    :returns: `pd.Series` - 累计标准化计算结果
    '''
    df = pd.DataFrame({'v': series})
    if scale_type[0] == 'maxmin':
        Nmin, Nmax = scale_type[1], scale_type[2]
        x = df['v']
        Xmin = df['v'].cummin()
        Xmax = df['v'].cummax()
        df['scale'] = Nmin + (x-Xmin) * (Nmax-Nmin) / (Xmax-Xmin)
    elif scale_type in ['std', 'z-score'] or \
                                        scale_type[0] in ['std', 'z-score']:
        df['cummean'] = cummean(series)
        df['cumstd'] = cumstd(series)
        df['scale'] = (df['v'] - df['cummean']) / df['cumstd']
    return df['scale']


def rolling_scale(series, lag, scale_type=('maxmin', 0, 1)):
    '''
    序列滚动标准化

    Parameters
    ----------
    series : np.array, pd.Series
        待计算目标序列
    lag : int
        滚动窗口
    scale_type : tuple
        标准化设置，可选：

        - 最大最小标准化：('maxmin', Nmin, Nmax)
        - 标准偏差法/Z-Score：('std', ) 或 'std'


    :returns: `pd.Series` - 滚动标准化计算结果
    '''
    df = pd.DataFrame({'v': series})
    if scale_type[0] == 'maxmin':
        Nmin, Nmax = scale_type[1], scale_type[2]
        x = df['v']
        Xmin = df['v'].rolling(lag).min()
        Xmax = df['v'].rolling(lag).max()
        df['scale'] = Nmin + (x-Xmin) * (Nmax-Nmin) / (Xmax-Xmin)
    elif scale_type in ['std', 'z-score'] or \
                                        scale_type[0] in ['std', 'z-score']:
        df['mean_dy'] = df['v'].rolling(lag).mean()
        df['std_dy'] = df['v'].rolling(lag).std()
        df['scale'] = (df['v'] - df['mean_dy']) / df['std_dy']
    return df['scale']


def get_quantiles(series, method='dense', **kw_rank):
    '''
    | 计算series(`list, pd.Series, np.array`)中每个数所处的百分位
    | method决定并列排序序号确定方式，见pd中rank函数的参数
    '''
    series = pd.Series(series)
    if 'pct' in kw_rank:
        kw_rank.pop('pct')
    return series.rank(method=method, pct=True, **kw_rank)


def cumrank_nonan(series, ascending=True, method='dense',
                  verbose=False):
    '''
    滚动计算累计排序号，使用二分法改进的插入排序法

    Parameters
    ----------
    series : list, pd.Series, np.array
        待排序目标序列
    ascending : bool
        是否升序
    method : str
        排序规则，见pd中rank函数的参数


    :returns: `list` - 滚动累计排序序号列表
    
    Note
    ----
    series会被当成没有无效值处理
    '''

    series = list(series)
    n = len(series)
    cumranks = [1] * n

    nums_sorted = [series[0]]
    ranks = [1]
    if not verbose:
        for k in range(1, n):
            num = series[k]
            irank, (nums_sorted, ranks) = rank_of_insert_bin(nums_sorted, ranks,
                                          num, ascending=ascending, method=method)
            cumranks[k] = irank
    else:
        for k in tqdm(range(1, n)):
            num = series[k]
            irank, (nums_sorted, ranks) = rank_of_insert_bin(nums_sorted, ranks,
                                          num, ascending=ascending, method=method)
            cumranks[k] = irank

    return cumranks


def cumrank(series, ascending=True, method='dense', verbose=False):
    '''
    滚动计算累计排序号

    Parameters
    ----------
    series : list, pd.Series, np.array
        待排序目标序列
    ascending : bool
        是否升序
    method : str
        排序规则，见pd中rank函数的参数


    :returns: `pd.Series` - 滚动累计排序序号
    
    Note
    ----
    series中无效值会被忽略
    '''
    df = pd.DataFrame({'v': series})
    if df['v'].isnull().sum() == 0:
        return cumrank_nonan(series, ascending=ascending, method=method, verbose=verbose)
    else:
        df_ = df.copy()
        df_.dropna(subset=['v'], how='any', inplace=True)
        df_['cumrank'] = cumrank_nonan(df_['v'], ascending=ascending, method=method, verbose=verbose)
        df['cumrank'] = df_['cumrank']
        return df['cumrank']


def _cumrank1_nonan(series, ascending=True, method='dense'):
    '''
    滚动计算累计排序号，使用插入排序法
    '''

    series = list(series)
    n = len(series)
    cumranks = [1] * n

    nums_sorted = [series[0]]
    ranks = [1]
    for k in range(1, n):
        num = series[k]
        irank, (nums_sorted, ranks) = rank_of_insert(nums_sorted, ranks,
                                    num, ascending=ascending, method=method)
        cumranks[k] = irank

    return cumranks


def _cumrank1(series, ascending=True, method='dense'):
    '''
    滚动计算累计排序号，使用插入排序法
    '''
    df = pd.DataFrame({'v': series})
    if df['v'].isnull().sum() == 0:
        return _cumrank1_nonan(series, ascending=ascending, method=method)
    else:
        df_ = df.copy()
        df_.dropna(subset=['v'], how='any', inplace=True)
        df_['cumrank'] = _cumrank1_nonan(df_['v'], ascending=ascending, method=method)
        df['cumrank'] = df_['cumrank']
        return df['cumrank']


def _cumrank2(series, ascending=True, method='dense'):
    '''
    滚动计算累计排序号, pd原始排序方法
    '''
    df = pd.DataFrame({'v': series})
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)
    df['cumrank'] = np.nan
    for k in range(0, df.shape[0]):
        df.loc[df.index[k], 'cumrank'] = df.loc[df.index[:k+1], 'v'].rank(
                                  ascending=ascending, method=method).iloc[-1]
    df.index = ori_idx
    return df['cumrank']


def get_pct_loc(value, series, isnew=True, method='dense'):
    '''
    | 给定value(`float`)和series(`pd.Series, np.array`)，计算value在series中所处百分位
    | 若isnew为True，则将value当成新数据，若为False，则当成series中已经存在的数据
    | method决定并列排序序号确定方式，参见pd中的rank函数参数
    '''
    if isnull(value):
        return np.nan
    if not method in ['dense', 'average']:
        raise ValueError('未识别的并列排序方法！')
    vals = [value] + list(series)
    vals = pd.Series(vals)
    ranks = vals.rank(method=method)
    rank = ranks.iloc[0]
    if method == 'dense':
        return rank / ranks.max()
    elif method == 'average':
        if isnew or list(ranks).count(rank) == 1:
            return rank / len(ranks)
        else:
            return (rank-0.5) / (len(vals)-1)
        
        
def cum_n_unique(series, skipna=True):
    '''
    | 滚动计算series(`np.array, pd.Series, list`)中值的unique个数
    | 返回list
    '''
    vals = list(series)
    n = len(vals)
    if skipna:
        Nunique = [np.nan] * n
        k0 = 0
        while k0 < n and isnull(vals[k0]):
            k0 += 1
        Nunique[k0] = 1
        vunique = [vals[k0]]
        for k in range(k0+1, n):
            if isnull(vals[k]):
                continue
            else:
                if vals[k] in vunique:
                    Nunique[k] = Nunique[k0]
                else:
                    vunique.append(vals[k])
                    Nunique[k] = Nunique[k0] + 1
                k0 += 1
    else:
        Nunique = [1] * n
        vunique = [vals[0]]
        for k in range(1, n):
            if vals[k] in vunique:
                Nunique[k] = Nunique[k-1]
            else:
                vunique.append(vals[k])
                Nunique[k] = Nunique[k-1] + 1
    return Nunique


def cum_n_unique_pd(series, skipna=True):
    '''
    | 滚动计算series(`np.array, pd.Series, list`)中值的unique个数
    | 返回list
    | 与 :func:`cum_n_unique` 的区别是此函数使用pandas计算而不是循环迭代
    '''

    df = pd.DataFrame({'v': series})
    if skipna:
        df_ = df.dropna(subset=['v'], how='any').copy()
    else:
        df_ = df.copy()
    df_['Nunique'] = ~df_['v'].duplicated()
    df_['Nunique'] = df_['Nunique'].cumsum()

    df['Nunique'] = df_['Nunique']

    return df['Nunique']


def cum_pct_loc(series, method='dense', verbose=False):
    '''
    | 滚动计算series(`np.array, pd.Series`)数据累计所处百分位
    | 调用 :func:`dramkit.datsci.stats.cum_n_unique_pd` 函数
    '''
    if not method in ['dense', 'average']:
        raise ValueError('未识别的并列排序方法！')
    df = pd.DataFrame({'v': series})
    df['cumrank'] = cumrank(df['v'], method=method, verbose=verbose)
    if method == 'dense':
        df['cumNunique'] = cum_n_unique_pd(df['v'])
        df['PctLoc'] = df['cumrank'] / df['cumNunique']
    elif method == 'average':
        df['idx'] = range(1, df.shape[0]+1)
        df['PctLoc'] = df['cumrank'] / df['idx']
    return df['PctLoc']


def _cum_pct_loc1(series, method='dense'):
    '''
    | 滚动计算series(`np.array, pd.Series`)数据累计所处百分位
    | 调用 :func:`dramkit.datsci.stats.cum_n_unique` 函数
    '''
    if not method in ['dense', 'average']:
        raise ValueError('未识别的并列排序方法！')
    df = pd.DataFrame({'v': series})
    df['cumrank'] = cumrank(df['v'], method=method)
    if method == 'dense':
        df['cumNunique'] = cum_n_unique(df['v'])
        df['PctLoc'] = df['cumrank'] / df['cumNunique']
    elif method == 'average':
        df['idx'] = range(1, df.shape[0]+1)
        df['PctLoc'] = df['cumrank'] / df['idx']
    return df['PctLoc']


def _cum_pct_loc2(series, method='dense'):
    '''
    | 滚动计算series(`np.array, pd.Series`)数据累计所处百分位
    | 调用 :func:`dramkit.datsci.stats.get_pct_loc` 函数
    '''
    df = pd.DataFrame({'v': series})
    df['PctLoc'] = np.nan
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)
    df.loc[df.index[0], 'PctLoc'] = 1.0
    if isnull(df.loc[df.index[0], 'v']):
        df.loc[df.index[0], 'PctLoc'] = np.nan
    for k in range(1, df.shape[0]):
        value = df.loc[df.index[k], 'v']
        values = df.loc[df.index[:k], 'v']
        df.loc[df.index[k], 'PctLoc'] = get_pct_loc(value, values,
                                                    isnew=True, method=method)
    df.index = ori_idx
    return df['PctLoc']


def rolling_pct_loc(series, lag, method='dense'):
    '''
    | 滚动计算series(`np.array, pd.Series`)数据所处百分位
    | lag为滚动窗口长度
    | method为排序处理方式，见pd中的rank函数参数
    '''
    df = pd.DataFrame({'v': series})
    ori_idx = df.index
    df.reset_index(drop=True, inplace=True)
    # df['PctLoc'] = np.nan
    # for k in range(0, df.shape[0]-lag+1):
    #     value = df.loc[df.index[k+lag-1], 'v']
    #     values = df.loc[df.index[k:k+lag-1], 'v']
    #     df.loc[df.index[k+lag-1], 'PctLoc'] = \
    #                     get_pct_loc(value, values, isnew=True, method=method)
    df['PctLoc'] = df['v'].rolling(lag).apply(lambda x:
              get_pct_loc(x.iloc[-1], x.iloc[:-1], isnew=True, method=method))
    df.index = ori_idx
    return df['PctLoc']


def cal_mean_update_inrc(v, mean, n):
    '''均值增量更新算法(根据新值v和已知均值mean，已知计数n计算新的均值)'''
    # res = (mean * n + v) / (n+1)
    res = mean + (v - mean) / (n+1)
    return res


def cal_mean_robbins_morno(vals, alphas=None, mean_init=0):
    '''Robbins-Monro算法计算均值'''
    n = len(vals)
    if isnull(alphas):
        alphas = [1/k for k in range(1, n+1)]
    m = mean_init
    for k in range(n):
        m += alphas[k] * (vals[k] - m)
    return m


def vif(df: pd.DataFrame,
        cols: list = None,
        const: bool = False,
        method: int = 1):
    '''
    计算VIF（经测试method=1比method=2快三倍左右）
    
    Examples
    --------
    >>> df = pd.DataFrame({
    >>>          'a': [1, 1, 2, 3, 4],#, 5, 8, 19],
    >>>          'b': [2, 2, 3, 2, 1],#, 6, 9, 20],
    >>>          'c': [4, 6, 7, 8, 9],#, 7, 3, 1],
    >>>          'd': [4, 3, 4, 5, 4],#, 4, 9, 30]
    >>>          })
    >>> vif(df)
    {'a': 22.949999999999942,
     'b': 2.9999999999999964,
     'c': 12.949999999999967,
     'd': 2.9999999999999964}
    >>> vif(df, method=2)
    {'const': 136.87499999999918,
     'a': 22.949999999999985,
     'b': 2.9999999999999987,
     'c': 12.950000000000006,
     'd': 3.0000000000000107}
    >>> vif(df, const=True)
    {'const': 136.87499999999923,
     'a': 22.949999999999942,
     'b': 2.9999999999999964,
     'c': 12.949999999999967,
     'd': 2.9999999999999964}
    
    References
    ----------
    - https://www.zhihu.com/question/270451437/answer/405814593
    - https://javaforall.cn/135202.html
    '''
    if isnull(cols):
        cols = list(df.columns)
    df = df[cols]
    # 方式1，用变量相关系数矩阵的逆矩阵的对角元
    if method == 1:
        # rowvar=False表示每列为一个变量，每行为一个样本
        res = {}
        if const:
            x = df.mean().to_frame()
            x_ = x.transpose()
            s = np.linalg.inv(np.cov(df, rowvar=False, ddof=0))
            res = {'const': 1 + np.dot(np.dot(x_, s), x)[0][0]}
        corr = np.corrcoef(df, rowvar=False)
        res_ = np.linalg.inv(corr).diagonal()
        res.update(dict(zip(cols, res_)))
    elif method == 2:
        X = add_constant(df)
        res = [variance_inflation_factor(X.values, i) \
               for i in range(X.shape[1])]
        res = dict(zip(X.columns, res))
    else:
        raise ValueError('未知别的`method`(只能为1或2)!')
    return res


def parms_est():
    '''各种分布不同方法的参数估计，待实现'''
    raise NotImplementedError


def auc():
    '''计算auc，待实现'''
    raise NotImplementedError


def var_hom_test(s1, s2):
    '''方差齐性检验，待实现'''
    raise NotImplementedError


def ind_ttest(s1, s2):
    '''独立样本T检验，待实现'''
    raise NotImplementedError


def rel_ttest(s1, s2):
    '''配对样本T检验，待实现'''
    raise NotImplementedError


def anova_oneway(df, col_val, col_group):
    '''
    单因素方差分析，col_val为待比较列，col_group为组别列，待实现
    '''
    raise NotImplementedError
