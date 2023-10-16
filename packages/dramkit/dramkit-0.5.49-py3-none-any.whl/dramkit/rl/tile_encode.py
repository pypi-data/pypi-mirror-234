# -*- coding: utf-8 -*-

from beartype import beartype
from beartype.typing import Union, List, Callable
import numpy as np
from dramkit.gentools import raise_error

#%%
class TileEncoder(object):
    '''
    | 瓦块编码
    | 参考：https://github.com/MeepMoop/tilecoding
    '''
    
    @beartype
    def __init__(self,
                 n_tiles_per_dim: List[int],
                 low_up_per_dim: List[List[Union[float, int]]],
                 n_layer: int = 8,
                 func_offset: Callable = lambda n: 2*np.arange(n)+1):
        '''
        n_tiles_per_dim : list, tuple
            一层中每个维度的瓦块数量
        low_up_per_dim : list
            每个维度的取值上下界
        n_layer : int
            层数
        func_offset : Callable
            计算各层与第一层之间在各个维度上偏移的瓦片数据的函数，输入为层数，返回为各层瓦块的偏移数量列表
        '''
        
        self.n_dim = len(n_tiles_per_dim) # 维度
        self.n_tiles_per_dim = n_tiles_per_dim # 每个维度瓦块数量
        self.bounds = np.array(low_up_per_dim) # 边界值
        self.n_layer = n_layer # 层数
        
        # 扩展（每个维度瓦块数量手动增1个）
        n_tiles_per_dim_ = np.array(np.ceil(n_tiles_per_dim), dtype=int) + 1
        self.n_tiles_per_dim_ = n_tiles_per_dim_
        # 瓦块总数量（特征数量）
        self.n_all_tiles = n_layer * np.prod(n_tiles_per_dim_)
        
        # 各层各个维度偏离的瓦块数量
        self.offsets = \
            func_offset(self.n_dim) * \
            np.repeat([np.arange(n_layer)], self.n_dim, 0).T / \
            float(n_layer) % 1
        
        # 每个瓦块所代表的长度的倒数，即一个单位长度占几个瓦块
        self.n_tiles_per_dim_norm = np.array(n_tiles_per_dim) / (self.bounds[:, 1] - self.bounds[:, 0])
        # 各层瓦块的起始编号
        self.start_index_per_layer = np.prod(n_tiles_per_dim_) * np.arange(n_layer)
        # n_tile_gap_per_dim表示在各个维度方向上，下一个瓦块和上一个瓦块之间的间隔瓦块数
        # 计算瓦块编号时用
        # 例如3*3的二维情况，假设第一维在第二个瓦块，第二位在第三个瓦块，则所在瓦块的编号为1*1+3*2=7
        self.n_tile_gap_per_dim = np.array([np.prod(n_tiles_per_dim_[0:i]) for i in range(self.n_dim)])
  
    @beartype
    def __getitem__(self, x: Union[list, tuple, int, float, np.ndarray]):
        '''返回x所在的所有瓦块的编号列表'''
        if (x > self.bounds[:, 1]).sum() + (x < self.bounds[:, 0]).sum() > 0:
            raise_error('CrossBoundError', '越界！')
        x_low = x - self.bounds[:, 0]
        n_tiles = x_low * self.n_tiles_per_dim_norm # 每个维度占了第几个瓦块
        off_coords = (n_tiles + self.offsets).astype(int) # 加上偏移量
        return self.start_index_per_layer + np.dot(off_coords, self.n_tile_gap_per_dim)

    def __call__(self, x):
        return self.__getitem__(x)

#%%
if __name__ == '__main__':
    from dramkit.gentools import TimeRecoder
    tr = TimeRecoder()
    
    #%%
    # '''
    n_tiles_per_dim = [8, 8, 8]
    low_up_per_dim = [[0.0, 2*np.pi],
                      [0.0, 2*np.pi],
                      [0.0, 2*np.pi]]
    # n_tiles_per_dim = [8, 8]
    # low_up_per_dim = [[0.0, 2*np.pi], [0.0, 2*np.pi]]
    # n_tiles_per_dim = [8, 8]
    # low_up_per_dim = [[-1.2, 0.6], [-0.07, 0.07]]
    n_layer = 8
    func_offset = lambda n: 2 * np.arange(n) + 1
    self = TileEncoder(n_tiles_per_dim, low_up_per_dim, n_layer, func_offset)
    x = (0, 2, 3) if len(n_tiles_per_dim) == 3 else (0, 2)
    # x = np.pi
    # x = 0.02
    print(self[x])
    print(self(x))
    # '''
    
    #%%
    import time
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    n_tiles_per_dim = [8, 8]
    bounds = [[0.0, 2*np.pi], [0.0, 2*np.pi]]
    n_layer = 8

    # create tile coder
    tile_encoder = TileEncoder(n_tiles_per_dim, bounds, n_layer)

    # target function with gaussian noise
    def target_func(x, y):
        return np.sin(x) + np.cos(y) + 0.1 * np.random.randn()

    # linear function weight vector, step size for GD
    w = np.zeros(tile_encoder.n_all_tiles)
    lr = 0.1 / n_layer
    
    # 随机梯度下降SGD
    # take 10000 samples of target function, 
    # output mse of batches of 100 points
    strt_tm = time.time()
    batch_size = 100
    for batches in range(100):
        mse = 0.0
        for b in range(batch_size):
            x = bounds[0][0] + np.random.rand() * (bounds[0][1] - bounds[0][0])
            y = bounds[1][0] + np.random.rand() * (bounds[1][1] - bounds[1][0])
            target = target_func(x, y)
            tiles = tile_encoder[x, y]
            w[tiles] += lr * (target - w[tiles].sum())
            mse += (target - w[tiles].sum()) ** 2
        mse /= batch_size
        print('samples:', (batches + 1) * batch_size, 'batch_mse:', mse)
    print('elapsed time: %ss'%(time.time() - strt_tm))
    
    # # 小批量梯度下降MBSGD
    # strt_tm = time.time()
    # batch_size = 10
    # for batches in range(20000):
    #     mse = 0.0
    #     dif = 0
    #     for b in range(batch_size):
    #         x = bounds[0][0] + np.random.rand() * (bounds[0][1] - bounds[0][0])
    #         y = bounds[1][0] + np.random.rand() * (bounds[1][1] - bounds[1][0])
    #         target = target_func(x, y)
    #         tiles = tile_encoder[x, y]
    #         sim = w[tiles].sum()
    #         dif += target - sim
    #     w[tiles] += lr * (dif / batch_size)
    # print('elapsed time: %ss'%(time.time() - strt_tm))

    # get learned function
    print('mapping function...')
    res = 200
    x = np.arange(bounds[0][0], bounds[0][1], (bounds[0][1] - bounds[0][0]) / res)
    y = np.arange(bounds[1][0], bounds[1][1], (bounds[1][1] - bounds[1][0]) / res)
    z = np.zeros([len(x), len(y)])
    z_tgt = np.zeros([len(x), len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            tiles = tile_encoder[x[i], y[j]]
            z[i, j] = w[tiles].sum()
            z_tgt[i, j] = target_func(x[i], y[j])
            
            
    # plot
    fig = plt.figure(figsize=(8, 6))
    ax = Axes3D(fig, auto_add_to_figure=False)
    ax = fig.add_axes(ax)
    ax = fig.gca()
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, z_tgt, cmap=plt.get_cmap('hot'))
    plt.title('真实结果')
    plt.show()

    # plot
    fig = plt.figure(figsize=(8, 6))
    ax = Axes3D(fig, auto_add_to_figure=False)
    ax = fig.add_axes(ax)
    ax = fig.gca()
    X, Y = np.meshgrid(x, y)
    surf = ax.plot_surface(X, Y, z, cmap=plt.get_cmap('hot'))
    plt.title('梯度下降拟合结果')
    plt.show()
    
    #%%
    tr.used()

