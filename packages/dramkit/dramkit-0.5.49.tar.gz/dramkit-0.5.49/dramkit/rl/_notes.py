# -*- coding: utf-8 -*-

from dramkit import TimeRecoder
tr = TimeRecoder()


'''
# 普通蒙特卡洛方法的特点是每次更新价值只用了状态-动作所在的路径上并且在其后面出现的步骤的价值，
所以对采样数据的利用率很低
# 因此，普通蒙特卡洛对求解最优路径较长的任务比较困难（比如冰湖游戏或悬崖寻路）
# 例如，悬崖寻路的最优路径(状态）为：
     [36 ^ 24 > 25 > 26 > 27 > 28 > 29 > 30 > 31 > 32 > 33 > 34 > 35 v 47]
  假设有三条采样路径：
     [36 ^ 24 > 25 > 26 > 27 > 28 > 29]
     [26 > 27 > 28 > 29 > 30 > 31 > 32 > 33 > 34 > 35 v 47]
     [36 ^ 24 > 25 > 26 > 27]
  # 普通蒙特卡洛计方法算状态25的价值时，并没有用到第二条路径中的状态
  （因为第二条路径中没出现过25），这就导致的关键数据的丢失，
  因为实际上第一条路径和第二条路径都是最优路径的一部分
  
# SARSA算法相较于普通MC对数据的利用率更高（能一定程度上提升路径之间的`连接`程度）
# 例如，上面的例子中，SARSA在计算状态25的价值时，用到了第二条路径中的状态
  （第三条路径中25的后面是26，第二条路径中出现了26）
# SARSA算法的一个显著缺点是更新时不会使用到路径中当前更新状态之后n步的数据，因此数据利用率仍然是低下的

# TODO
# 可能的提升方法：
# 将采样路径生成一棵树，然后计算树中每条路径上每个节点的价值
'''

#%%
import pandas as pd
from dramkit.gentools import raise_error
from dramkit.rl.mc import cal_v_s_a as cal_q_mc
from dramkit.rl.td import cal_v_s_a_sarsa as cal_q_td
from dramkit.rl.utils_gym import s_a_dict2df

#%%
state_spaces = list(range(0, 48))
action_spaces = list(range(0, 4))
a_names = ['^', '>', 'v', '<']

def gen_clfwlk_route(str_route):
    a_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    route = []
    s_a = str_route.split(' ')
    for k in range(0, len(s_a)-2, 2):
        s, a, s_ = int(s_a[k]), a_map[s_a[k+1]], int(s_a[k+2])
        r = -100 if s_ == 36 else -1
        end = s_ == 47
        route.append((s, a, r, s_, end))
    return route

def get_q(routes, method):
    routes = [gen_clfwlk_route(x) for x in routes]
    if method == 'mc':
        q = cal_q_mc(routes, state_spaces, action_spaces, gamma=1)
        q = s_a_dict2df(q, a_names=a_names)
    elif method == 'sarsa':
        q = cal_q_td(routes, len(state_spaces), len(action_spaces), gamma=1)
        q = pd.DataFrame(q, columns=a_names)
    else:
        raise_error('QValueMethodError', '未识别的方法！')
    # 仅查看价值不为0的状态
    q = q[q.sum(axis=1) != 0]
    return q, routes

#%%
routes = [
    '36 ^ 24 > 25 > 26 > 27 > 28 > 29',
    '26 > 27 > 28 > 29 > 30 > 31 > 32 > 33 > 34 > 35 v 47',
    '36 ^ 24 > 25 > 26 > 27',
    '25 ^ 13 ^ 1 > 2 v 14'
]

#%%
# 普通mc价值计算
q1, _ = get_q(routes, 'mc')
# SARSA价值计算
q2, _ = get_q(routes, 'sarsa')

#%%
'''
# 蒙特卡洛树
routes = [gen_clfwlk_route(x) for x in routes]

from dramkit.rl.mcts import Node, Tree
tree = Tree()
for route in routes:
    for s, a, r, s_new, end in route:
        node = Node(state_p, action, state, reward, terminal, kwargs)

# '''

#%%
'''
# 蒙特卡洛图
paths = [gen_clfwlk_route(x) for x in routes]
edges = {}
for path in paths:
    for step in path:
        s, a, r, s_next, end = step
        if (s, s_next) in edges:
            edges[(s, s_next)]['r'] += r
            edges[(s, s_next)]['n'] += 1
        else:
            edges[(s, s_next)] = {}
            edges[(s, s_next)]['a'] = a
            edges[(s, s_next)]['r'] = r
            edges[(s, s_next)]['n'] = 1
edges_ = []
for (from_, to_), attrs in edges.items():
    edges_.append((from_, to_, attrs))
    
from dramkit.datsci.utils_networkx import gen_digraph_edge_list
g = gen_digraph_edge_list(edges_)
import matplotlib.pyplot as plt
import networkx as nx

plt.figure(figsize=(8, 8))
pos = nx.nx_agraph.graphviz_layout(g, prog="twopi")
nx.draw(g, pos)
plt.show()


roots = [node for node, in_degree in g.in_degree() if in_degree == 0]
ends = [node for node, out_degree in g.out_degree() if out_degree == 0]
gpaths = []
for root in roots:
    for end in ends:
        gpaths += list(nx.all_simple_paths(g, root, end))

# '''

#%%
tr.used()





