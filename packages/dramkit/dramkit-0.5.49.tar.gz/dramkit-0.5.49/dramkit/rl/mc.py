# -*- coding: utf-8 -*-

from itertools import product
from beartype.typing import Callable
import numpy as np
from tqdm import tqdm
try:
    import gymnasium as gym
except:
    import gym
from dramkit.gentools import isna

from dramkit.rl.utils_gym import show_pi

#%%
def cal_v_s(routes: list,
            state_spaces: list,
            gamma: float,
            first_visit: bool = False,
            backtrack: bool = True):
    '''
    | 根据采样路径列表routes估计状态价值
    | 路径列表routes的每个元素为一条路径（也是一个列表）
    | 每条路径的元素为(s|状态, a|动作, r|奖励, snew|新状态, end|是否结束)五元组
    '''
    
    n_s = {s: 0 for s in state_spaces}
    v_s = {s: 0 for s in state_spaces}
    
    def _update(s, k_r):
        n_s[s] += 1
        v_s[s] += (k_r-v_s[s]) / n_s[s]
        return n_s, v_s
    
    if not first_visit:
        if backtrack:
            # 一条路径上从后往前计算状态价值
            for route in routes:
                k_r = 0
                for k in range(len(route)-1, -1, -1):
                    (s, a, r, s_, end) = route[k]
                    k_r = r + gamma * k_r # 步骤(时间)k的奖励
                    n_s, v_s = _update(s, k_r)
        else:
            # 一条路径上从前往后计算状态价值
            for route in routes:
                n_ = len(route)
                # 从前往后计算须先取出每个步骤(时间)的奖励
                r_route = [x[2] for x in route]
                for k in range(n_):
                    (s, a, r, s_, end) = route[k]
                    # 步骤(时间)k的奖励
                    k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
                    n_s, v_s = _update(s, k_r)
    else:
        for route in routes:
            k_r = 0
            route_r = []
            for k in range(len(route)-1, -1, -1):
                (s, a, r, s_, end) = route[k]
                k_r = r + gamma * k_r
                route_r.append((s, k_r))
            visited = {s: 0 for s in state_spaces}
            for s, k_r in route_r[::-1]:
                # 仅考虑首次访问
                if visited[s]:
                    break
                visited[s] = 1
                n_s, v_s = _update(s, k_r)

    return v_s


def cal_v_sa(routes: list,
             state_spaces: list,
             action_spaces: list,
             gamma: float,
             first_visit: bool = False,
             backtrack: bool = True):
    '''
    根据采样路径列表routes估计状态-动作价值
    '''
    
    sa_spaces = list(product(state_spaces, action_spaces))
    n_sa = {sa: 0 for sa in sa_spaces}
    v_sa = {sa: 0 for sa in sa_spaces}
    
    def _update(sa, k_r):
        n_sa[sa] += 1
        v_sa[sa] += (k_r-v_sa[sa]) / n_sa[sa]
        return n_sa, v_sa
    
    if not first_visit:
        if backtrack:
            # 从后往前计算
            for route in routes:
                k_r = 0
                for k in range(len(route)-1, -1, -1):
                    (s, a, r, s_, end) = route[k]
                    sa = (s, a)
                    k_r = r + gamma * k_r
                    n_sa, v_sa = _update(sa, k_r)
        else:
            # 从前往后计算
            for route in routes:
                n_ = len(route)
                r_route = [x[2] for x in route]
                for k in range(n_):
                    (s, a, r, s_, end) = route[k]
                    sa = (s, a)
                    k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
                    n_sa, v_sa = _update(sa, k_r)
    else:
        for route in routes:
            k_r = 0
            route_r = []
            for k in range(len(route)-1, -1, -1):
                (s, a, r, s_, end) = route[k]
                sa = (s, a)
                k_r = r + gamma * k_r
                route_r.append((sa, k_r))
            visited = {sa: 0 for sa in sa_spaces}
            for sa, k_r in route_r[::-1]:
                if visited[sa]:
                    break
                visited[sa] = 1
                n_sa, v_sa = _update(sa, k_r)

    return v_sa


def cal_v_s_a(routes: list,
              state_spaces: list,
              action_spaces: list,
              gamma: float,
              first_visit: bool = False,
              backtrack: bool = True):
    '''
    根据采样路径列表routes估计状态-动作价值
    '''
    
    n_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    v_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    
    def _update(s, a, k_r):
        n_s_a[s][a] += 1
        v_s_a[s][a] += (k_r-v_s_a[s][a]) / n_s_a[s][a]
        # print(s, n_s_a[s], v_s_a[s])
        return n_s_a, v_s_a
    
    if not first_visit:
        if backtrack:
            for route in routes:
                k_r = 0
                for k in range(len(route)-1, -1, -1):
                    (s, a, r, s_, end) = route[k]
                    k_r = r + gamma * k_r
                    n_s_a, v_s_a = _update(s, a, k_r)
        else:
            for route in routes:
                n_ = len(route)
                r_route = [x[2] for x in route]
                for k in range(n_):
                    (s, a, r, _, end) = route[k]
                    k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
                    n_s_a, v_s_a = _update(s, a, k_r)
    else:
        for route in routes:
            k_r = 0
            route_r = []
            for k in range(len(route)-1, -1, -1):
                (s, a, r, s_, end) = route[k]
                s_a = (s, a)
                k_r = r + gamma * k_r
                route_r.append((s_a, k_r))
            visited = {(s, a): 0 for a in action_spaces for s in state_spaces}
            for s_a, k_r in route_r[::-1]:
                if visited[s_a]:
                    break
                visited[s_a] = 1
                s, a = s_a
                n_s_a, v_s_a = _update(s, a, k_r)       
    
    return v_s_a


def v_sa_to_v_s(v_sa: dict, p_sa: dict):
    v_ = {sa: p_sa[sa]*v for sa, v in v_sa.items()}
    v_s = {s: 0 for (s, a) in v_.keys()}
    for (s, a), v in v_.items():
        v_s[s] += v
    return v_s


def v_s_a_to_v_s(v_s_a: dict, p_s_a: dict):
    v_s = {}
    for s in v_s_a:
        v_s[s] = sum([p_s_a[s][a]*v for a, v in v_s_a[s].items()])
    return v_s

#%%
def mcdp_epsilon_gym(env: gym.Env,
                     state_spaces: list,
                     action_spaces: list, 
                     p_s_a: dict = None,
                     gamma: float = 1.0,
                     n_mc: int = 10000,
                     max_step: int = 100,
                     epsilon: float = 0.1,
                     e_decaying: bool = False,
                     first_visit: bool = False,
                     backtrack: bool = True,
                     func_s_1st: Callable = None):
    '''
    epsilon探索更新
    
    Note
    ----
    epsilon衰减是按epsilon/k来计算的，若要普通衰减，应将epsilon设置为1.0
    '''
    
    n_a = len(action_spaces)
    n_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    v_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    if isna(p_s_a):
        p_s_a = {s: {a: 1/n_a for a in action_spaces} for s in state_spaces}
    
    def _update(s, a, k, k_r):
        n_s_a[s][a] += 1
        v_s_a[s][a] += (k_r-v_s_a[s][a]) / n_s_a[s][a]
        # 柔性贪婪探索策略更新
        epsilon_ = epsilon/(k+1) if e_decaying else epsilon
        for _a in p_s_a[s]:
            p_s_a[s][_a] = epsilon_ / n_a
        # # 同时存在多个最大动作价值取第一个
        # a_best = max(v_s_a[s], key=v_s_a[s].get)
        # p_s_a[s][a_best] += (1 - epsilon_)
        # 同时存在多个最大动作价值，概率平均分配
        a_max_v = max(v_s_a[s].values())
        a_bests = [_a for _a, _v in v_s_a[s].items() if _v == a_max_v]
        for _a in a_bests:
            p_s_a[s][_a] += (1 - epsilon_) / len(a_bests)
        return n_s_a, v_s_a, p_s_a
    
    routes = []
    for i in tqdm(range(n_mc)):
        # 一个回合
        n_step = 0
        route = []
        s, _ = env.reset()
        if not isna(func_s_1st):
            env, s = func_s_1st(env)
        while n_step < max_step:
            a = np.random.choice(list(p_s_a[s].keys()),
                                 p=list(p_s_a[s].values()))
            s_new, r, terminated, truncated, _ = env.step(a)
            end = terminated or truncated
            route.append((s, a, r, s_new, end))
            s = s_new
            if end:
                break # 回合结束
            n_step += 1
        routes.append(route)
        
        if not first_visit:
            if backtrack:
                k_r = 0
                for k in range(len(route)-1, -1, -1):
                    s, a, r, s_, end = route[k]
                    k_r = r + gamma * k_r
                    n_s_a, v_s_a, p_s_a = _update(s, a, k, k_r)
            else:
                n_ = len(route)
                r_route = [x[2] for x in route]
                for k in range(n_):
                    s, a, r, s_, end = route[k]
                    k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
                    n_s_a, v_s_a, p_s_a = _update(s, a, k, k_r)
        else:
            k_r = 0
            route_r = []
            for s, a, r, s_, end in route[::-1]:
                k_r = r + gamma * k_r
                route_r.append(((s, a), k_r))
            visited = {(s, a): 0 for a in action_spaces for s in state_spaces}
            k_ = len(route_r)
            for k in range(k_-1, -1, -1):
                (s, a), k_r = route_r[k]
                if visited[(s, a)]:
                    break
                visited[(s, 1)] = 1
                n_s_a, v_s_a, p_s_a = _update(s, a, k_-1-k, k_r)
    
    return p_s_a, v_s_a, routes

#%%
def mcdp_epsilon_rho_gym(env: gym.Env,
                         state_spaces: list,
                         action_spaces: list, 
                         p_s_a: dict = None,
                         p_s_a_b: dict = None,
                         gamma: float = None,
                         n_mc: int = 1000,
                         max_step: int = 100,
                         epsilon: float = 0.0,
                         e_decaying: bool = False,
                         rho: float = 1.0,
                         weight_rho: bool = True,
                         first_visit: bool = False,
                         backtrack: bool = True,
                         func_s_1st: Callable = None):
    
    n_a = len(action_spaces)
    n_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    v_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    if isna(p_s_a):
        p_s_a = {s: {a: 1/n_a for a in action_spaces} for s in state_spaces}
    if isna(p_s_a_b):
        p_s_a_b = {s: {a: 1/n_a for a in action_spaces} for s in state_spaces}
    
    def _update(s, a, k, k_r, rho):
        if weight_rho:
            n_s_a[s][a] += rho
            v_s_a[s][a] += (rho/n_s_a[s][a]) * (k_r-v_s_a[s][a])
        else:
            n_s_a[s][a] += 1
            v_s_a[s][a] += (rho*k_r-v_s_a[s][a]) / n_s_a[s][a]
        # 柔性贪婪探索策略更新
        epsilon_ = epsilon/(k+1) if e_decaying else epsilon
        for _a in p_s_a[s]:
            p_s_a[s][_a] = epsilon_ / n_a
        a_best = max(v_s_a[s], key=v_s_a[s].get)
        # # 同时存在多个最大动作价值取第一个
        # p_s_a[s][a_best] += (1 - epsilon_)
        # 同时存在多个最大动作价值，概率平均分配
        a_max_v = max(v_s_a[s].values())
        a_bests = [_a for _a, _v in v_s_a[s].items() if _v == a_max_v]
        for _a in a_bests:
            p_s_a[s][_a] += (1 - epsilon_) / len(a_bests)
        
        # TODO: 确认break条件是否正确
        # to_break = rho == 0
        to_break = a_best != a
        if not to_break:
            # TODO: 确认下面这个rho更新公式是否正确
            rho *= p_s_a[s][a] / p_s_a_b[s][a]
            # rho *= p_s_a[s][a_best] / p_s_a_b[s][a]

        return n_s_a, v_s_a, p_s_a, rho, to_break
    
    routes = []
    for i in tqdm(range(n_mc)):
        # 一个回合
        n_step = 0
        route = []
        s, _ = env.reset()
        if not isna(func_s_1st):
            env, s = func_s_1st(env)
        while n_step < max_step:
            a = np.random.choice(list(p_s_a[s].keys()),
                                 p=list(p_s_a[s].values()))
            s_new, r, terminated, truncated, _ = env.step(a)
            end = terminated or truncated
            route.append((s, a, r, s_new, end))
            s = s_new
            if end:
                break # 回合结束
            n_step += 1
        routes.append(route)
        
        if not first_visit:
            if backtrack:
                k_r = 0
                rho_ = rho
                for k in range(len(route)-1, -1, -1):
                    s, a, r, s_, end = route[k]
                    k_r = r + gamma * k_r
                    n_s_a, v_s_a, p_s_a, rho_, brk = _update(s, a, k, k_r, rho_)
                    if brk:
                        break
            else:
                n_ = len(route)
                r_route = [x[2] for x in route]
                rho_ = rho
                for k in range(n_):
                    s, a, r, s_, end = route[k]
                    k_r = sum([r_route[_]*gamma**(_-k) for _ in range(k, n_)])
                    n_s_a, v_s_a, p_s_a, rho_, brk = _update(s, a, k, k_r, rho_)
                    if brk:
                        break
        else:
            k_r = 0
            route_r = []
            for s, a, r, s_, end in route[::-1]:
                k_r = r + gamma * k_r
                route_r.append(((s, a), k_r))
            visited = {(s, a): 0 for a in action_spaces for s in state_spaces}
            k_ = len(route_r)
            rho_ = rho
            for k in range(k_-1, -1, -1):
                (s, a), k_r = route_r[k]
                if visited[(s, a)]:
                    break
                visited[(s, 1)] = 1
                n_s_a, v_s_a, p_s_a, rho_, brk = _update(s, a, k_-1-k, k_r, rho_)
                if brk:
                    break

    return p_s_a, v_s_a, routes

#%%
def get_routes_mc_gym(env: gym.Env,
                      state_spaces: list,
                      action_spaces: list, 
                      p_s_a: dict = None,
                      n_mc: int = 1000,
                      max_step: int = 100):
    n_a = len(action_spaces)
    if isna(p_s_a):
        p_s_a = {s: {a: 1/n_a for a in action_spaces} for s in state_spaces}
    routes = []
    for i in tqdm(range(n_mc)):
        # 一个回合
        n_step = 0
        route = []
        s, _ = env.reset()
        while n_step < max_step:
            a = np.random.choice(list(p_s_a[s].keys()),
                                 p=list(p_s_a[s].values()))
            s_new, r, terminated, truncated, _ = env.step(a)
            end = terminated or truncated
            route.append((s, a, r, s_new, end))
            s = s_new
            if end:
                break # 回合结束
            n_step += 1
        routes.append(route)
    return routes
    
#%%
def s_a_dict_to_df(dict_2d, s_names, a_names):
    res = pd.DataFrame(dict_2d).transpose()
    res.index = s_names
    res.columns = a_names
    return res

#%%
if __name__ == '__main__':
    import pandas as pd
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    '''
    # 饥饿游戏
    from dramkit.rl.env_hungrygame import HungryGamaEnv
    # env = HungryGamaEnv()
    env = HungryGamaEnv(p_he2f=1, p_fn2e=1)
    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    
    state_spaces = list(range(s0, n_s))
    action_spaces = list(range(a0, n_a))
    a_names = env.a_names
    a_map = dict(zip(action_spaces, a_names))
    s_names = env.s_names
    s_map = dict(zip(state_spaces, s_names))
    
    n_mc = 1000
    gamma = 4/5
    max_step = 30
    first_visit = False
    # '''
    
    '''
    # 随机策略
    print('pi_rand...')
    pi_rand = {s: {a: np.random.rand() for a in action_spaces} \
                  for s in state_spaces}
    for s in state_spaces:
        for a in action_spaces:
            psum = sum(pi_rand[s].values())
            pi_rand[s][a] = pi_rand[s][a] / psum
    routes_rand = get_routes_mc_gym(env, state_spaces, action_spaces, n_mc=n_mc)
    v_s_a_rand  = cal_v_s_a(routes_rand, state_spaces, action_spaces, gamma)
    v_s_rand = pd.Series(cal_v_s(routes_rand, state_spaces, gamma)).to_frame()
    v_s_a_rand = s_a_dict_to_df(v_s_a_rand, s_names, a_names)
    pi_rand = s_a_dict_to_df(pi_rand, s_names, a_names)
    print(v_s_a_rand)
    print(pi_rand)
    # '''
    
    '''
    # 同策略优化
    print('pi_on...')
    pi_on, v_s_a_on, routes_on = mcdp_epsilon_gym(
            env, state_spaces, action_spaces,
            n_mc = n_mc, max_step=max_step,
            first_visit=first_visit,
            gamma=gamma, epsilon=0.0, e_decaying=False)
    v_s_a_on = s_a_dict_to_df(v_s_a_on, s_names, a_names)
    pi_on = s_a_dict_to_df(pi_on, s_names, a_names)
    v_s_a_on1  = s_a_dict_to_df(
        cal_v_s_a(routes_on, state_spaces, action_spaces, gamma),
        s_names, a_names)
    print(v_s_a_on)
    print(pi_on)
    # '''
    
    '''
    # 异策略优化
    print('pi_off...')
    pi_off, v_s_a_off, routes_off = mcdp_epsilon_rho_gym(
            env, state_spaces, action_spaces,
            n_mc=n_mc, max_step=max_step,
            first_visit=first_visit,
            gamma=gamma, epsilon=0.0)
    v_s_a_off = s_a_dict_to_df(v_s_a_off, s_names, a_names)
    pi_off = s_a_dict_to_df(pi_off, s_names, a_names)
    v_s_a_off1  = s_a_dict_to_df(
        cal_v_s_a(routes_off, state_spaces, action_spaces, gamma),
        s_names, a_names)
    print(v_s_a_off)
    print(pi_off)
    # '''
    
    #%%
    '''
    # 21点扑克游戏
    env_name = 'Blackjack-v1'
    env = gym.make(env_name)
    
    n_a, a0 = env.action_space.n, env.action_space.start
    s1, s2, s3 = env.observation_space
    n_s1, n_s2, n_s3 = s1.n, s2.n, s3.n
    s10, s20, s30 = s1.start, s2.start, s3.start
    
    action_spaces = list(range(a0, n_a))
    state_spaces = list(product(
                            range(s10, n_s1),
                            # range(s10, 22),
                            range(s20, n_s2),
                            range(s30, n_s3)))
    s_names, a_names = state_spaces, action_spaces
    
    n_mc = 10000
    gamma = 1.0
    N = 1000
    render_mode = None
    # '''
    
    '''
    # 随机策略
    pi_rand = {s: {0: np.random.rand()} for s in state_spaces}
    for s in state_spaces:
        pi_rand[s][1] = 1-pi_rand[s][0]
    routes_rand = get_routes_mc_gym(env, state_spaces, action_spaces, n_mc=n_mc)
    v_s_a_rand  = cal_v_s_a(routes_rand, state_spaces, action_spaces, gamma)
    v_s_rand = pd.Series(cal_v_s(routes_rand, state_spaces, gamma)).to_frame()
    print('pi_rand...')
    show_pi(env_name, pi_rand, N=N, render_mode=render_mode)
    v_s_a_rand = s_a_dict_to_df(v_s_a_rand, s_names, a_names)
    pi_rand = s_a_dict_to_df(pi_rand, s_names, a_names)
    print(v_s_a_rand.max())
    # '''
    
    '''
    # 同策略优化
    pi_on, v_s_a_on, routes_on = mcdp_epsilon_gym(
            env, state_spaces, action_spaces, n_mc=n_mc,
            gamma=gamma, epsilon=0.1)
    print('pi_on...')
    show_pi(env_name, pi_on, N=N, render_mode=render_mode)
    v_s_a_on = s_a_dict_to_df(v_s_a_on, s_names, a_names)
    pi_on = s_a_dict_to_df(pi_on, s_names, a_names)
    print(v_s_a_on.max())
    # '''
    
    '''
    # 异策略优化
    pi_off, v_s_a_off, routes_off = mcdp_epsilon_rho_gym(
            env, state_spaces, action_spaces, n_mc=n_mc,
            gamma=gamma, epsilon=0.0)
    print('pi_off...')
    show_pi(env_name, pi_off, N=N, render_mode=render_mode)
    v_s_a_off = s_a_dict_to_df(v_s_a_off, s_names, a_names)
    pi_off = s_a_dict_to_df(pi_off, s_names, a_names)
    print(v_s_a_off.max())
    # '''
    
    #%%
    '''
    # 冰湖游戏
    env_name = 'FrozenLake-v1'
    env = gym.make(env_name)
    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    
    state_spaces = list(range(s0, n_s))
    action_spaces = list(range(a0, n_a))
    a_names = ['<', 'v', '>', '^']
    s_names = state_spaces
    
    n_mc = 10000
    gamma = 1.0
    render_mode = 'human'
    N = 5
    # max_step = np.inf
    max_step = 100
    # '''
    
    '''
    # 最优策略
    # https://zhuanlan.zhihu.com/p/554765525
    pi_best = {
        0:  {0:  1.0, 1:  0.0, 2:  0.0, 3:  0.0},
        1:  {0:  0.0, 1:  0.0, 2:  0.0, 3:  1.0},
        2:  {0:  0.0, 1:  0.0, 2:  0.0, 3:  1.0},
        3:  {0:  0.0, 1:  0.0, 2:  0.0, 3:  1.0},
        4:  {0:  1.0, 1:  0.0, 2:  0.0, 3:  0.0},
        5:  {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
        6:  {0:  1.0, 1:  0.0, 2:  0.0, 3:  0.0},
        7:  {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
        8:  {0:  0.0, 1:  0.0, 2:  0.0, 3:  1.0},
        9:  {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
        10: {0:  1.0, 1:  0.0, 2:  0.0, 3:  0.0},
        11: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
        12: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
        13: {0:  0.0, 1:  0.0, 2:  1.0, 3:  0.0},
        14: {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
        15: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
        }
    routes_best = get_routes_mc_gym(env, state_spaces, action_spaces, n_mc=n_mc)
    v_s_a_best  = cal_v_s_a(routes_best, state_spaces, action_spaces, gamma)
    v_s_best = cal_v_s(routes_best, state_spaces, gamma)
    print('pi_best...')
    # show_pi(env_name, pi_best, N=N, render_mode=render_mode,
    #         max_step=max_step)
    v_s_best = pd.Series(v_s_best).values.reshape(-1, 4).round(4)
    print('v_s_best:')
    print(v_s_best)
    v_s_a_best = s_a_dict_to_df(v_s_a_best, s_names, a_names)
    pi_best = s_a_dict_to_df(pi_best, s_names, a_names)
    # '''
    
    '''
    # 随机策略
    pi_rand = {s: {a: np.random.rand() for a in action_spaces} \
                  for s in state_spaces}
    for s in state_spaces:
        psum = sum(pi_rand[s].values())
        for a in action_spaces:
            pi_rand[s][a] = pi_rand[s][a] / psum
    routes_rand = get_routes_mc_gym(env, state_spaces, action_spaces, n_mc=n_mc)
    v_s_a_rand  = cal_v_s_a(routes_rand, state_spaces, action_spaces, gamma)
    v_s_rand = cal_v_s(routes_rand, state_spaces, gamma)
    print('pi_rand...')
    show_pi(env_name, pi_rand, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_rand = pd.Series(v_s_rand).to_frame()
    v_s_a_rand = s_a_dict_to_df(v_s_a_rand, s_names, a_names)
    pi_rand = s_a_dict_to_df(pi_rand, s_names, a_names)
    # '''
    
    '''
    # 同策略优化
    def func_s_1st(env):
        s = np.random.choice(state_spaces)
        env.env.env.env.s = s
        return env, s
    # func_s_1st = None
    pi_on, v_s_a_on, routes_on = mcdp_epsilon_gym(
            env, state_spaces, action_spaces,
            n_mc = n_mc, max_step=max_step,
            gamma=gamma, epsilon=1.0, e_decaying=True,
            func_s_1st=func_s_1st) # epsilon=1.0, e_decaying=True是最优参数
    print('pi_on...')
    show_pi(env_name, pi_on, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_a_on = s_a_dict_to_df(v_s_a_on, s_names, a_names)
    pi_on = s_a_dict_to_df(pi_on, s_names, a_names)
    # '''
    
    '''
    # 异策略优化
    def func_s_1st(env):
        s = np.random.choice(state_spaces)
        env.env.env.env.s = s
        return env, s
    # func_s_1st = None
    pi_off, v_s_a_off, routes_off = mcdp_epsilon_rho_gym(
            env, state_spaces, action_spaces,
            n_mc=n_mc, max_step=max_step, first_visit=True,
            gamma=gamma, epsilon=0.1, e_decaying=False,
            weight_rho=False, func_s_1st=func_s_1st)
    print('pi_off...')
    show_pi(env_name, pi_off, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_a_off = s_a_dict_to_df(v_s_a_off, s_names, a_names)
    pi_off = s_a_dict_to_df(pi_off, s_names, a_names)
    # '''
    
    #%%
    '''
    # 悬崖寻路
    env_name = 'CliffWalking-v0'
    env = gym.make(env_name)
    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    
    state_spaces = list(range(s0, n_s))
    action_spaces = list(range(a0, n_a))
    a_names = ['^', '>', 'v', '<']
    s_names = state_spaces
    
    n_mc = 1000
    gamma = 1.0
    # render_mode = 'human'
    render_mode = None
    N = 2
    max_step = 2000
    # max_step = np.inf
    # '''
    
    '''
    # 随机策略
    pi_rand = {s: {a: np.random.rand() for a in action_spaces} \
                  for s in state_spaces}
    pi_rand[36][0] = 1
    for s in [0, 12, 24]:
        pi_rand[s][3] = 0
    for s in [11, 23, 35]:
        pi_rand[s][1] = 0
    for s in range(0, 13):
        pi_rand[s][0] = 0
    for s in range(25, 36):
        pi_rand[s][2] = 0
    for s in state_spaces:
        psum = sum(pi_rand[s].values())
        for a in action_spaces:
            pi_rand[s][a] = pi_rand[s][a] / psum
    routes_rand = get_routes_mc_gym(env, state_spaces, action_spaces, n_mc=n_mc)
    v_s_a_rand  = cal_v_s_a(routes_rand, state_spaces, action_spaces, gamma)
    v_s_rand = cal_v_s(routes_rand, state_spaces, gamma)
    print('pi_rand...')
    show_pi(env_name, pi_rand, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_rand = pd.Series(v_s_rand).to_frame()
    v_s_a_rand = s_a_dict_to_df(v_s_a_rand, s_names, a_names)
    pi_rand = s_a_dict_to_df(pi_rand, s_names, a_names)
    # '''
    
    '''
    # 同策略优化
    def func_s_1st(env):
        s = np.random.choice(state_spaces)
        env.env.env.s = s
        return env, s
    # func_s_1st = None
    pi_on, v_s_a_on, routes_on = mcdp_epsilon_gym(
            env, state_spaces, action_spaces,
            n_mc = n_mc, max_step=max_step,
            gamma=gamma, epsilon=1.0, e_decaying=True,
            func_s_1st=func_s_1st)
    print('pi_on...')
    show_pi(env_name, pi_on, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_a_on = s_a_dict_to_df(v_s_a_on, s_names, a_names)
    pi_on = s_a_dict_to_df(pi_on, s_names, a_names)
    # '''
    
    '''
    # 异策略优化
    def func_s_1st(env):
        s = np.random.choice(state_spaces)
        env.env.env.s = s
        return env, s
    func_s_1st = None
    pi_off, v_s_a_off, routes_off = mcdp_epsilon_rho_gym(
            env, state_spaces, action_spaces,
            n_mc=n_mc, max_step=max_step, first_visit=False,
            gamma=gamma, epsilon=1.0, e_decaying=True,
            weight_rho=False, func_s_1st=func_s_1st)
    print('pi_off...')
    show_pi(env_name, pi_off, N=N, render_mode=render_mode,
            max_step=max_step)
    v_s_a_off = s_a_dict_to_df(v_s_a_off, s_names, a_names)
    pi_off = s_a_dict_to_df(pi_off, s_names, a_names)
    # '''
    
    #%%
    tr.used()











