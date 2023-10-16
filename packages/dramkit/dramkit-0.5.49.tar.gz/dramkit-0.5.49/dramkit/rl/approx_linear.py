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
from dramkit.rl.utils_gym import (Agent,
                                  RandomAgent,
                                  show_pi_agent)

#%%
class LinearSARSA(Agent):
    '''线性拟合方法+SARSA'''
    
    def __init__(self,
                 env: gym.Env,
                 n_a: int,
                 s_bounds: List[List[Union[np.float32, int, float]]],
                 n_tiles_per_dim: List[int] = None,
                 n_layer: int = 8,
                 expected: bool = False,
                 gamma: float = 1.0,
                 lr: float = 0.05,
                 epsilon: float = 0.05,
                 e_decaying: bool = False,
                 logger: logging.Logger = None
                 ):
        self.env = env
        self.n_a = n_a
        self.s_bounds = np.array(s_bounds)
        self.s_dim = self.s_bounds.shape[0]
        if isna(n_tiles_per_dim):
            n_tiles_per_dim = [8] * self.s_dim
        self.encoder = TileEncoder(n_tiles_per_dim, s_bounds, n_layer=n_layer)
        self.expected = expected
        self.gamma = gamma
        self.lr = lr
        self.epsilon = epsilon
        self.e_decaying = e_decaying
        self.w = np.zeros((self.encoder.n_all_tiles, self.n_a))
        
    def s2tiles(self, s):
        return self.encoder(s)
    
    def get_v_s_a(self, s, a):
        tiles = self.s2tiles(s)
        v_s = self.w[tiles, a].sum()
        return v_s
    
    def _cal_p_e(self, k_decay):
        if self.e_decaying:
            return self.epsilon / k_decay
        else:
            return self.epsilon
        
    def decide(self, s, k_decay=1):
        p_e = self._cal_p_e(k_decay)
        if np.random.uniform() < p_e:
            a = np.random.choice(range(self.n_a))
        else:
            v_s_a_ = [self.get_v_s_a(s, a) for a in range(self.n_a)]
            a_max_v = max(v_s_a_)
            a_bests = [i for i in range(len(v_s_a_)) if v_s_a_[i] == a_max_v]
            a = np.random.choice(a_bests)
        return a

    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        u = r + self.gamma * self.get_v_s_a(s_next, a_next) #* (1-end)
        tiles = self.s2tiles(s)
        self.w[tiles, a] += self.lr * (u - self.get_v_s_a(s, a))
        
    def train(self,
              n: int = 1000,
              max_step: int = np.inf,
              func_s_1st: Callable = None,
              params_dict: dict = {}):
        self.set_params(params_dict)
        self.train_rewards = []
        self.train_routes = []
        for k in tqdm(range(n)):
            s, _ = self.env.reset()
            if not isna(func_s_1st):
                env, s = func_s_1st(self.env)
            route = []
            k_r = 0
            n_step = 0
            a = self.decide(s, n_step+1)
            end = False
            while (not end) and (n_step < max_step):
                s_next, r, terminated, truncated, _ = self.env.step(a)
                end = terminated or truncated
                k_r += r
                n_step += 1
                # a_next仅在在线策略（单步和多步SARSA策略）中使用
                # 在离线策略（期望SARSA和QLearning）中不会使用
                if self.expected:
                    a_next = np.nan
                else:
                    a_next = self.decide(s_next, n_step+1)
                self.learn(s, a, r, s_next, end, a_next, n_step+1)
                # 如果是离线策略，新的动作在学习步骤完成之后选择
                if self.expected:
                    a_next = self.decide(s_next, n_step+1)
                route.append((s, a, r, s_next, end, a_next))
                s, a = s_next, a_next
            self.train_rewards.append(k_r)
            self.train_routes.append(route)
            
    def plot_train_rewards(self):
        df = pd.DataFrame({'r': self.train_rewards})
        df['n'] = range(1, df.shape[0]+1)
        df['r_cummean'] = df['r'].cumsum() / df['n']
        df['r_rollmean'] = df['r'].rolling(20).mean()
        plot_series(df, {'r': '-b', 'r_cummean': '-r',
                         'r_rollmean': '-g'})
        
#%%
class LinearSARSALambda(LinearSARSA):
    '''带资格迹'''
    
    def __init__(self,
                 *args,
                 lambd: float = 0.9,
                 beta: float = 0.0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.lambd = lambd
        self.beta = beta
        # 资格迹
        self.e = np.zeros((self.encoder.n_all_tiles, self.n_a))
                    
    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        # 更新资格迹
        self.e *= self.lambd * self.gamma
        tiles = self.s2tiles(s)
        self.e[tiles, a] = 1.0 + self.beta * self.e[tiles, a]
        # 更新价值权重
        u = r + self.gamma * self.get_v_s_a(s_next, a_next) #* (1 - end)
        td = u - self.get_v_s_a(s, a)
        self.w += (self.lr * td * self.e)
        if end:
            self.e = np.zeros_like(self.e)
    
#%%
if __name__ == '__main__':
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    # '''
    # 小车上山
    env_name = 'MountainCar-v0'
    env = gym.make(env_name)
    n_a = int(env.action_space.n)
    s_high, s_low = env.observation_space.high, env.observation_space.low
    s_bounds = [[float(s_low[0]), float(s_high[0])],
                [float(s_low[1]), float(s_high[1])]]
    
    rand_agent = RandomAgent(n_a=n_a)
    print('random ...')
    show_pi_agent(env_name, rand_agent, N=100,
                  render_mode=None, plot_rewards=False)
    # '''
    
    # '''
    # 线性近似最优策略求解
    # self = LinearSARSA(env, n_a, s_bounds,
    #                     expected=False,
    #                     lr=0.05,
    #                     epsilon=1.0,
    #                     e_decaying=True
    #                     )
    self = LinearSARSALambda(env, n_a, s_bounds,
                              lambd=0.9,
                              beta=0.5,
                              lr=0.03,
                              epsilon=0.01,
                              e_decaying=False,
                              )
    self.train(n=300)
    self.plot_train_rewards()
    show_pi_agent(env_name, self, N=100,
                  render_mode=None,
                  plot_rewards=False)
    # '''
    
    #%%
    # '''
    print(('线性拟合（实际上是通过砖瓦编码将连续观测变量转化为离散变量'
           '在观测环境为低维简单的情况下（如小车上山）有效果，'
           '在复杂情况下（如倒立摆游戏）几乎不太可能求得较优策略。'))
    # '''
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
    show_pi_agent(env_name, rand_agent, N=200,
                  render_mode=None, plot_rewards=True)
    # '''
    
    '''
    # 线性近似最优策略求解
    # self = LinearSARSA(env, n_a, s_bounds,
    #                     expected=False,
    #                     lr=0.1,
    #                     epsilon=0.01,
    #                     e_decaying=False,
    #                     n_tiles_per_dim=[8, 64, 8, 64]
    #                     )
    self = LinearSARSALambda(env, n_a, s_bounds,
                              lambd=0.9,
                              beta=0.5,
                              lr=0.03,
                              epsilon=0.01,
                              e_decaying=False,
                              n_tiles_per_dim=[8, 64, 8, 64]
                              )
    self.train(n=200)
    self.plot_train_rewards()
    show_pi_agent(env_name, self, N=100,
                  render_mode=None,
                  plot_rewards=False)
    # '''
    
    #%%
    tr.used()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    