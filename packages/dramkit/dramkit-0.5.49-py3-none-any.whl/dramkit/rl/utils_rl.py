# -*- coding: utf-8 -*-

import random
from collections import deque
import pandas as pd
from beartype.typing import Iterable


class PlayBackPool(object):
    '''经验池'''
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity) # 队列，先进先出

    def add(self, *data):
        '''将数据加入buffer'''
        if len(data) == 1 and isinstance(data[0], Iterable):
            data = tuple(data[0])
        self.buffer.append(data)

    def sample(self,
               batch_size: int,
               row_sample: bool = False) -> tuple:
        '''
        | 从buffer中采样数据，数量为batch_size
        | 注意：默认row_sample为False，
        | 采样结果若直接转为pd.DataFrame或np.array，形状为维度*样本量，
        | 若要转为样本量*维度，则需要再transpose，
        | 或将row_sample设置为True
        
        Examples
        --------
        >>> p = PlayBackPool(5)
        >>> p.add(1, 2, 3)
        >>> p.add([4, 5, 6])
        >>> p.add(7, 8, 9)
        >>> pd.DataFrame(p.sample(2))
        >>> pd.DataFrame(p.sample(2, row_sample=True))
        '''
        selects = random.sample(self.buffer, batch_size)
        if row_sample:
            return selects
        dim = len(selects[0])
        res = ', '.join(['d%s'%d for d in range(1, dim+1)])
        res = '(%s)'%res
        exec('(%s) = zip(*selects)'%res)
        return eval(res)
    
    @property
    def size(self) -> int:
        '''目前buffer中数据的数量'''
        return len(self.buffer)









