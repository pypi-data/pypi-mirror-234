# -*- coding: utf-8 -*-

import random
import numpy as np
import pandas as pd
from tqdm import tqdm
from beartype.typing import Union, Callable
try:
    import gymnasium as gym
except:
    import gym
from dramkit.gentools import isna
from dramkit.plottools import plot_series
from dramkit.rl.mcts import Node, MCTS
from dramkit.rl.utils_gym import init_s_a_np, show_pi
from dramkit.rl.gym_best_pi import get_best_pi

#%%
class MCTSGym(MCTS):
    
    def __init__(self,
                 env: Union[str, gym.Env],
                 s_shape: Union[int, tuple, list],
                 n_a: int,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.env = gym.make(env) if isinstance(env, str) else env
        self.s_shape = s_shape
        self.n_a = n_a
        self.v_s_a = init_s_a_np(self.s_shape, self.n_a)
        
    def get_unvisit_actions(self,
                            env: gym.Env,
                            node: Node) -> Union[list, None]:
        kid_acts = [x.action for x in self.tree.get_children_nodes(node)]
        return [x for x in range(self.n_a) if x not in kid_acts]
    
    def sim_until_over(self,
                       env: gym.Env,
                       node: Node,
                       max_step: int = 50,
                       r_sum: bool = False,
                       gamma: float = 1.0) -> Union[int, float]:
        '''从给定节点开始模拟直到结束，返回奖励'''
        n_step = 0
        reward = 0
        a = node.action
        if isna(a):
            a = np.random.choice(self.n_a)
        while n_step < max_step:
            s, r, end1, end2, info = env.step(a)
            if r_sum:
                reward += r*gamma
            else:
                reward = r
            n_step += 1
            if end1 or end2:
                break
            a = np.random.choice(self.n_a)
        return reward
    
    def train(self,
              n: int = 100,
              func_s_1st: Callable = None,
              n_sim: int = 50,
              p_explore: float = 1.0,
              c_ucb: Union[int, float] = 1.0,
              max_step: int = 50,
              r_sum: bool = False,
              gamma: float = 1.0,
              params_dict: dict = {}):
        self.set_params(params_dict)
        self.train_rewards = []
        self.train_routes = []
        for k in tqdm(range(n)):
            s, _ = self.env.reset()
            if not isna(func_s_1st):
                self.env, s = func_s_1st(self.env)
            route = []
            k_r = 0
            n_step = 0
            end = False
            node = self.check_root(self.env, func_s_1st)
            # TODO: 每次从已有树的节点中选择开始状态，有可能陷入局部搜索，有些状态无法被探索到
            # TODO: 但若每次都独立随机选择开始状态，可能导致每次循环生成不交叉或交叉的子树，因此需要想办法对子树进行合并
            if not isna(node.state_p):
                ids = list(self.tree.nodes.keys())
                unid = random.sample(ids, 1)[0]
                node = self.tree.nodes[unid]
            a, s = node.action, node.state
            if isna(a):
                node = self.uct(self.env,
                                node,
                                n_sim=n_sim,
                                p_explore=p_explore,
                                c_ucb=c_ucb,
                                sim_max_step=max_step,
                                r_sum=r_sum,
                                gamma=gamma)
                if isinstance(node, str):
                    break
                a, s = node.action, node.state
                self.v_s_a[node.state_p][a] = self.ucb(node, c=c_ucb)
            while (not end) and (n_step < max_step):
                s_next, r, terminated, truncated, _ = self.env.step(a)
                end = terminated or truncated
                k_r += gamma*r
                n_step += 1
                node = self.uct(self.env,
                                node,
                                n_sim=n_sim,
                                p_explore=p_explore,
                                c_ucb=c_ucb,
                                sim_max_step=max_step,
                                r_sum=r_sum,
                                gamma=gamma)
                if isinstance(node, str):
                    break
                a_next = node.action
                route.append((s, a, r, s_next, end, a_next))
                s, a = s_next, a_next
                self.v_s_a[node.state_p][a] = self.ucb(node, c=c_ucb)
            self.train_rewards.append(k_r)
            self.train_routes.append(route)
            
    def plot_train_rewards(self):
        df = pd.DataFrame({'r': self.train_rewards})
        df['n'] = range(1, df.shape[0]+1)
        df['r_cummean'] = df['r'].cumsum() / df['n']
        df['r_rollmean'] = df['r'].rolling(20).mean()
        plot_series(df, {'r': '-b', 'r_cummean': '-r',
                         'r_rollmean': '-g'})
    
    def decide(self, s, k_decay: int = 1):
        pass
    
#%%
if __name__ == '__main__':
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    # """
    env_name = 'FrozenLake-v1'
    # is_slippery = True
    is_slippery = False
    env = gym.make(env_name, is_slippery=is_slippery)
    
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
    
    
    self = MCTSGym(env=env,
                   s_shape=int(n_s),
                   n_a=int(n_a)
                   )
    
    n = 1
    n_sim = 100
    p_explore = 1.0
    c_ucb = 1.0
    max_step = 100
    sim_max_step = max_step
    r_sum = False
    gamma = 1.0
    params_dict = {}
    
    self.train(n=n,
                func_s_1st=func_s_1st,
                n_sim=n_sim,
                p_explore=p_explore,
                c_ucb=c_ucb,
                max_step=max_step,
                r_sum=r_sum,
                gamma=gamma
                )
    self.plot_train_rewards()
    
    # show_pi(env, self.v_s_a, N=50, max_step=max_step,
    #         render_mode=None)
    # pi_best = get_best_pi(env_name if is_slippery else env_name+'_noslip',
    #                       a_names=a_names)
    # show_pi(env, pi_best, N=50, is_pi=True,
    #         max_step=max_step, render_mode='human')
    
    # """
    
    #%%
    tr.used()
        
    
