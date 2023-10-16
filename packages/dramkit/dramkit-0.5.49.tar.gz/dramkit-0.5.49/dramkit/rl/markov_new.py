# -*- coding: utf-8 -*-

import numpy as np
from beartype.typing import List

from dramkit.gentools import isna


class MDP(object):
    '''马尔科夫决策过程'''
    
    def __init__(p_sa2s: np.ndarray = None,
                 r_sa2s: np.ndarray = None,
                 p_sa2sr: np.ndarray = None,
                 rewards: List[int, float] = None,
                 s_names: List[str] = None,
                 a_names: List[str] = None,
                 s_stop: str = None):
        
        assert (not (isna(p_sa2s) or isna(r_sa2s))) or \
               (not (isna(p_sa2sr) or isna(rewards))), \
               ('动力系统信息: 必须提供`p_sa2s`+`p_sa2s`'
                '或`p_sa2sr`+`rewards`的组合!')
               












