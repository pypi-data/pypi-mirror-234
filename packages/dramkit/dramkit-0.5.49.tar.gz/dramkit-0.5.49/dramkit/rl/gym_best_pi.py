# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from dramkit.gentools import isna

acts_CliffWalking_v0 = {0: '^', 1: '>', 2: 'v', 3: '<'}
acts_FrozenLake_v1 = {0: '<', 1: 'v', 2: '>', 3: '^'}

_best_a_CliffWalking_v0 = np.array(
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
_best_a_CliffWalking_v0 = np.eye(4)[_best_a_CliffWalking_v0]
_best_a_CliffWalking_v0 = pd.DataFrame(_best_a_CliffWalking_v0).transpose()
_best_a_CliffWalking_v0 = _best_a_CliffWalking_v0.to_dict(orient='dict')

_best_a_FrozenLake_v1 = {
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
acts_FrozenLake_v1 = {0: '<', 1: 'v', 2: '>', 3: '^'}
_best_a_FrozenLake_v1_noslip = {
    0:  {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
    1:  {0:  0.5, 1:  0.0, 2:  0.5, 3:  0.0},
    2:  {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
    3:  {0:  1.0, 1:  0.0, 2:  0.0, 3:  0.0},
    4:  {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
    5:  {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
    6:  {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
    7:  {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
    8:  {0:  0.0, 1:  0.0, 2:  1.0, 3:  0.0},
    9:  {0:  0.0, 1:  0.5, 2:  0.5, 3:  0.0},
    10: {0:  0.0, 1:  1.0, 2:  0.0, 3:  0.0},
    11: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
    12: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
    13: {0:  0.0, 1:  0.0, 2:  1.0, 3:  0.0},
    14: {0:  0.0, 1:  0.0, 2:  1.0, 3:  0.0},
    15: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25},
}


best_pis = {
    'FrozenLake-v1': _best_a_FrozenLake_v1,
    'FrozenLake-v1_noslip': _best_a_FrozenLake_v1_noslip,
    'CliffWalking-v0': _best_a_CliffWalking_v0
}


def get_best_pi(env_name, df=True,
                a_names=None, s_names=None):
    res = best_pis[env_name]
    if df:
        res = pd.DataFrame(res).transpose()
        if not isna(a_names):
            res.columns = a_names
        if not isna(s_names):
            res.index = s_names
    return res
    
    
    
    
    
    
    
    
    
    
    
    
    
    
