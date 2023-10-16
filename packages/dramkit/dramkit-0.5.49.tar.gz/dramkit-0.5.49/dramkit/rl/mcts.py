# -*- coding: utf-8 -*-

import copy
import math
import numpy as np
from beartype.typing import Any, Union, List, Dict, Callable
try:
    import gymnasium as gym
except:
    import gym
from dramkit.gentools import (GenClass,
                              isna,
                              x_div_y)
from dramkit.datsci.utils_networkx import gen_digraph_edge_list
from dramkit.rl.utils_gym import Agent

#%%
class Node(GenClass):
    '''树的节点'''

    def __init__(self,
                 state_p: Any,
                 action: Any,
                 state: Any,
                 reward: Union[float, int],
                 terminal: bool,
                 func_unid: Callable = None,
                 **kwargs):
        super().__init__(**kwargs)
        # 节点id（唯一标识）
        if isna(func_unid):
            self.unid = (state_p, action, state)
        else:
            self.unid = func_unid(state_p, action, state)
        # 动作和状态：在状态state_p执行动作action，达到了状态state
        self.state_p = state_p
        self.action = action
        self.state = state
        self.terminal = terminal # 是否结束
        # 奖励：从采取动作action到达状态state获得的回报（即单步奖励）
        self.reward = reward
        self.rewards = [reward]
        # 访问次数：该节点及其下所有后续子节点完成一次模拟，该节点访问次数+1
        self.n_visit = 0
        # 累计回报：该节点及其下所有后续子节点完成一次模拟，累计相应奖励到该节点
        self.tot_sim_reward = 0 # 累计回报
        self.parent = None # 父节点id
        self.children = [] # 子节点id列表
        
    @property
    def n_child(self) -> int:
        return len(self.children)
    
    @property
    def mean_sim_reward(self) -> float:
        return  x_div_y(self.tot_sim_reward, self.n_visit, v_xy0=np.nan)

    def __repr__(self):
        '''print显示内容'''
        show_attrs = {'state_p': 's_p',
                      'action': 'a', 'state': 's',
                      'reward': 'r', 'terminal': 'end',
                      'n_child': 'n_child', 'n_visit': 'n_visit',
                      'mean_sim_reward': 'r_mean'}
        str_ = []
        for k in show_attrs:
            str_.append('{}: {}'.format(show_attrs[k], eval('self.%s'%k)))
        str_ = ', '.join(str_)
        return '(' + str_ + ')'

#%%
class Tree(GenClass):
    '''树'''
    
    def __init__(self,
                 root: Node = None,
                 nodes: Dict[str: Node] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.nodes = {} if isna(nodes) else nodes
        
    def add_node(self, node: Node, parent: Node = None):
        '''
        往树中添加节点
        '''
        unid = node.unid
        if unid in self.nodes:
            self.nodes[unid].rewards.append(node.reward)
            # 若node原来父节点为None（即node为根节点）且新的父节点不为None，父节点替换根节点
            if isna(self.nodes[unid].parent) and (not isna(parent)):
                p_unid = parent.unid
                # p_unid_old = self.nodes[unid].parent # 已有的父节点
                self.root = parent
                self.nodes[p_unid].parent = None # 根节点的父节点为None
            return self.nodes[unid]
        self.nodes[unid] = node
        if isna(parent):
            self.root = node # 只有根节点的父节点才为None
            self.nodes[unid].parent = None
        else:
            p_unid = parent.unid
            self.nodes[unid].parent = p_unid
            self.nodes[p_unid].children.append(unid)
        return node
    
    def get_children_unids(self, unid: tuple) -> List[tuple]:
        '''根据unid查询下级子节点unid'''
        return [self.nodes[i].unid for i in self.nodes[unid].children]

    def get_children_nodes(self, node: Node) -> List[Node]:
        '''获取（下一级）所有子节点列表'''
        return [self.nodes[i] for i in self.nodes[node.unid].children]

    def get_parent_node(self, node: Node) -> Union[Node, None]:
        '''获取父节点'''
        # 不能直接用p_unid=node.parent，因为要检查node是否已经加入了树
        p_unid = self.nodes[node.unid].parent
        if isna(p_unid):
            return None
        return self.nodes[p_unid]
    
    def tree2edges(self, unid: tuple = None, edges: list = None):
        '''树转化为图'''
        if isna(unid):
            unid = self.root.unid
        if isna(edges):
            edges = []
        node = self.nodes[unid]
        for child in node.children:
            edges.append((node, self.nodes[child]))
            self.tree2edges(child, edges)
        return edges
        
    def show(self, unid: tuple = None):
        '''可视化，自定义'''
        self.edges = self.tree2edges(unid)
        self.graph = gen_digraph_edge_list(self.edges)
        
#%%
class MCTS(Agent):
    '''蒙特卡洛树搜索'''
    
    def __init__(self,
                 tree: Tree = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.tree = Tree() if isna(tree) else tree
        
    def check_root(self,
                   env: gym.Env,
                   func_s_1st: Callable = None
                   ):
        if isna(self.tree.root):
            s, _ = env.reset()
            if not isna(func_s_1st):
                env, s = func_s_1st(env)
            root_node = Node(state_p=None,
                             action=None,
                             state=s,
                             reward=0,
                             terminal=False)
            self.tree.add_node(root_node)
        return self.tree.root

    def ucb(self,
            node: Node,
            c: Union[int, float] = 1.0,) -> float:
        '''UCB公式'''
        if node.n_visit == 0:
            return np.inf
        parent = self.tree.get_parent_node(node)
        e = math.sqrt(2.0 * math.log(parent.n_visit) / node.n_visit)
        v = node.mean_sim_reward + c * e
        return v
    
    def get_unvisit_actions(self,
                            env: gym.Env,
                            node: Node,
                            ) -> Union[list, None]:
        raise NotImplementedError
        
    def _random_choice_add_node(self,
                                env: gym.Env,
                                node: Node,
                                actions: list) -> Node:
        '''给定节点，从可选动作actions中随机选择一个执行并添加子节点'''
        a = np.random.choice(actions)
        s, r, end1, end2, _ = env.step(a)
        child = Node(state_p=node.state,
                     action=a,
                     state=s,
                     reward=r,
                     terminal=end1 or end2)
        return self.tree.add_node(child, parent=node)
    
    def _get_best_child(self,
                        env: gym.Env,
                        node: Node,
                        c_ucb: Union[int, float] = 1.0):
        '''获取最优子节点'''
        children = self.tree.get_children_nodes(node)
        ucbs = [self.ucb(x, c=c_ucb) for x in children]
        i = np.argmax(ucbs)
        best_child = children[i]
        s, _, _, _, _ = env.step(best_child.action)
        # assert s == best_child.state
        return best_child
    
    def select(self,
               env: gym.Env,
               node: Node,
               p_explore: float = 1.0,
               c_ucb: Union[int, float] = 1.0) -> Node:
        '''给定节点，选择子节点，p_explore为不选择最优子节点而探索新节点的概率'''
        if len(node.children) == 0: # 无子节点，选择自身
            return node
        actions = self.get_unvisit_actions(env, node)
        if isna(actions) or len(actions) == 0:
            # 已完全扩展，选择ucb最大的子节点
            # TODO: 可以改成根据所有子节点ucb值进行轮盘赌选择，而不是直接取最优？
            return self._get_best_child(env, node, c_ucb=c_ucb)
        else:
            # 未完全扩展（还有未被发现的子节点，即还有动作未被执行过），
            # 以一定概率进行探索（从中随机选一个）
            if np.random.rand() < p_explore:
                return self._random_choice_add_node(env, node, actions)
            else:
                return self._get_best_child(env, node, c=c_ucb)
        
    def expand(self,
               env: gym.Env,
               node: Node) -> Node:
        '''从给定节点扩展一个子节点'''
        # 如果当前节点没有被访问过，直接从此节点开始模拟
        if node.n_visit == 0:
            return node
        actions = self.get_unvisit_actions(env, node)
        if isna(actions) or len(actions) == 0: # 已完全扩展
            return node
        # 随机选择一个可用节点进行扩展
        return self._random_choice_add_node(env, node, actions)
    
    def sim_until_over(self,
                       env: gym.Env,
                       node: Node,
                       max_step: int = 50,
                       r_sum: bool = False,
                       gamma: float = 1.0) -> Union[int, float]:
        '''自定义实现，从给定节点开始模拟直到结束，返回奖励'''
        raise NotImplementedError
    
    def simulate(self,
                 env: gym.Env,
                 node: Node,
                 max_step: int = 50,
                 r_sum: bool = False,
                 gamma: float = 1.0) -> Union[int, float]:
        '''
        从给定节点开始模拟直到结束，返回奖励
        '''
        if node.terminal:
            return node.reward
        return self.sim_until_over(env, node,
                                   max_step=max_step,
                                   r_sum=r_sum, gamma=gamma)
    
    def trace_back(self, node: Node, reward: Union[float, int]):
        '''回溯更新访问次数和奖励'''
        while not isna(node):
            node.n_visit += 1
            node.tot_sim_reward += reward
            node = self.tree.get_parent_node(node)
    
    def uct(self,
            env: gym.Env,
            node: Node,
            n_sim: int = 50,
            p_explore: float = 1.0,
            c_ucb: Union[int, float] = 1.0,
            sim_max_step: int = 50,
            r_sum: bool = False,
            gamma: float = 1.0) -> Node:
        '''蒙特卡洛树搜索，返回最优动作'''
        if node.terminal:
            return 'over'
        for k in range(n_sim):
            env_ = copy.deepcopy(env)
            node_ = self.select(env_, node,
                                p_explore=p_explore,
                                c_ucb=c_ucb)
            new_node = self.expand(env_, node_)
            reward = self.simulate(env_,
                                   new_node,
                                   max_step=sim_max_step,
                                   r_sum=r_sum,
                                   gamma=gamma)
            self.trace_back(new_node, reward)
            
        if len(node.children) == 0:
            print('none')
            return 'none'
        best_child = self._get_best_child(env, node, c_ucb=c_ucb)
        return best_child
    