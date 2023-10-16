# -*- coding: utf-8 -*-

try:
    import gymnasium as gym
except:
    import gym
    
import logging
from tqdm import tqdm
from collections import deque
from beartype.typing import Union, List, Callable
import random
import numpy as np
import pandas as pd

from sklearn.linear_model import SGDRegressor as sgdr

from dramkit.gentools import isna, roulette_base
from dramkit.plottools.plot_common import plot_series

from dramkit.rl.tile_encode import TileEncoder
from dramkit.rl.utils_rl import PlayBackPool
from dramkit.rl.utils_gym import (Agent,
                                  RandomAgent,
                                  show_pi_agent)
    
#%%
class DQN(Agent):
    '''sklearn中的机器学习模型+Q学习'''
    
    def __init__(self,
                 *args,
                 pool_size=20000,
                 batch_size=50,
                 gap_step=10,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.mdls = {a: sgdr() for a in range(self.n_a)}
        self.mdls_tgt = {a: sgdr() for a in range(self.n_a)}
        for a in range(self.n_a):
            self.mdls[a].intercept_ = np.array([0.0])
            self.mdls_tgt[a].intercept_ = np.array([0.0])
            self.mdls[a].coef_ = np.zeros(self.s_dim)
            self.mdls_tgt[a].coef_ = np.zeros(self.s_dim)
        self.pool_size = pool_size
        self.batch_size = batch_size
        self.gap_step = gap_step
        # self.pools = {a: PlayBackPool(self.pool_size) for a in range(self.n_a)}
        self.pools = PlayBackPool(self.pool_size)
        # self.gaps = {a: 0 for a in range(self.n_a)}
        self.gaps = 0
        self.n_learn = 0
        self.expected = True
    
    # def get_v_s_a(self, s, a, tgt=False):
    #     if self.pools[a].size >= self.batch_size:
    #         if not tgt:
    #             return self.mdls[a].predict(np.array(s).reshape(1, -1))[0]
    #         return self.mdls_tgt[a].predict(np.array(s).reshape(1, -1))[0]
    #     return 0.0
    def get_v_s_a(self, s, a, tgt=False):
        if self.pools.size >= self.batch_size:
            if not tgt:
                return self.mdls[a].predict(np.array(s).reshape(1, -1))[0]
            return self.mdls_tgt[a].predict(np.array(s).reshape(1, -1))[0]
        return 0.0
    
    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        # self.pools[a].add(s, a, r, s_next, end)
        # self.gaps[a] += 1
        # if self.pools[a].size >= self.batch_size and self.gaps[a] >= self.gap_step:
        #     self.gaps[a] = 0
        #     _s, _a, _r, _s_next, _end = self.pools[a].sample(self.batch_size)
            
        # v_s_next_max = max([self.get_v_s_a(s_next, a_, tgt=True) for a_ in range(self.n_a)])
        # u = r + self.gamma * v_s_next_max #* (1-end)
        # # v_s = self.get_v_s_a(s, a)
        # # td = u - v_s
        # # v_s += self.lr * td
        # self.pools[a].add(s, u)
        # self.gaps[a] += 1
        # if self.pools[a].size >= self.batch_size and self.gaps[a] >= self.gap_step:
        #     x, y = self.pools[a].sample(self.batch_size)
        #     x, y = np.array(x), np.array(y)
        #     self.mdls[a].partial_fit(x, y)
        #     self.n_learn += 1
        #     self.gaps[a] = 0
        # if end:
        #     self.mdls_tgt = self.mdls.copy()
        
        v_s_next_max = max([self.get_v_s_a(s_next, a_, tgt=True) for a_ in range(self.n_a)])
        u = r + self.gamma * v_s_next_max #* (1-end)
        # v_s = self.get_v_s_a(s, a)
        # td = u - v_s
        # v_s += self.lr * td
        self.pools.add(s, u, a)
        self.gaps += 1
        if self.pools.size >= self.batch_size and self.gaps >= self.gap_step:
            x, y, _a = self.pools.sample(self.batch_size)
            for a in range(self.n_a):
                idxs = [i for i in range(len(_a)) if _a[i] == a]
                x_ = [x[i] for i in idxs]
                y_ = [y[i] for i in idxs]
                if len(y_) > 0:
                    x_, y_ = np.array(x_), np.array(y_)
                    self.mdls[a].partial_fit(x_, y_)
            self.n_learn += 1
            self.gaps = 0
        if end:
            self.mdls_tgt = self.mdls.copy()
    
#%%
if __name__ == '__main__':
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    '''
    # 倒立摆
    env_name = 'CartPole-v1'
    env = gym.make(env_name)
    n_a = int(env.action_space.n)
    s_high, s_low = env.observation_space.high, env.observation_space.low
    s_bounds = [[float(s_low[0]), float(s_high[0])],
                [float(s_low[1]), float(s_high[1])],
                [float(s_low[2]), float(s_high[2])],
                [float(s_low[3]), float(s_high[3])]]
    
    rand_agent = RandomAgent(n_a=n_a)
    print('random ...')
    show_pi_agent(env_name, rand_agent, N=1000,
                  render_mode=None, plot_rewards=True)
    # '''
    
    '''
    # 线性近似最优策略求解
    self = LinearSARSA(env, n_a, s_bounds,
                       expected=False,
                       lr=0.1,
                       epsilon=0.01,
                       e_decaying=False,
                       n_tiles_per_dim=[8, 64, 8, 64]
                       )
    # self = LinearSARSALambda(env, n_a, s_bounds,
    #                           lambd=0.9,
    #                           beta=0.5,
    #                           lr=0.03,
    #                           epsilon=0.01,
    #                           e_decaying=False,
    #                           )
    # self = DQL(env, n_a, s_bounds,
    #                  epsilon=0.01,
    #                  e_decaying=False
    #                  )
    self.train(n=1000)
    self.plot_train_rewards()
    show_pi_agent(env_name, self, N=100,
                  render_mode=None,
                  plot_rewards=False)
    # '''
    
    #%%
    '''
    # 小车上山
    env_name = 'MountainCar-v0'
    env = gym.make(env_name)
    n_a = int(env.action_space.n)
    s_high, s_low = env.observation_space.high, env.observation_space.low
    s_bounds = [[float(s_low[0]), float(s_high[0])],
                [float(s_low[1]), float(s_high[1])]]
    
    # rand_agent = RandomAgent(n_a=n_a)
    # print('random ...')
    # show_pi_agent(env_name, rand_agent, N=100,
    #               render_mode=None, plot_rewards=False)
    # '''
    
    '''
    # 线性近似最优策略求解
    # self = LinearSARSA(env, n_a, s_bounds,
    #                     expected=False,
    #                     lr=0.05,
    #                     epsilon=1.0,
    #                     e_decaying=True
    #                     )
    # self = LinearSARSALambda(env, n_a, s_bounds,
    #                           lambd=0.9,
    #                           beta=0.5,
    #                           lr=0.03,
    #                           epsilon=0.01,
    #                           e_decaying=False,
    #                           )
    self = DQL(env, n_a, s_bounds,
                     epsilon=0.01,
                     e_decaying=False
                     )
    self.train(n=100)
    self.plot_train_rewards()
    show_pi_agent(env_name, self, N=100,
                  render_mode=None,
                  plot_rewards=False)
    # '''
    
    #%%
    tr.used()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    