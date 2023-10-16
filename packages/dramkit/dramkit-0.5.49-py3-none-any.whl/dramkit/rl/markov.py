# -*- coding: utf-8 -*-

import time
import sympy
import scipy
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import product
from scipy.linalg import block_diag

from dramkit.gentools import (link_lists,
                              isnull,
                              capture_print,
                              rand_sum,
                              raise_error)

#%%
def get_matrixs_by_sasr(pi_s2a,
                        p_sa2sr,
                        rewards,
                        s_names=None,
                        a_names=None):
    '''
    | 根据策略矩阵pi_s2a: P(s,a)和动力系统矩阵p_sa2sr: P(s',r'|s,a)
    | 生成相关矩阵
    | pi_s2a为策略概率矩阵
    | p_sa2sr为带奖励值的状态&动作-状态转移概率矩阵
    | rewards为奖励空间列表
    | gamma为奖励的权重衰减系数（折扣因子）
    | s_names和a_names分别为状态空间和动作空间的名称列表
    | 注意：概率矩阵、奖励空间列表和状态空间及动作空间名称的顺序必须是对应的
    '''
    
    pi_s2a, p_sa2sr = np.array(pi_s2a), np.array(p_sa2sr)
    rewards = list(rewards)
    n_s, n_a = pi_s2a.shape
    n_sa, n_sr = p_sa2sr.shape
    
    if s_names is None:
        s_names = ['s%s'%k for k in range(1, n_s+1)]
    if a_names is None:
        a_names = ['a%s'%k for k in range(1, n_a+1)]        
    sa_names = list(product(s_names, a_names))
    sr_names = list(product(s_names, rewards))        
    
    # 策略状态-动作概率矩阵
    pi_s2a = pd.DataFrame(pi_s2a, index=s_names, columns=a_names)
    pi_s2a.index.name = 's'
    pi_s2a.columns.name = 'a'
    # 状态&动作-状态&奖励概率矩阵
    p_sa2sr = pd.DataFrame(p_sa2sr, index=sa_names, columns=sr_names)
    p_sa2sr.index.name = 'sa'
    p_sa2sr.columns.name = 'sr'
    
    # 状态&动作-状态转移概率矩阵
    p_sa2s = p_sa2sr.transpose()
    p_sa2s = p_sa2s.reset_index()
    p_sa2s[['s', 'r']] = p_sa2s['sr'].tolist()
    def _sum(df):
        return df.drop(['sr', 's', 'r'], axis=1).sum()
    p_sa2s = p_sa2s.groupby('s').apply(lambda x: _sum(x))
    p_sa2s = p_sa2s.transpose()
    p_sa2s = p_sa2s.reindex(columns=s_names,
                            index=p_sa2sr.index)
    
    # 策略状态-动作矩阵构造分块对角矩阵
    pi_s2a_diag = block_diag(*(pi_s2a.iloc[k, :] for k in range(pi_s2a.shape[0])))
    
    # 策略下状态-状态转移概率矩阵
    pi_s2s = np.matmul(pi_s2a_diag, p_sa2s)
    pi_s2s.index = s_names
    pi_s2s.index.name = 's'
    
    # 策略下状态&动作-状态&动作转移概率矩阵
    pi_sa2sa = pd.concat([p_sa2s]*len(a_names), axis=1)
    pi_sa2sa.columns = [(s, a) for a in a_names for s in p_sa2s.columns]
    pi_sa2sa = pi_sa2sa.reindex(index=p_sa2s.index,
                                columns=p_sa2s.index)
    pi_sa2sa = pi_sa2sa * link_lists(pi_s2a.to_dict('split')['data'])
    
    r_e_sa2s = [x[1] for x in sr_names]
    r_e_sa2s = r_e_sa2s * p_sa2sr
    # 状态&动作期望奖励
    r_e_sa = r_e_sa2s.sum(axis=1).to_frame()
    r_e_sa.columns = ['r']
    # 状态期望奖励
    r_e_s = r_e_sa.reset_index()
    r_e_s[['s', 'a']] = r_e_s['sa'].tolist()
    def _sum2(df):
        return df.drop(['sa', 's', 'a'], axis=1).sum()
    r_e_s = r_e_s.groupby('s').apply(lambda x: _sum2(x))
    r_e_s = r_e_s.reindex(index=pi_s2a.index)
    # 状态&动作-状态期望奖励
    r_e_sa2s = r_e_sa2s.transpose()
    r_e_sa2s = r_e_sa2s.reset_index()
    r_e_sa2s[['s', 'r']] = r_e_sa2s['sr'].tolist()
    def _sum3(df):
        return df.drop(['sr', 's', 'r'], axis=1).sum()
    r_e_sa2s = r_e_sa2s.groupby('s').apply(lambda x: _sum3(x))
    r_e_sa2s = r_e_sa2s.transpose()
    r_e_sa2s = r_e_sa2s.reindex(columns=s_names,
                            index=p_sa2s.index)
    # 状态&动作-状态奖励
    r_sa2s = r_e_sa2s / p_sa2s.replace(0, np.nan) # 概率为0时计算不出来
    
    # 策略下每个状态的期望奖励
    r_e_pi_s = pi_s2a * r_e_sa.values.reshape(n_s, n_a)
    r_e_pi_s = r_e_pi_s.sum(axis=1).to_frame()
    r_e_pi_s.columns = ['r']
    
    return  pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, \
            pi_sa2sa, r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s
            
            
def get_matrixs_by_sas(pi_s2a,
                       p_sa2s,
                       r_sa2s,
                       s_names=None,
                       a_names=None):
    '''
    | 根据策略矩阵pi_s2a: P(s,a)和动力系统矩阵p_sa2s: P(s'|s,a)、r_sa2s: R(s'|s,a)
    | 生成相关矩阵
    | pi_sa2s为状态&动作-状态转移概率矩阵
    | r_sa2s为与p_sa2s一一对应的奖励表
    '''
    
    pi_s2a, p_sa2s = np.array(pi_s2a), np.array(p_sa2s)
    n_s, n_a = pi_s2a.shape
    n_sa, n_s = p_sa2s.shape
    
    if s_names is None:
        s_names = ['s%s'%k for k in range(1, n_s+1)]
    if a_names is None:
        a_names = ['a%s'%k for k in range(1, n_a+1)]        
    sa_names = list(product(s_names, a_names))        
    
    # 策略状态-动作概率矩阵
    pi_s2a = pd.DataFrame(pi_s2a, index=s_names, columns=a_names)
    pi_s2a.index.name = 's'
    pi_s2a.columns.name = 'a'
    # 状态&动作-状态转移概率矩阵
    p_sa2s = pd.DataFrame(p_sa2s, index=sa_names, columns=s_names)
    p_sa2s.index.name = 'sa'
    p_sa2s.columns.name = 's'
    # 状态&动作-状态奖励
    r_sa2s = pd.DataFrame(r_sa2s, index=sa_names, columns=s_names)
    r_sa2s.index.name = 'sa'
    r_sa2s.columns.name = 's'
        
    # 策略状态-动作矩阵构造分块对角矩阵
    pi_s2a_diag = block_diag(*(pi_s2a.iloc[k, :] for k in range(pi_s2a.shape[0])))
    
    # 策略下状态-状态转移概率矩阵
    pi_s2s = np.matmul(pi_s2a_diag, p_sa2s)
    pi_s2s.index = s_names
    pi_s2s.index.name = 's'
    
    # 策略下状态&动作-状态&动作转移概率矩阵
    pi_sa2sa = pd.concat([p_sa2s]*len(a_names), axis=1)
    pi_sa2sa.columns = [(s, a) for a in a_names for s in p_sa2s.columns]
    pi_sa2sa = pi_sa2sa.reindex(index=p_sa2s.index,
                                columns=p_sa2s.index)
    pi_sa2sa = pi_sa2sa * link_lists(pi_s2a.to_dict('split')['data'])
    
    # 状态&动作-状态期望奖励
    r_e_sa2s = r_sa2s * p_sa2s
    
    # 状态&动作期望奖励
    r_e_sa = r_e_sa2s.sum(axis=1).to_frame()
    r_e_sa.columns = ['r']
    
    # 状态期望奖励
    r_e_s = r_e_sa.reset_index()
    r_e_s[['s', 'a']] = r_e_s['sa'].tolist()
    def _sum2(df):
        return df.drop(['sa', 's', 'a'], axis=1).sum()
    r_e_s = r_e_s.groupby('s').apply(lambda x: _sum2(x))
    r_e_s = r_e_s.reindex(index=pi_s2a.index)
    
    # 策略下每个状态的期望奖励
    r_e_pi_s = pi_s2a * r_e_sa.values.reshape(n_s, n_a)
    r_e_pi_s = r_e_pi_s.sum(axis=1).to_frame()
    r_e_pi_s.columns = ['r']
    
    p_sa2sr = None
    
    return  pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, \
            pi_sa2sa, r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s
            
#%%
def _bellman_all(pi_s2a, pi_s2a_diag, p_sa2s, r_e_sa, gamma,
                 symbol=False):
    a_up = np.concatenate([np.eye(pi_s2a.shape[0]), -pi_s2a_diag], axis=1)
    a_low = np.concatenate([-gamma*p_sa2s, np.eye(pi_s2a.shape[0]*pi_s2a.shape[1])], axis=1)
    a_ = np.concatenate([a_up, a_low], axis=0)
    
    y_up = [[0] for _ in range(pi_s2a.shape[0])]
    y_ = np.concatenate((y_up, r_e_sa), axis=0)
    
    system = np.concatenate([a_, y_], axis=1)
    
    if symbol:
        system = sympy.Matrix(system)        
        ynames = []
        for s in pi_s2a.index:
            exec('{s} = symbols("{s}")'.format(s=s))
            ynames.append(eval('{}'.format(s)))
        for sa in p_sa2s.index:
            exec('{sa0}_{sa1} = symbols("{sa0}_{sa1}")'.format(sa0=sa[0], sa1=sa[1]))
            ynames.append(eval('{}_{}'.format(sa[0], sa[1])))            
        results = sympy.solve_linear_system(system, *ynames)
    else:
        results = np.linalg.solve(a_, y_)
        results = pd.DataFrame(results,
                               index=list(pi_s2a.index)+list(p_sa2s.index),
                               columns=['v'])
        results = results['v'].to_dict()
    
    return results, pd.DataFrame(np.array(system))


def bellman_sasr(pi_s2a, p_sa2sr, rewards, gamma,
                 s_names=None, a_names=None, symbol=False):
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sasr(pi_s2a, p_sa2sr, rewards,
                                s_names=s_names, a_names=a_names)
    return _bellman_all(pi_s2a, pi_s2a_diag, p_sa2s, r_e_sa, gamma,
                        symbol=symbol)


def bellman_sas(pi_s2a, p_sa2s, r_sa2s, gamma,
                s_names=None, a_names=None, symbol=False):
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    return _bellman_all(pi_s2a, pi_s2a_diag, p_sa2s, r_e_sa, gamma,
                        symbol=symbol)


def _bellman_ss_sv(p_s2s, r_s, gamma, symbol=False):
    i = pd.DataFrame(np.eye(p_s2s.shape[0]),
                     index=p_s2s.index,
                     columns=p_s2s.columns)
    a_ = i - gamma * p_s2s
    
    y_ = np.array(r_s).reshape(-1,1)
    
    system = np.concatenate([a_.values, y_], axis=1)
    
    if symbol:
        system = sympy.Matrix(system)        
        ynames = []
        for s in p_s2s.index:
            exec('{s} = symbols("{s}")'.format(s=s))
            ynames.append(eval('{}'.format(s)))            
        results = sympy.solve_linear_system(system, *ynames)
    else:
        results = np.linalg.solve(a_, y_)
        results = pd.DataFrame(results,
                               index=p_s2s.index,
                               columns=['v'])
        results = results['v'].to_dict()
        
    return results, pd.DataFrame(np.array(system))


def bellman_sas_sv(pi_s2a, p_sa2s, r_sa2s, gamma,
                   s_names=None, a_names=None, symbol=False):
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    return _bellman_ss_sv(pi_s2s, r_e_pi_s, gamma, symbol=symbol)


def bellman_ss_sv(p_s2s, r_s, gamma,
                  s_names=None, symbol=False):
    p_s2s = pd.DataFrame(p_s2s)
    r_s = pd.DataFrame(r_s)
    if s_names is None:
        s_names = ['s%s'%k for k in range(1, p_s2s.shape[0]+1)]
    p_s2s.index = s_names
    p_s2s.columns = s_names
    r_s.index = s_names
    return _bellman_ss_sv(p_s2s, r_s, gamma, symbol=symbol)


def bellman_sas_av(pi_s2a, p_sa2s, r_sa2s, gamma,
                   s_names=None, a_names=None, symbol=False):
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    
    i = pd.DataFrame(np.eye(p_sa2s.shape[0]),
                     index=p_sa2s.index,
                     columns=p_sa2s.index)   
    a_ = i - gamma * pi_sa2sa
    
    y_ = np.array(r_e_sa['r']).reshape(-1,1)
    
    system = np.concatenate([a_.values, y_], axis=1)
    
    if symbol:
        system = sympy.Matrix(system)    
        ynames = []
        for sa in pi_sa2sa.index:
            exec('{sa0}_{sa1} = symbols("{sa0}_{sa1}")'.format(sa0=sa[0], sa1=sa[1]))
            ynames.append(eval('{}_{}'.format(sa[0], sa[1])))        
        results = sympy.solve_linear_system(system, *ynames)
    else:
        results = np.linalg.solve(a_, y_)
        results = pd.DataFrame(results,
                               index=pi_sa2sa.index,
                               columns=['v'])
        results = results['v'].to_dict()
        
    return results, pd.DataFrame(np.array(system))

def get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma):
    v_sa = np.array(r_e_sa).reshape(-1, 1) + \
           gamma*np.dot(np.array(p_sa2s), np.array(v_s).reshape(-1, 1))
    if isinstance(r_e_sa, pd.DataFrame):
        v_sa = pd.DataFrame(v_sa, columns=['v'],
                            index=r_e_sa.index)
    if isinstance(r_e_sa, pd.Series):
        v_sa = pd.Series(v_sa, index=r_e_sa.index)
    return v_sa


def get_sv_from_sav(v_sa, pi_s2a):
    p_s2a = np.array(pi_s2a)
    n_s, n_a = p_s2a.shape
    v_s = np.array(v_sa).reshape(n_s, n_a) * p_s2a
    v_s = v_s.sum(axis=1)
    if isinstance(pi_s2a, pd.DataFrame):
        v_s = pd.DataFrame(v_s, columns=['v'],
                           index=pi_s2a.index)
    return v_s

#%%
def get_best_bellman_linprog(p_sa2s, r_sa2s, gamma,
                             weights=None, bounds=None):
    p_sa2s, r_sa2s = np.array(p_sa2s), np.array(r_sa2s)
    r_e_sa = (p_sa2s*r_sa2s).sum(axis=1)
    if isnull(weights):
        weights = np.ones(p_sa2s.shape[1])
    else:
        weights = np.array(weights)
    n_sa, n_s = p_sa2s.shape
    n_a = int(n_sa / n_s)
    a_ub = gamma * p_sa2s - np.repeat(np.eye(n_s), n_a, axis=0)
    b_ub = -np.array(r_e_sa)
    if isnull(bounds):
        bounds = [(None, None),] * n_s
    v_s = scipy.optimize.linprog(weights, a_ub, b_ub, bounds=bounds,
                                 method='highs')
    v_s = v_s.x
    if isnull(v_s):
        raise_error('LingProError', '线性规划求解失败！')
    v_sa = get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma)
    return v_s, v_sa

#%%
def get_sv_mc(pi_s2a, p_sa2s, r_sa2s, gamma,
              max_step, n=1000,
              s_names=None, a_names=None, s_stop=None,
              first_visit=False):
    '''蒙特卡洛估计状态价值'''
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    
    s_names = pi_s2a.index.tolist()
    a_names = pi_s2a.columns.tolist()
    if isnull(s_stop):
        s_stop = s_names[-1]
        
    # 蒙特卡洛采样
    s_ = [x for x in s_names if x != s_stop]
    routes = []
    for _ in tqdm(range(n)):
        route, n_step = [], 0
        s = np.random.choice(s_) # 随机选择初始状态
        while s != s_stop and n_step < max_step:
            n_step += 1
            rand, tmp = np.random.rand(), 0
            # 根据策略选择动作
            for _a in a_names:
                tmp += pi_s2a.loc[s, _a]
                if rand < tmp:
                    a = _a
                    r = r_e_sa.loc[[(s, a)], 'r'][(s, a)]
                    break
            rand, tmp = np.random.rand(), 0
            # 根据转移概率获取下一个状态
            for _s in s_names:
                tmp += p_sa2s.loc[[(s, a)], _s][(s, a)]
                if rand < tmp:
                    s_new = _s
                    break
            route.append((s, a, r, s_new, s_new == s_stop))
            s = s_new
        routes.append(route)
        
    # 状态价值估计
    if not first_visit:
        # 一条路径上从后往前计算状态价值
        s_n = {s: 0 for s in s_names}
        s_v = {s: 0 for s in s_names}
        for route in routes:
            k_r = 0
            for k in range(len(route)-1, -1, -1):
                (s, a, r, s_new, stop) = route[k]
                k_r = r + gamma * k_r # 步骤(时间)k的奖励
                s_n[s] = s_n[s] + 1
                s_v[s] = s_v[s] + (k_r-s_v[s]) / s_n[s]
        # # 一条路径上从前往后计算状态价值
        # s_n = {s: 0 for s in s_names}
        # s_v = {s: 0 for s in s_names}
        # for route in routes:
        #     n_ = len(route)
        #     # 从前往后计算须先取出每个步骤(时间)的奖励
        #     r_route = [x[2] for x in route]
        #     for k in range(n_):
        #         (s, a, r, s_new, stop) = route[k]
        #         # 步骤(时间)k的奖励
        #         k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
        #         s_n[s] = s_n[s] + 1
        #         s_v[s] = s_v[s] + (k_r-s_v[s]) / s_n[s]
    else:
        s_n = {s: 0 for s in s_names}
        s_v = {s: 0 for s in s_names}
        for route in routes:
            k_r = 0
            route_r = []
            for k in range(len(route)-1, -1, -1):
                (s, a, r, s_new, stop) = route[k]
                k_r = r + gamma * k_r
                route_r.append((s, k_r))
            visited = {s: 0 for s in s_names}
            for s, k_r in route_r[::-1]:
                # 仅考虑首次访问
                if visited[s]:
                    break
                visited[s] = 1
                s_n[s] = s_n[s] + 1
                s_v[s] = s_v[s] + (k_r-s_v[s]) / s_n[s]
        
    return s_v, routes

#%%
def get_occupancy(routes, s, a, max_step, gamma):
    '''计算状态动作对(s, a)出现的频率, 以此来估算策略的占用度量'''
    rho = 0
    n_all = np.zeros(max_step) # 记录每个时间步t被经历的次数
    n_sa = np.zeros(max_step) # 记录(s_t, a_t)=(s, a)的次数
    for route in routes:
        for k in range(len(route)):
            (_s, _a, r, s_new, stop) = route[k]
            n_all[k] += 1
            if s == _s and a == _a:
                n_sa[k] += 1
    for i in range(max_step):
    # for i in reversed(range(max_step)):
        if n_all[i]:
            # n_sa[i] / n_all[i]为第i步中(s, a)出现的比例
            rho += (gamma ** i) * (n_sa[i] / n_all[i])
    return (1-gamma) * rho

#%%
# @capture_print()
def get_sv_dp(pi_s2a, p_sa2s, r_sa2s, gamma,
              tol=1e-6, max_iter=2000,
              s_names=None, a_names=None,
              show_step=1000, **kwargs):
    '''动态规划-策略状态价值评估'''
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    
    n_s, n_a = pi_s2a.shape
    # 初始化状态价值
    v_s = pd.DataFrame({'v': np.zeros(n_s)}, index=pi_s2a.index)
    k = 0
    while k < max_iter:
        v_sa = get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma)
        v_s_new = get_sv_from_sav(v_sa, pi_s2a)
        max_dif = abs(v_s_new - v_s).max().max()
        v_s = v_s_new
        if max_dif < tol:
            k = np.inf
        k += 1
        if show_step and k % show_step == 0:
            print('iter: %d, max_dif: %s'%(k, max_dif))
    v_sa = get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma)
    return v_s, v_sa


def dp_improve_pi(pi_s2a, v_sa):
    '''动态规划，策略改进'''
    p_s2a = np.array(pi_s2a)
    n_s, n_a = p_s2a.shape
    vsa = np.array(v_sa).reshape(n_s, n_a)
    optimal = True
    bests_a = vsa.argmax(axis=1)
    best_pi_s2a = np.eye(n_a)[bests_a]
    if (abs(best_pi_s2a-p_s2a)).sum() > 0:
        optimal = False
    return best_pi_s2a, optimal


def dp_pi(p_sa2s, r_sa2s, gamma, pi_s2a=None,
          tol=1e-6, max_iter_est=2000, max_iter_impr=1000,
          s_names=None, a_names=None, show_step_est=1000,
          show_step=1000, kwargs_est={}, **kwargs):
    '''动态规划，策略迭代'''
    # 初始化为任意一个策略
    if isnull(pi_s2a):
        n_sa, n_s = np.array(p_sa2s.shape)
        n_a = int(n_sa/n_s)
        # pi_s2a = [rand_sum(1, n_a, 0.0, 1.0) for _ in range(n_s)]
        pi_s2a = np.ones((n_s, n_a)) / n_a
    k = 0
    while k < max_iter_impr:
        # 策略评估
        v_s, v_sa = get_sv_dp(pi_s2a, p_sa2s, r_sa2s, gamma,
                              tol=tol, max_iter=max_iter_est,
                              s_names=s_names, a_names=a_names,
                              show_step=show_step_est, **kwargs_est)
        # 策略改进
        pi_s2a, optimal = dp_improve_pi(pi_s2a, v_sa)
        if optimal:
            break
        k += 1
        if show_step and k % show_step == 0:
            print('iter: %d ...'%k)
    return pi_s2a, v_s, v_sa


def dp_val(p_sa2s, r_sa2s, gamma, pi_s2a=None,
           s_names=None, a_names=None,
           tol=1e-6, max_iter=2000, show_step=1000,
           **kwargs):
    '''动态规划，价值迭代'''
    n_sa, n_s = np.array(p_sa2s.shape)
    n_a = int(n_sa/n_s)
    if isnull(pi_s2a):
        # pi_s2a = [rand_sum(1, n_a, 0.0, 1.0) for _ in range(n_s)]
        pi_s2a = np.ones((n_s, n_a)) / n_a 
        
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
        
    # 价值迭代过程
    v_s = np.zeros(n_s) # 初始化状态价值
    k = 0
    while k < max_iter:
        v_sa = get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma)
        v_sa = np.array(v_sa).reshape(-1, n_a)
        v_s_new = v_sa.max(axis=1)        
        max_dif = abs(v_s_new - v_s).max()
        v_s = v_s_new
        if max_dif < tol:
            k = np.inf
        if show_step and k % show_step == 0:
            print('iter: %d, max_dif: %s'%(k, max_dif))
        k += 1
     
    # 生成最优策略
    v_sa = get_sav_from_sv(v_s, p_sa2s, r_e_sa, gamma)
    bests_a = np.array(v_sa).reshape(-1, n_a).argmax(axis=1)
    pi_s2a = np.eye(n_a)[bests_a]
    
    return pi_s2a, v_s, v_sa

#%%
if __name__ == '__main__':
    sympy.init_printing()
    from sympy import symbols
    from IPython.display import display
    from dramkit.gentools import TimeRecoder
    
    tr = TimeRecoder()
    
    #%%
    '''
    # 饥饿游戏----------------------------------------------
    # 《强化学习-原理与Python实现》第二章例子
    s_names = ['Hgry', 'Full'] # 状态空间
    a_names = ['notEat', 'Eat'] # 动作空间
    rewards = [-3, -2, 1, 2] # 奖励空间
    x, y = symbols('x y')
    alpha, beta, gamma = symbols('alpha beta gamma')
    # 策略概率表
    pi_s2a = [[1-x,   x],
              [  y, 1-y]]
    # 状态&动作-状态&奖励概率表
    p_sa2sr = [[      0,    1, 0, 0, 0, 0,     0,      0],
               [1-alpha,    0, 0, 0, 0, 0, alpha,      0],
               [      0, beta, 0, 0, 0, 0,     0, 1-beta],
               [      0,    0, 0, 0, 0, 0,     1,      0]]
    # 状态&动作-状态转移概率表
    p_sa2s = [[      1,      0],
              [1-alpha,  alpha],
              [   beta, 1-beta],
              [      0,      1]]
    # 状态&动作-状态奖励表
    r_sa2s = [[-2, 0],
              [-3, 1],
              [-2, 2],
              [ 0, 1]]
    
    # alpha_, beta_, gamma_ = 2/3, 3/4, 4/5
    alpha_, beta_, gamma_ = 1, 1, 4/5
    # '''
    
    '''
    # 1. 使用带奖励的状态&动作-状态&奖励转移矩阵-----------------
    res1, sys1 = bellman_sasr(
                    pi_s2a, p_sa2sr, rewards, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    display(res1)
    # for k, v in res1.items():
    #     display(k, v)
    # '''
    
    '''
    # 2. 使用状态&动作-状态转移矩阵----------------------------          
    res2, sys2 = bellman_sas(
                    pi_s2a, p_sa2s, r_sa2s, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    for k, v in res2.items():
        display(k, v)
        display(k, v.subs([(alpha, alpha_), 
                           (beta, beta_),
                           (gamma, gamma_)]))
    # '''
           
    '''
    # 3. 仅对状态价值自身相互表示
    res3, sys3 = bellman_sas_sv(
                    pi_s2a, p_sa2s, r_sa2s, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    res34 = res3.copy()
    # display(res3)
    for k, v in res3.items():        
        display(k, v)
        display(k, v.subs([(alpha, alpha_), 
                           (beta, beta_),
                           (gamma, gamma_)]))
    # '''
        
    '''
    # 4. 仅对动作价值自身相互表示
    res4, sys4 = bellman_sas_av(
                    pi_s2a, p_sa2s, r_sa2s, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    res34.update(res4)
    # display(res4)
    for k, v in res4.items():        
        display(k, v)
        display(k, v.subs([(alpha, alpha_), 
                           (beta, beta_),
                           (gamma, gamma_)]))
    # '''
        
    '''
    # 求状态价值最大值
    # xv = yv = np.linspace(0, 1, 50)
    xv, yv = [0], [0]
    dfv = pd.DataFrame(product(xv, yv), columns=['x', 'y'])
    dfv['x'] = 1 - dfv['x']
    for k, v in res34.items():
        v_name = str(k)
        dfv[v_name] = dfv[['x', 'y']].apply(
                        lambda xy: v.subs(
                            [(alpha, alpha_), (beta, beta_),
                             (gamma, gamma_),
                             (x, xy['x']), (y, xy['y'])]),
                        axis=1)
    print(dfv.max())
    # '''
    
    '''
    # 由状态价值得到动作价值-----------------------------------
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)
    # res5 = r_e_sa + gamma*np.dot(p_sa2s, np.array(list(res3.values())).reshape(-1, 1))
    res5 = get_sav_from_sv(list(res3.values()), p_sa2s, r_e_sa, gamma)
    for k in range(res5.shape[0]):
        # display(res5['v'].iloc[k])
        display(res5['v'].iloc[k].subs([(alpha, alpha_), 
                                        (beta, beta_),
                                        (gamma, gamma_),
                                        # (x, 0.816327),
                                        (x, 1),
                                        # (y, 1)
                                        (y, 0)
                                        ])
                )
    # '''
        
    '''
    # 线性规划求解
    pi_s2a, p_sa2sr, p_sa2s, pi_s2a_diag, pi_s2s, pi_sa2sa, \
    r_sa2s, r_e_sa2s, r_e_sa, r_e_s, r_e_pi_s = \
            get_matrixs_by_sas(pi_s2a, p_sa2s, r_sa2s,
                               s_names=s_names, a_names=a_names)

    for c in p_sa2s.columns:
        def _subs(x):
            try:
                return x.subs([(alpha, alpha_), (beta, beta_)])
            except:
                return x
        p_sa2s[c] = p_sa2s[c].apply(_subs)
    v_s, v_sa = get_best_bellman_linprog(p_sa2s, r_sa2s,
                                         gamma=gamma_,
                                         bounds=None,
                                         weights=None)
    print(v_s)
    print(v_sa)
    # '''
    
    #%%
    # 学生路径----------------------------------------------
    # https://www.cnblogs.com/pinard/p/9426283.html
    
    '''
    # 求状态价值（评估）--------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3']
    p_s2s = [[0.5, 0.5,   0,   0],
             [0.5,   0, 0.5,   0],
             [  0,   0,   0, 0.5],
             [  0, 0.1, 0.2, 0.2]
             ]
    r_s = [-0.5, -1.5, -1, 5.5]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=1,
                        s_names=s_names, symbol=False)
    display(s_vals)
    # '''
    
    '''
    # 求状态价值（评估）--------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3', 'Slp']
    p_s2s = [[0.5, 0.5,   0,   0,   0],
             [0.5,   0, 0.5,   0,   0],
             [  0,   0,   0, 0.5, 0.5],
             [  0, 0.1, 0.2, 0.2, 0.5],
             [  0,   0,   0,   0,   0]
             ]
    r_s = [-0.5, -1.5, -1, 5.5, 0]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=1,
                        s_names=s_names, symbol=False)
    display(s_vals)
    # '''
    
    '''
    # 求状态价值（评估）--------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3', 'Slp', 'Pub']
    p_s2s = [[0.5, 0.5,   0,   0,   0,   0],
             [0.5,   0, 0.5,   0,   0,   0],
             [  0,   0,   0, 0.5, 0.5,   0],
             [  0,   0,   0,   0, 0.5, 0.5],
             # [  0,   0,   0,   0,   1,   0],
             # [  0,   0,   0,   0, 0.6,   0],
             [  0,   0,   0,   0,   0,   0],
             [  0, 0.2, 0.4, 0.4,   0,   0]
             ]
    r_s = [-0.5, -1.5, -1, 5.5, 0, 0]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=1,
                        s_names=s_names, symbol=True)
    # display(s_vals)
    for k, v in s_vals.items():
        print(k, v)
    # '''
    
    '''
    # 求状态价值（评估）--------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3', 'Pub']
    p_s2s = [[0.5, 0.5,   0,   0,   0],
             [0.5,   0, 0.5,   0,   0],
             [  0,   0,   0, 0.5,   0],
             [  0,   0,   0,   0, 0.5],
             [  0, 0.2, 0.4, 0.4,   0]
             ]
    r_s = [-0.5, -1.5, -1, 5.5, 0]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=1,
                        s_names=s_names, symbol=False)
    # display(s_vals)
    for k, v in s_vals.items():
        print(k, v)
    # '''
    
    '''
    # 求解最优策略-------------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3', 'Slp']
    a_names = ['Keep', 'Quit']
    a, b, c, d, e = symbols('a b c d e')
    pi_s2a = [[1-a,   a],
              [  b, 1-b,],
              [  c, 1-c],
              [  d, 1-d],
              # [  e, 1-e]
              [  0,   0]
              # [  1,   0]
              # [0.5, 0.5]
              # [0.3, 0.7]
              ]
    p_sa2s = [[1,   0,   0,   0,   0],
              [0,   1,   0,   0,   0],
              [0,   0,   1,   0,   0],
              [1,   0,   0,   0,   0],
              [0,   0,   0,   1,   0],
              [0,   0,   0,   0,   1],
              [0,   0,   0,   0,   1],
              [0, 0.1, 0.2, 0.2,   0],
              # [0,   0,   0,   0,   1],
              [0,   0,   0,   0,   0],
              [0,   0,   0,   0,   0]
              ]
    r_sa2s = [[-1,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0],
              [ 0,  0, -2,  0,  0],
              [-1,  0,  0,  0,  0],
              [ 0,  0,  0, -2,  0],
              [ 0,  0,  0,  0,  0],
              [ 0,  0,  0,  0, 10],
              [ 0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0]
              ]
    gamma = 1
    vals, system = bellman_sas(
                    pi_s2a, p_sa2s, r_sa2s, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    for k, v in vals.items():        
        # display(k, v)
        print(k, ':  ', v.subs([(a, 1), 
                                (b, 1),
                                (c, 1),
                                (d, 1),
                                (e, 1)]))
        
    # 线性规划求解
    v_s, v_sa = get_best_bellman_linprog(p_sa2s, r_sa2s,
                                         gamma=gamma,
                                         weights=None)
    print(v_s)
    print(v_sa)
    # '''
    
    '''
    # 求解最优策略-------------------------------------------
    s_names = ['Fb', 'S1', 'S2', 'S3', 'Slp', 'Pub']
    a_names = ['Keep', 'Quit']
    a, b, c, d, e, f = symbols('a b c d e f')
    pi_s2a = [[1-a,   a],
              [  b, 1-b],
              [  c, 1-c],
              [  d, 1-d],
              [  0,   0],
              # [0.5, 0.5],
              # [  e, 1-e],
              [1-f,   f]]
    p_sa2s = [[1,   0,   0,   0,   0,   0],
              [0,   1,   0,   0,   0,   0],
              [0,   0,   1,   0,   0,   0],
              [1,   0,   0,   0,   0,   0],
              [0,   0,   0,   1,   0,   0],
              [0,   0,   0,   0,   1,   0],
              [0,   0,   0,   0,   1,   0],
              [0,   0,   0,   0,   0,   1],
              [0,   0,   0,   0,   1,   0],
              [0,   0,   0,   0,   0,   0],
              [0,   0,   0,   0,   0,   0],
              [0, 0.1, 0.2, 0.2,   0,   0],
              # [0, 0.2, 0.4, 0.4,   0,   0]
              ]
    r_sa2s = [[-1,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0, -2,  0,  0,  0],
              [-1,  0,  0,  0,  0,  0],
              [ 0,  0,  0, -2,  0,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0, 10,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0]
              ]
    gamma = 1
    vals, system = bellman_sas(
                    pi_s2a, p_sa2s, r_sa2s, gamma,
                    s_names=s_names, a_names=a_names,
                    symbol=True)
    for k, v in vals.items():        
        # display(k, v)
        print(k, ':  ', v.subs([(a, 1), 
                                (b, 1),
                                (c, 1),
                                (d, 1),
                                (e, 1),
                                (f, 1)]))
        
    # 线性规划求解
    v_s, v_sa = get_best_bellman_linprog(p_sa2s, r_sa2s,
                                         gamma=gamma,
                                         weights=None)
    print(v_s)
    print(v_sa)
    # '''
    
    #%%
    '''
    # 悬崖寻路----------------------------------------------
    try:
        import gymnasium as gym
    except:
        import gym
    env = gym.make('CliffWalking-v0')
    p_sa2s = np.zeros((env.nS*env.nA, env.nS))
    r_sa2s = np.zeros((env.nS*env.nA, env.nS))
    k = 0
    for s in env.P:
        if s != 47: # 47是终点
            for a in env.P[s]:
                p_sa2s[k, env.P[s][a][0][1]] = env.P[s][a][0][0]
                r_sa2s[k, env.P[s][a][0][1]] = env.P[s][a][0][2]
                k += 1
    
    s_names = ['loc_%s'%x for x in range(env.nS)]
    a_names = ['^', '>', 'v', '<']
    n_s, n_a = len(s_names), len(a_names)
    gamma = 0.9
    
    def show_pi(pi_s2a, N=5, max_step=np.inf):
        # gym悬崖寻路可视化
        env = gym.make('CliffWalking-v0', render_mode='human')
        for n in range(N):
            observation, info = env.reset()
            n_step = 0
            while True:
                action = np.argmax(pi_s2a[observation])
                observation, reward, terminated, truncated, info = env.step(action)
                n_step += 1
                if n_step > max_step:
                    break
                if terminated or truncated:
                    break
        env.close()
    # '''
    
    '''
    # 随机策略
    for _ in range(10):
        pi_s2a = np.random.rand(n_s, n_a)
        pi_s2a[36, 0] = 1
        pi_s2a[(0, 12, 24), 3] = 0
        pi_s2a[(11, 23, 35), 1] = 0
        pi_s2a[tuple(range(0, 13)), 0] = 0
        pi_s2a[tuple(range(25, 36)), 2] = 0
        show_pi(pi_s2a, N=1, max_step=5)
    # '''
    
    '''
    # 线性规划求解
    v_s, v_sa = get_best_bellman_linprog(p_sa2s, r_sa2s,
                                         gamma=gamma,
                                         weights=None)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(v_sa.reshape(-1, env.nA))
    # 生成最优策略
    bests_a = np.array(v_sa).reshape(-1, n_a).argmax(axis=1)
    pi_s2a = np.eye(n_a)[bests_a]
    show_pi(pi_s2a, N=2)
    # '''
    
    '''
    # 动态规划求解（策略迭代）
    # 随机策略
    pi_s2a_rand = [rand_sum(1, env.nA, 0.0, 1.0) for _ in range(env.nS)]
    # 最优策略
    pi_s2a_best = np.eye(4)[v_sa.reshape(-1, env.nA).argmax(axis=1)]
    p_s2a = pi_s2a_rand
    # p_s2a = pi_s2a_best
    # 策略评估
    v_s, v_sa = get_sv_dp(p_s2a, p_sa2s, r_sa2s, gamma, max_iter=3000)
    # 策略优化提升（单步）
    best_pi_s2a, optimal = dp_improve_pi(p_s2a, v_sa)
    # 策略迭代提升求解
    pi_s2a, v_s, v_sa = dp_pi(
        p_sa2s, r_sa2s, gamma, pi_s2a=p_s2a, tol=1e-6,
        max_iter_est=2000, max_iter_impr=1000,
        s_names=None, a_names=None, show_step_est=1000,
        show_step=1000)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(np.array(v_sa).reshape(-1, env.nA))
    print('实际最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a_best.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    print('dp优化最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    # '''
    
    '''
    # 动态规划求解（价值迭代）
    pi_s2a, v_s, v_sa = dp_val(
        p_sa2s, r_sa2s, gamma, pi_s2a=p_s2a,
        s_names=None, a_names=None,
        tol=1e-6, max_iter=2000, show_step=1000)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(np.array(v_sa).reshape(-1, env.nA))
    print('实际最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a_best.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    print('dp优化最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    show_pi(pi_s2a)
    # '''
    
    #%%
    # 《动手学强化学习》第三章例子
    '''
    # 求状态价值（评估）--------------------------------------
    s_names = None
    p_s2s = [[0.9, 0.1, 0.0, 0.0, 0.0, 0.0],
             [0.5, 0.0, 0.5, 0.0, 0.0, 0.0],
             [0.0, 0.0, 0.0, 0.6, 0.0, 0.4],
             [0.0, 0.0, 0.0, 0.0, 0.3, 0.7],
             [0.0, 0.2, 0.3, 0.5, 0.0, 0.0],
             [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
             ]
    r_s = [-1, -2, -2, 10, 1, 0]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=0.5,
                        s_names=s_names, symbol=False)
    display(s_vals)
    # '''
    
    '''
    # 给定策略求状态价值（评估）-------------------------------
    s_names = None
    p_s2s = [[0.5, 0.5, 0.0, 0.0, 0.0],
             [0.5, 0.0, 0.5, 0.0, 0.0,],
             [0.0, 0.0, 0.0, 0.5, 0.5],
             [0.0, 0.1, 0.2, 0.2, 0.5],
             [0.0, 0.0, 0.0, 0.0, 1.0]
             ]
    r_s = [-0.5, -1.5, -1.0, 5.5, 0]    
    # 给定策略下状态价值计算
    s_vals, system = bellman_ss_sv(
                        p_s2s, r_s, gamma=0.5,
                        s_names=s_names, symbol=False)
    display(s_vals)
    # '''
    
    '''
    # 蒙特卡洛估计状态价值
    s_names = ['s1', 's2', 's3', 's4', 's5']
    a_names = ['keep', 'quit']
    s_stop = 's5'
    gamma = 0.8
    max_step = 20
    n = 1000
    p_sa2s = [[1.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 1.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 1.0, 0.0, 0.0],
              [1.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 1.0],
              [0.0, 0.0, 0.0, 0.0, 1.0],
              [0.0, 0.2, 0.4, 0.4, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0]
              ]
    r_sa2s = [[-1,   0,   0,   0,  0],
              [ 0,   0,   0,   0,  0],
              [ 0,   0,  -2,   0,  0],
              [-1,   0,   0,   0,  0],
              [ 0,   0,   0,  -2,  0],
              [ 0,   0,   0,   0,  0],
              [ 0,   0,   0,   0, 10],
              # [ 0, 0.2, 0.4, 0.4,  0],
              [0,    0,   0,   0,   0],
              [ 0,   0,   0,   0,  0],
              [ 0,   0,   0,   0,  0]
              ]
    pi_s2a_1 = [[0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5],
                [0.5, 0.5]
                ]
    pi_s2a_2 = [[0.6, 0.4],
                [0.7, 0.3],
                [0.5, 0.5],
                [0.1, 0.9],
                [0.0, 0.0]
                ]
    
    s_vals, routes = get_sv_mc(pi_s2a_1, p_sa2s, r_sa2s, gamma,
                               max_step, n=n, s_names=s_names,
                               a_names=a_names, s_stop=s_stop,
                               first_visit=True)
    display(s_vals)
    
    # 与贝尔曼方程评估比较
    s_vals_blm, system = bellman_sas(pi_s2a_1, p_sa2s, r_sa2s, gamma,
                                 s_names=s_names, a_names=a_names, symbol=False)
    display(s_vals_blm)
    # '''
    
    
    '''
    # 占用度量
    routes1 = routes
    s_vals2, routes2 = get_sv_mc(pi_s2a_2, p_sa2s, r_sa2s, gamma,
                                 max_step, n=n, s_names=s_names,
                                 a_names=a_names, s_stop=s_stop)
    display(s_vals2)
    s, a = 's4', 'quit'
    rho1 = get_occupancy(routes1, s, a, max_step, gamma)
    rho2 = get_occupancy(routes2, s, a, max_step, gamma)
    display(rho1, rho2)
    
    rhos = []
    for s, a in product(s_names, a_names):
        rho = get_occupancy(routes2, s, a, max_step, gamma)
        rhos.append([s, a, rho])
    rhos = pd.DataFrame(rhos, columns=['s', 'a', 'rho'])
    print(rhos['rho'].sum())
    # '''

    #%%
    '''
    # 冰湖游戏----------------------------------------------
    try:
        import gymnasium as gym
    except:
        import gym
    env = gym.make('FrozenLake-v1')
    n_s = env.observation_space.n
    n_a = env.action_space.n
    p_sa2s = np.zeros((n_s*n_a, n_s))
    r_sa2s = np.zeros((n_s*n_a, n_s))
    k = 0
    for s in env.P:
        for a in env.P[s]:
            for s_ in env.P[s][a]:
                p_sa2s[k, s_[1]] = s_[0]
                r_sa2s[k, s_[1]] = s_[2]
            k += 1

    s_names = ['loc_%s'%x for x in range(n_s)]
    a_names = ['<', 'v', '>', '^']
    gamma = 1.0

    def show_pi(pi_s2a, N=5, max_step=np.inf):
        # gym冰湖游戏可视化
        env = gym.make('FrozenLake-v1', render_mode='human')
        n_win = 0
        for n in range(N):
            observation, info = env.reset()
            n_step = 0
            while True:
                action = np.argmax(pi_s2a[observation])
                observation, reward, terminated, truncated, info = env.step(action)
                n_step += 1
                if n_step > max_step:
                    break
                if terminated or truncated:
                    if reward > 0:
                        n_win += 1
                    break
        print('n_win: {}/{}'.format(n_win, N))
        env.close()
    # '''

    '''
    # 随机策略
    for _ in range(10):
        pi_s2a = np.random.rand(n_s, n_a)
        show_pi(pi_s2a, N=1, max_step=5)
    # '''

    '''
    # 动态规划求解（策略迭代）
    # 随机策略
    pi_s2a_rand = [rand_sum(1, n_a, 0.0, 1.0) for _ in range(n_s)]
    p_s2a = pi_s2a_rand
    # 策略评估
    v_s, v_sa = get_sv_dp(p_s2a, p_sa2s, r_sa2s, gamma, max_iter=3000)
    # 策略优化提升（单步）
    best_pi_s2a, optimal = dp_improve_pi(p_s2a, v_sa)
    # 策略迭代提升求解
    pi_s2a, v_s, v_sa = dp_pi(
        p_sa2s, r_sa2s, gamma, pi_s2a=p_s2a, tol=1e-6,
        max_iter_est=2000, max_iter_impr=1000,
        s_names=None, a_names=None, show_step_est=1000,
        show_step=1000)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(np.array(v_sa).reshape(-1, n_a))
    print('dp优化最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    # show_pi(pi_s2a)
    # '''

    '''
    # 动态规划求解（价值迭代）
    pi_s2a, v_s, v_sa = dp_val(
        p_sa2s, r_sa2s, gamma, pi_s2a=p_s2a,
        s_names=None, a_names=None,
        tol=1e-6, max_iter=2000, show_step=1000)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(np.array(v_sa).reshape(-1, n_a))
    print('dp优化最佳策略: ')
    best_acts = [a_names[x] for x in pi_s2a.argmax(axis=1)]
    best_acts = np.array(best_acts).reshape(4, -1)
    print(best_acts)
    show_pi(pi_s2a)
    # '''
    
    '''
    # 线性规划求解，会失败（因为本身就没有唯一最优解？）
    v_s, v_sa = get_best_bellman_linprog(p_sa2s, r_sa2s,
                                          gamma=gamma,
                                          weights=None)
    print(np.array(v_s).reshape(4, -1).round(2))
    print(v_sa.reshape(-1, n_a))
    # 生成最优策略
    bests_a = np.array(v_sa).reshape(-1, n_a).argmax(axis=1)
    pi_s2a = np.eye(n_a)[bests_a]
    show_pi(pi_s2a, N=2)
    # '''
    
    #%%
    tr.used()
    