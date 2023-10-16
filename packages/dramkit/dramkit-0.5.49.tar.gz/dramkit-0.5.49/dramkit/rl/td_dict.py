# -*- coding: utf-8 -*-

try:
    import gymnasium as gym
except:
    import gym
from beartype import beartype
from beartype.typing import Union, Callable
import logging
import numpy as np
import pandas as pd
from tqdm import tqdm

from dramkit.gentools import (raise_error,
                              catch_error,
                              isna,
                              merge_dicts_act)
from dramkit.plottools.plot_common import plot_series
from dramkit.rl.utils_gym import (Agent,
                                  show_pi,
                                  show_pi_agent,
                                  choice_best_a)

#%%
def cal_v_s_a_sarsa(routes: list,
                    state_spaces: list,
                    action_spaces: list,
                    gamma: float,
                    lr: float = None,
                    playback_step: int = 1):
    '''
    根据采样路径列表routes估计状态-动作价值
    '''
    
    has_anext = len(routes[0][0]) == 6
    
    v_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    if isna(lr):
        n_s_a = {s: {a: 0 for a in action_spaces} for s in state_spaces}
    else:
        n_s_a = None
    
    def update_n_s_a(s, a):
        if isna(lr):
            n_s_a[s][a] += 1
    
    def _cal_lr(s, a):
        if isna(lr):
            return 1 / n_s_a[s][a]
        return lr
    
    if playback_step == 1:
        for route in routes:
            n = len(route)
            for k in range(n):
                if has_anext:
                    s, a, r, s_next, end, a_next = route[k]
                    u = r + gamma * v_s_a[s_next][a_next] #* (1-end)
                else:
                    s, a, r, s_next, end = route[k]
                    if k < n-1:
                        a_next = route[k+1][1]
                        u = r + gamma * v_s_a[s_next][a_next] #* (1-end)
                    else:
                        u = r
                update_n_s_a(s, a)
                v_s_a[s][a] += _cal_lr(s, a) * (u - v_s_a[s][a])
                # print(s, n_s_a[s], v_s_a[s])
    else:
        playback_pool = [] # 回放池
        for route in routes:
            n = len(route)
            for k in range(n):
                if has_anext:
                    s, a, r, s_next, end, a_next = route[k]
                else:
                    s, a, r, s_next, end = route[k]
                playback_pool.append((s, a, r)) 
                if len(playback_pool) == playback_step:
                    if has_anext:
                        u = v_s_a[s_next][a_next] # 最后（最新）一步奖励
                    else:
                        if k < n-1:
                            a_next = route[k+1][1]
                            u = v_s_a[s_next][a_next]
                        else:
                            u = 0
                    # 从后往前计算累计奖励
                    for i in range(playback_step-1, -1, -1):
                        _s, _a, _r = playback_pool[i]
                        u = _r + gamma * u
                        # 将结束之前的几步也更新
                        if end and i > 0:
                            update_n_s_a(_s, _a)
                            v_s_a[_s][_a] += _cal_lr(_s, _a) * (u - v_s_a[_s][_a])
                    s0, a0, r0 = playback_pool.pop(0)
                    update_n_s_a(s0, a0)
                    v_s_a[s0][a0] += _cal_lr(s0, a0) * (u - v_s_a[s0][a0])
                if end:
                    playback_pool = []
    
    return v_s_a
    
#%%
class TDBase(Agent):
    '''
    | 时序差分算法，基本算法
    | playback_step设置回放池步数，须>=1
    | expected为False时为普通SARSA算法（同策算法），为True时为期望SARSA算法（异策算法）
    | qlearning为True时为Q学习算法（Q学习可以看做期望SARSA算法的变形特例）
    '''
    
    @beartype
    def __init__(self,
                 env: gym.Env,
                 s_spaces: Union[list, tuple],
                 a_spaces: Union[list, tuple],
                 epsilon: float = 0.0,
                 e_decaying: bool = False,
                 gamma: float = 1.0,
                 lr: Union[float, None] = 0.1,
                 save_pi: bool = False,
                 a_names: Union[list, tuple] = None,
                 s_names: Union[list, tuple] = None,
                 playback_step: int = 1,
                 expected: bool = False,
                 qlearning: bool = False,
                 logger: logging.Logger = None,
                 **kwargs):
        attrs = locals().copy()
        kwargs = attrs.pop('kwargs')
        attrs.update(kwargs)
        self.set_params(attrs)
        
        self.n_s = len(self.s_spaces)
        self.n_a = len(self.a_spaces)
        self.v_s_a = {s: {a: 0 for a in self.a_spaces} 
                         for s in self.s_spaces}
        if isna(self.lr):
            self.n_s_a = {s: {a: 0 for a in self.a_spaces}
                             for s in self.s_spaces}
        if self.save_pi:
            self.pi_s_a = {s: {a: 1/self.n_a for a in self.a_spaces} 
                              for s in self.s_spaces}
        if self.playback_step < 1:
            raise_error('PlaybackStepError', '多步时序差分算法中的回放步数不能小于1！', logger=self.logger)
        if self.playback_step > 1:
            self.playback_pool = []
        if self.qlearning:
            self.expected = True # Q-learning是期望SARSA的变形（特例）
        
    def set_params(self, params_dict: dict):
        '''设置或修改属性'''
        if 'logger' in params_dict:
            logger = params_dict.pop('logger')
            self.logger = logger
        _in_attrs = []
        for attr in _in_attrs:
            if attr in params_dict:
                raise_error('AttrsSetError',
                            '禁止设置属性`{}`'.format(attr),
                            logger=self.logger)                
        for k, v in params_dict.items():
            if not k == 'self':
                self.__dict__[k] = v
                
    @catch_error()
    def call_self_func(self,
                       funcname: str,
                       *args,
                       logger:logging.Logger = None,
                       **kwargs):
        return eval('self.{}(*args, **kwargs)'.format(funcname))
    
    def _cal_p_e(self, k_decay):
        if self.e_decaying:
            return self.epsilon / k_decay
        else:
            return self.epsilon
        
    def _cal_lr(self, s, a):
        if isna(self.lr):
            return 1 / self.n_s_a[s][a]
        return self.lr
            
    def decide(self, s, k_decay: int = 1):
        '''
        | 动作选择
        | 若有策略概率矩阵，则根据概率矩阵选择，否则用epsilon探索方案选择
        | 若采取其它动作选择方案，则需自定义重写该函数
        '''
        if 'pi_s_a' in self.__dict__:
            a = np.random.choice(list(self.pi_s_a[s].keys()),
                                 p=list(self.pi_s_a[s].values()))
        else:
            p_e = self._cal_p_e(k_decay)
            if np.random.uniform() < p_e:
                a = np.random.choice(self.a_spaces)
            else:
                a = choice_best_a(self.v_s_a, s, is_pi=False,
                                  maxs_1st=False)
        return a
    
    def update_n_s_a(self, s, a):
        if 'n_s_a' in self.__dict__:
            self.n_s_a[s][a] += 1
    
    def update_pi(self, s, a, k_decay: int = 1):
        p_e = self._cal_p_e(k_decay)
        for _a in self.pi_s_a[s]:
            self.pi_s_a[s][_a] = p_e / self.n_a
        # # 同时存在多个最大动作价值取第一个
        # a_best = max(self.v_s_a[s], key=self.v_s_a[s].get)
        # self.pi_s_a[s][a_best] += (1 - p_e)
        # 同时存在多个最大动作价值，概率平均分配
        a_max_v = max(self.v_s_a[s].values())
        a_bests = [_a for _a, _v in self.v_s_a[s].items() if _v == a_max_v]
        for _a in a_bests:
            self.pi_s_a[s][_a] += (1 - p_e) / len(a_bests)
            
    def _cal_v_s(self, s, k_decay):
        s_max = max(self.v_s_a[s].values())
        if self.qlearning:
            return s_max
        p_e = self._cal_p_e(k_decay)
        s_mean = np.mean(list(self.v_s_a[s].values()))
        v_s = s_mean * p_e + s_max * (1 - p_e)
        return v_s
        
    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        if self.playback_step == 1:
            if not self.expected:
                u = r + self.gamma * self.v_s_a[s_next][a_next] #* (1 - end)
            else:
                v_s_next = self._cal_v_s(s_next, k_decay)
                u = r + self.gamma * v_s_next #* (1 - end)
            self.update_n_s_a(s, a)
            self.v_s_a[s][a] += self._cal_lr(s, a) * (u - self.v_s_a[s][a])
        else:
            self.playback_pool.append((s, a, r)) # 回放池
            if len(self.playback_pool) == self.playback_step:
                if not self.expected:
                    u = self.v_s_a[s_next][a_next] # 最后（最新）一步奖励
                else:
                    u = self._cal_v_s(s_next, k_decay) # 最新一步所在的状态价值
                # 从后往前计算累计奖励
                for i in range(self.playback_step-1, -1, -1):
                    _s, _a, _r = self.playback_pool[i]
                    u = _r + self.gamma * u
                    # 将结束之前的几步也更新（如果不更新的话下一次循环就更新不到了）
                    if end and i > 0:
                        self.update_n_s_a(_s, _a)
                        self.v_s_a[_s][_a] += self._cal_lr(_s, _a) * (u - self.v_s_a[_s][_a])
                s0, a0, r0 = self.playback_pool.pop(0)
                self.update_n_s_a(s0, a0)
                self.v_s_a[s0][a0] += self._cal_lr(s0, a0) * (u - self.v_s_a[s0][a0])
            if end:
                self.playback_pool = []
        
    def train(self,
              n: int = 10000,
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
                    a_next = None
                else:
                    a_next = self.decide(s_next, n_step+1)
                self.learn(s, a, r, s_next, end, a_next, n_step+1)
                if self.save_pi:
                    self.call_self_func('update_pi', s, a, n_step, logger=self.logger)
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
        
    def _s_a_dict2df(self, s_a_dict):
        if isna(s_a_dict):
            return s_a_dict
        df = pd.DataFrame(s_a_dict).transpose()
        if not isna(self.a_names):
            df.columns = self.a_names
        if not isna(self.s_names):
            df.index = self.s_names
        return df
                
    @property
    def df_pi_s_a(self):
        if self.save_pi:
            return self._s_a_dict2df(self.pi_s_a)
        return None
        
    @property
    def df_v_s_a(self):
        return self._s_a_dict2df(self.v_s_a)
    
    @property
    def df_n_s_a(self):
        if 'n_s_a' in self.__dict__:
            return self._s_a_dict2df(self.n_s_a)
        return None
    
#%%
class OffSARSA(TDBase):
    '''异策时序差分算法'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError
        
#%%
class DoubleQLearning(TDBase):
    '''双重Q学习'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.qlearning = True
        self.expected = True # 双重Q-Learning也是期望SARSA算法特例
        self.v_s_a_0 = {s: {a: 0 for a in self.a_spaces} 
                            for s in self.s_spaces}
        self.v_s_a_1 = {s: {a: 0 for a in self.a_spaces} 
                            for s in self.s_spaces}
        
    def _cal_v_s(self, s):
        a_max = choice_best_a(self.v_s_a_0, s,
                              is_pi=False, maxs_1st=False)
        return self.v_s_a_1[s][a_max]
        
    def _cal_lr(self, s, a):
        if isna(self.lr):
            # 因为两个策略共用一个计数，故学习率衰减要进行纠正，正常应该乘2
            # 不过乘2调整之后学习率仍然衰减太快，导致陷入局部最优，
            # 手动将学习率调高，更容易学习到较优策略
            # lr_adj = 2
            lr_adj = 200
            return min(lr_adj * 1/self.n_s_a[s][a], 1)
        return self.lr
        
    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        # 随机选择一个策略（状态-动作价值表）进行更新
        if np.random.randint(0, 2):
            self.v_s_a_0, self.v_s_a_1 = self.v_s_a_1, self.v_s_a_0
        if self.playback_step == 1:
            v_s_next = self._cal_v_s(s_next)
            u = r + self.gamma * v_s_next #* (1 - end)
            self.update_n_s_a(s, a)
            self.v_s_a_0[s][a] += self._cal_lr(s, a) * (u - self.v_s_a_0[s][a])
            self.v_s_a[s][a] = self.v_s_a_0[s][a] + self.v_s_a_1[s][a]
        else:
            self.playback_pool.append((s, a, r)) # 回放池
            if len(self.playback_pool) == self.playback_step:
                u = self._cal_v_s(s_next)
                # 从后往前计算累计奖励
                for i in range(self.playback_step-1, -1, -1):
                    _s, _a, _r = self.playback_pool[i]
                    u = _r + self.gamma * u
                    # 将结束之前的几步也更新（如果不更新的话下一次循环就更新不到了）
                    if end and i > 0:
                        self.update_n_s_a(_s, _a)
                        self.v_s_a_0[_s][_a] += self._cal_lr(_s, _a) * (u - self.v_s_a_0[_s][_a])
                        self.v_s_a[_s][_a] = self.v_s_a_0[_s][_a] + self.v_s_a_1[_s][_a]
                s0, a0, r0 = self.playback_pool.pop(0)
                self.update_n_s_a(s0, a0)
                self.v_s_a_0[s0][a0] += self._cal_lr(s0, a0) * (u - self.v_s_a_0[s0][a0])
                self.v_s_a[s0][a0] = self.v_s_a_0[s0][a0] + self.v_s_a_1[s0][a0]
            if end:
                self.playback_pool = []
                
#%%
class SARSALambda(TDBase):
    '''资格迹算法'''
    
    def __init__(self,
                 *args,
                 lambd: float = 0.6,
                 beta: float = 1.0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.lambd = lambd
        self.beta = beta
        self.expected = False
        self.qlearning = False # TODO: 资格计算法+Q学习
        self.playback_step = 1 # TODO: 资格迹算法+多步历史回放
        assert not isna(self.lr) # TODO: 学习率改为衰减方式效果如何？
        self.e = {s: {a: 0 for a in self.a_spaces}
                     for s in self.s_spaces}
        
    def learn(self, s, a, r, s_next, end, a_next, k_decay):
        '''策略学习'''
        # 更新资格迹
        self.e_pre = self.e.copy()
        self.e = {s: {a: self.gamma*self.lambd*self.e_pre[s][a] 
                         for a in self.a_spaces}
                     for s in self.s_spaces}
        self.e[s][a] = 1.0 + self.beta * self.e[s][a]
        # 更新价值
        u = r + self.gamma * self.v_s_a[s_next][a_next] #* (1 - end)
        self.v_s_a_pre = self.v_s_a.copy()
        self.v_s_a = {s: {a: self.v_s_a_pre[s][a]+self.lr*self.e[s][a]*(u-self.v_s_a_pre[s][a])
                             for a in self.a_spaces}
                         for s in self.s_spaces}
        if end:
            self.e = {s: {a: 0 for a in self.a_spaces}
                         for s in self.s_spaces}
        
#%%
if __name__ == '__main__':
    from dramkit.rl.gym_best_pi import get_best_pi
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    # '''
    # 悬崖寻路
    env_name = 'CliffWalking-v0'
    env = gym.make(env_name)
    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    
    s_spaces = list(range(s0, n_s))
    a_spaces = list(range(a0, n_a))
    a_names = ['^', '>', 'v', '<']
    
    # 最优策略
    pi_best = get_best_pi(env_name, a_names=a_names)
    # show_pi(env_name, pi_best, N=2)
    
    def func_s_1st(env):
        s = np.random.choice(s_spaces)
        env.env.env.s = s
        return env, s
    func_s_1st = None
    
    save_pi = True
    # save_pi = False
    max_step = 2000
    
    # self = TDBase(env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=0.9,
    #               epsilon=0.1,
    #               # epsilon=1.0,
    #               e_decaying=False,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=1,
    #               save_pi=save_pi,
    #               expected=True,
    #               qlearning=True,
    #               )
    # self = DoubleQLearning(
    #               env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=1.0,
    #               epsilon=0.1,
    #               # epsilon=1.0,
    #               e_decaying=False,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=5,
    #               save_pi=save_pi
    #               )
    self = SARSALambda(
                  env=env,
                  s_spaces=s_spaces,
                  a_spaces=a_spaces,
                  a_names = a_names,
                  gamma=1.0,
                  # epsilon=0.1,
                  epsilon=1.0,
                  e_decaying=True,
                  lr=0.1,
                  save_pi=save_pi,
                  lambd=0.6,
                  # beta=0.5
                  # beta=1.0 # 累计迹
                  # beta=1-0.1 # (1-lr)荷兰迹
                  beta=0.0 # 替换迹
                  )
    # TODO: 实验表明，n并不是越大越好（为啥？）
    # 单步双重Q学习训练次数要比较多才能找到较优策略？
    # 双重Q学习lr设置为None时很难找到较优策略，
    # 原因是学习率衰减太小之后容易陷入局部最优（把学习率强制提升之后能找到较优策略）？
    self.train(n=500, max_step=max_step, func_s_1st=func_s_1st)
    # show_pi(env_name, self.v_s_a, N=5, max_step=30,
    #         render_mode=None)
    show_pi_agent(env_name, self, N=5, max_step=30,
                  render_mode=None)
    pi = self.df_pi_s_a    
    self.plot_train_rewards()
    v_s_a = cal_v_s_a_sarsa(
                self.train_routes,
                self.s_spaces,
                self.a_spaces,
                self.gamma,
                lr=self.lr,
                playback_step=self.playback_step)
    v_s_a = self._s_a_dict2df(v_s_a)
    print((v_s_a-self.df_v_s_a).sum().sum())
    # '''
    
    #%%
    '''
    # 冰湖游戏
    env_name = 'FrozenLake-v1'
    env = gym.make(env_name)    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    s_spaces = list(range(s0, n_s))
    a_spaces = list(range(a0, n_a))
    a_names = ['<', 'v', '>', '^']
    
    def func_s_1st(env):
        s = np.random.choice(s_spaces)
        env.env.env.env.s = s
        return env, s
    # func_s_1st = None
    
    # save_pi = True
    save_pi = False
    max_step = 100
    
    # self = TDBase(env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=1.0,
    #               # epsilon=0.1,
    #               epsilon=1.0,
    #               e_decaying=True,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=1,
    #               save_pi=save_pi,
    #               expected=True,
    #               qlearning=True,
    #               )
    # self = DoubleQLearning(
    #               env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=1.0,
    #               # epsilon=0.1,
    #               epsilon=1.0,
    #               e_decaying=True,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=1,
    #               save_pi=save_pi
    #               )
    self = SARSALambda(
                  env=env,
                  s_spaces=s_spaces,
                  a_spaces=a_spaces,
                  a_names = a_names,
                  gamma=1.0,
                  # epsilon=0.1,
                  epsilon=1.0,
                  e_decaying=True,
                  lr=0.1,
                  save_pi=save_pi
                  )
    self.train(n=2000, max_step=max_step, func_s_1st=func_s_1st)
    show_pi(env_name, self.v_s_a, N=5, max_step=max_step,
            render_mode=None)
    pi = self.df_pi_s_a
    pi_best = get_best_pi(env_name, a_names=a_names)
    self.plot_train_rewards()
    # '''
    
    #%%
    '''
    # 出租车调度
    env_name = 'Taxi-v3'
    env = gym.make(env_name)    
    n_a, a0 = env.action_space.n, env.action_space.start
    n_s, s0 = env.observation_space.n, env.observation_space.start
    s_spaces = list(range(s0, n_s))
    a_spaces = list(range(a0, n_a))
    a_names = ['v', '^', '>', '<', 'p', 'd']
    
    def func_s_1st(env):
        s = np.random.choice(s_spaces)
        env.env.env.env.s = s
        return env, s
    func_s_1st = None
    
    # save_pi = True
    save_pi = False
    max_step = 100
    
    # self = TDBase(env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=0.9,
    #               epsilon=0.1,
    #               # epsilon=1.0,
    #               e_decaying=False,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=1,
    #               save_pi=save_pi,
    #               expected=True,
    #               qlearning=True,
    #               )
    # self = DoubleQLearning(
    #               env=env,
    #               s_spaces=s_spaces,
    #               a_spaces=a_spaces,
    #               a_names = a_names,
    #               gamma=0.9,
    #               epsilon=0.1,
    #               # epsilon=1.0,
    #               e_decaying=False,
    #               lr=0.1,
    #               # lr=None,
    #               playback_step=1,
    #               save_pi=save_pi
    #               )
    self = SARSALambda(
                  env=env,
                  s_spaces=s_spaces,
                  a_spaces=a_spaces,
                  a_names = a_names,
                  gamma=0.9,
                  epsilon=0.01,
                  # epsilon=1.0,
                  e_decaying=False,
                  lr=0.1,
                  save_pi=save_pi,
                  lambd=0.6,
                  beta=1.0,
                  )
    self.train(n=2000, max_step=max_step, func_s_1st=func_s_1st)
    show_pi(env_name, self.v_s_a, N=5, max_step=max_step,
            render_mode=None)
    pi = self.df_pi_s_a
    self.plot_train_rewards()
    # '''
    
    #%%
    tr.used()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

