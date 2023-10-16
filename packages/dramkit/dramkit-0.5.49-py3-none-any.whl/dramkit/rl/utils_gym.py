# -*- coding: utf-8 -*-

try:
    import gymnasium as gym
except:
    import gym
import numpy as np
import pandas as pd
from beartype.typing import Union, Callable

from dramkit.gentools import (raise_error,
                              capture_print,
                              isna,
                              GenClass)
from dramkit.plottools.plot_common import plot_series


class Agent(GenClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def decide(self, s, k_decay: int = 1):
        pass
    
    def learn(self, *args, **kwargs):
        pass
    
    
class RandomAgent(Agent):
    '''随机选择动作'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def decide(self, s, k_decay: int = 1):
        return np.random.choice(range(self.n_a))
    
    
def init_s_a_np(s_shape: Union[int, tuple, list],
                n_a: int,
                v_init: Union[int, float] = 0):
    if isinstance(s_shape, int):
        s_a_shape = (s_shape, n_a)
    else:
        s_a_shape = tuple(list(s_shape) + [n_a])
    return v_init * np.ones(s_a_shape)


def choice_best_a(p_s_a: Union[dict, np.ndarray, pd.DataFrame],
                  s,
                  is_pi: bool = False,
                  maxs_1st: bool = False):
    if isinstance(p_s_a, pd.DataFrame):
        p_s_a = p_s_a.values
    if is_pi:
        if isinstance(p_s_a, np.ndarray):
            a = np.random.choice(list(range(len(p_s_a[s]))),
                                 p=p_s_a[s])
        else:
            a = np.random.choice(list(p_s_a[s].keys()),
                                 p=list(p_s_a[s].values()))
    else:
        if maxs_1st:
            # 同时存在多个最大动作价值取第一个
            if isinstance(p_s_a, np.ndarray):
                a = np.argmax(p_s_a[s])
            else:
                a = max(p_s_a[s], key=p_s_a[s].get)
        else:
            # 最大值有多个相等值时，随机选取
            if isinstance(p_s_a, np.ndarray):
                a_max_v = np.max(p_s_a[s])
                a_bests = np.where(p_s_a[s] == a_max_v)[0]
            else:
                a_max_v = max(p_s_a[s].values())
                a_bests = [_a for _a, _v in p_s_a[s].items() if _v == a_max_v]
            a = np.random.choice(a_bests)
    return a


# @capture_print()
def show_pi(env_name: Union[str, gym.Env],
            p_s_a: Union[dict, np.ndarray, pd.DataFrame],
            is_pi: bool = False,
            N: int = 1,
            max_step: int = np.inf,
            render_mode: Union[str, None] = 'human',
            show_nwin: bool = True,
            func_s2int: Callable = None,
            plot_rewards: bool = False,
            gamma: float = 1.0,
            **kwargs):
    # gym策略可视化
    def _s2int(s):
        if not isna(func_s2int):
            return func_s2int(s)
        return s
    assert isinstance(p_s_a, (np.ndarray, pd.DataFrame, dict))
    if isinstance(env_name, str):
        env = gym.make(env_name, render_mode=render_mode)
    elif isinstance(env_name, gym.Env):
        env = env_name
    else:
        raise_error('GymEnvError', '未识别的gym环境！')
    n_win = 0
    rewards = []
    for n in range(N):
        s, info = env.reset()
        s = _s2int(s)
        n_step = 0
        reward = 0
        while True:
            a = choice_best_a(p_s_a, s, is_pi=is_pi,
                              maxs_1st=False)
            s, r, terminated, truncated, info = env.step(a)
            reward += gamma*r
            s = _s2int(s)
            n_step += 1
            if n_step > max_step:
                break
            if terminated or truncated:
                if env.spec.id == 'CliffWalking-v0':
                    if r == -1:
                        n_win += 1
                elif env.spec.id == 'MountainCar-v0':
                    if n_step < 200:
                        n_win += 1
                elif env.spec.id == 'CartPole-v1':
                    if n_step >= 500:
                        n_win += 1
                else:
                    if r > 0:
                        n_win += 1                        
                break
        rewards.append(reward)
    if show_nwin:
        print('n_win: {}/{}'.format(n_win, N))
    if plot_rewards:
        df = pd.DataFrame({'r': rewards})
        df['n'] = range(1, df.shape[0]+1)
        df['r_cummean'] = df['r'].cumsum() / df['n']
        df['r_rollmean'] = df['r'].rolling(20).mean()
        plot_series(df, {'r': '-b', 'r_cummean': '-r',
                         'r_rollmean': '-g'})
    env.close()
    
    
# @capture_print()
def show_pi_agent(env_name: Union[str, gym.Env],
                  agent: Agent,
                  N: int = 1,
                  max_step: int = np.inf,
                  render_mode: Union[str, None] = 'human',
                  show_nwin: bool = True,
                  func_s2int: Callable = None,
                  plot_rewards: bool = False,
                  gamma: float = 1.0,
                  **kwargs):
    agent.epsilon = 0.0 # 取消探索
    def _s2int(s):
        if not isna(func_s2int):
            return func_s2int(s)
        return s
    if isinstance(env_name, str):
        env = gym.make(env_name, render_mode=render_mode)
    elif isinstance(env_name, gym.Env):
        env = env_name
    else:
        raise_error('GymEnvError', '未识别的gym环境！')
    n_win = 0
    rewards = []
    for n in range(N):
        s, info = env.reset()
        s = _s2int(s)
        n_step = 0
        reward = 0
        while True:
            a = agent.decide(s, n_step+1)
            s, r, terminated, truncated, info = env.step(a)
            reward += gamma*r
            s = _s2int(s)
            n_step += 1
            if n_step > max_step:
                break
            if terminated or truncated:
                if env.spec.id == 'CliffWalking-v0':
                    if r == -1:
                        n_win += 1
                elif env.spec.id == 'MountainCar-v0':
                    if n_step < 200:
                        n_win += 1
                elif env.spec.id == 'CartPole-v1':
                    if n_step >= 500:
                        n_win += 1
                else:
                    if r > 0:
                        n_win += 1
                break
        rewards.append(reward)
    if show_nwin:
        print('n_win: {}/{}'.format(n_win, N))
    if plot_rewards:
        df = pd.DataFrame({'r': rewards})
        df['n'] = range(1, df.shape[0]+1)
        df['r_cummean'] = df['r'].cumsum() / df['n']
        df['r_rollmean'] = df['r'].rolling(20).mean()
        plot_series(df, {'r': '-b', 'r_cummean': '-r',
                         'r_rollmean': '-g'})
    env.close()
    
    
def s_a_dict2df(s_a_dict, a_names=None, s_names=None):
    df = pd.DataFrame(s_a_dict).transpose()
    if not isna(a_names):
        df.columns = a_names
    if not isna(s_names):
        df.index = s_names
    return df

