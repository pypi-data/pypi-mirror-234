# -*- coding: utf-8 -*-

try:
    import gymnasium as gym
    from gymnasium.envs.toy_text.utils import categorical_sample
except:
    import gym
    from gym.envs.toy_text.utils import categorical_sample
import numpy as np
from dramkit.gentools import GenObject


class HungryGamaEnv(gym.Env):
    '''饥饿游戏，《强化学习-原理与Python实现》第二章例子'''
    
    def __init__(self, p_he2f=2/3, p_fn2e=3/4):
        self.spec = GenObject(id='HungryGame')
        
        self.p_he2f = p_he2f
        self.p_fn2e = p_fn2e
        self.n_s = 2
        self.n_a = 2
        self.observation_space = gym.spaces.Discrete(self.n_s)
        self.action_space = gym.spaces.Discrete(self.n_a)
        self.s_names = ['Hgry', 'Full']
        self.a_names = ['notEat', 'Eat']
        self.p_s_a_s = {
            0: {0: {0:        1, 1:        0},
                1: {0: 1-p_he2f, 1:   p_he2f}},
            1: {0: {0:   p_fn2e, 1: 1-p_fn2e},
                1: {0:        0, 1:        1}}
            }
        self.r_s_a_s = {
            0: {0: {0: -2, 1: 0},
                1: {0: -3, 1: 1}},
            1: {0: {0: -2, 1: 2},
                1: {0:  0, 1: 1}}
            }
        self.init_state_deistrib = np.ones(self.n_s) / self.n_s
        self.reset()
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        self.s = categorical_sample(
                 self.init_state_deistrib, self.np_random)
        return self.s, {'prob': self.init_state_deistrib[self.s]}
    
    def step(self, a):
        a_s = self.p_s_a_s[self.s][a]
        s = categorical_sample(
                 np.array(list(a_s.values())), self.np_random)
        r = self.r_s_a_s[self.s][a][s]
        return (s, r, False, False, {'prob': a_s[s]})
    
    def render(self):
        pass

