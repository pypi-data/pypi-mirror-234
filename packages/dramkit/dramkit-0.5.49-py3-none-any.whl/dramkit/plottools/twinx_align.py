"""
===============================================
Let twin-axis aligned at the specified position
===============================================

Let the left-axis and right-axis aligned at the specified position.

In some data that need twin-axis plot, a point at left-axis and
another point at right-axis have same meaning, they should be aligned.
For example, we plot netvalue curve of a portfolio at twin-left-axis
and profit raito curve at twin-right-axis, the point 1.0 at the
left-axis and the point 0.0 at the right-axis both mean the begin
state of the portifolio, so they should be aligned.
"""


def twinxalign(ax_left, ax_right, v_left, v_right):
    """
    Let the position `v_left` on `ax_left`
    and the position `v_right` on `ax_right` be aligned
    """
    left_min, left_max = ax_left.get_ybound()
    right_min, right_max = ax_right.get_ybound()
    k = (left_max-left_min) / (right_max-right_min)
    b = left_min - k * right_min
    x_right_new = k * v_right + b
    dif = x_right_new - v_left
    # 第一次线性映射，目的是获取左轴和右轴的伸缩比例，通过这层映射，
    # 计算可以得到右轴指定位置映射到左轴之后在左轴的位置。
    # 右轴目标映射到左轴的位置与左轴目标位置存在一个差值，
    # 这个差值就是右轴的一端需要扩展的距离，这个距离是映射到左轴之后按左轴的尺度度量的。
    # 通过第一次线性映射的逆映射，计算得到右轴一端实际需要扩展的距离。
    # 得到右轴一端的扩展距离之后，右轴就有两个固定点：一个端点和一个目标点。
    # 将右轴这两个固定点与左轴对应的点做第二次线性映射，可以再次得到两轴的伸缩比例，
    # 得到新的伸缩比例之后，通过左轴的另一个端点进行逆映射，可以计算题右轴的另一个端点。
    # TODO: （下面最后一步貌似不需要，待确认）
    # 最后通过右轴两个端点位置以及新的伸缩比例对右轴进行伸缩变化，
    # 即可将左轴与右轴在指定刻度位置对齐。
    if dif >= 0:
        right_min_new = ((left_min-dif) - b) / k
        k_new = (left_min-v_left) / (right_min_new-v_right)
        b_new = v_left - k_new * v_right
        right_max_new = (left_max - b_new) / k_new
    else:
        right_max_new = ((left_max-dif) - b) / k
        k_new = (left_max-v_left) / (right_max_new-v_right)
        b_new = v_left - k_new * v_right
        right_min_new = (left_min - b_new) / k_new
    # def _forward(x):
    #     return k_new * x + b_new
    # def _inverse(x):
    #     return (x - b_new) / k_new
    ax_right.set_ylim([right_min_new, right_max_new])
    # ax_right.set_yscale('function', functions=(_forward, _inverse))
    return ax_left, ax_right


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    
    def plot_example(align=False):
        """Plot sim data"""
        plt.figure(figsize=(10, 7))
        ax1 = plt.subplot(111)
        ax1.plot(net_value, '-k')
        ax1.axhline(1, c='k', lw=1, ls='--')
        ax1.set_ylabel('NetValue(black)', fontsize=16)
        ax2 = ax1.twinx()
        ax2.plot(gain_pct, '-b')
        ax2.axhline(0, c='r', lw=1, ls='--')
        ax2.set_ylabel('GainPct(blue)', fontsize=16)
        if align:
            twinxalign(ax1, ax2, 1, 0)
            plt.title('aligned', fontsize=16)
        else:
            plt.title('not align', fontsize=16)
        plt.show()
        
    # # 数据
    # import pandas as pd
    # # 每日净流入
    # net_in = [100, 0, 0, 0, 20, 0, 0, 0, 0, -20,
    #           0, 0, 30, 0, 0, 0, 0, 0, -30, 0]
    # # 每日盈亏金额
    # net_gain= [0, -2, -3, 5, 2, 3, 4, 5, 5, -1,
    #            -4, -10, 2, 5, 9, 6, 0, 1, -1, 9]
    # df = pd.DataFrame({'net_in': net_in, 'net_gain': net_gain})
    # df['total_in'] = df['net_in'].cumsum()
    # df['value'] = df['total_in'] + df['net_gain'].cumsum()
    # df['net_value'] = df['value'] / df['value'].iloc[0] # 每日净值  
    # df['gain_pct'] = df['value'] / df['total_in'] - 1 # 实际累计盈亏比例
    # net_value = df['net_value'].values
    # gain_pct = df['gain_pct'].values

    # Sim data
    net_value = np.array([1.0, 0.98, 0.95, 1.0, 1.22, 1.25, 1.29, 1.34,
                          1.39, 1.18, 1.14, 1.04, 1.36, 1.41, 1.5, 1.56,
                          1.56, 1.57, 1.26, 1.35])
    gain_pct = np.array([0.0, -0.02, -0.05, 0.0, 0.02, 0.04, 0.07,
                          0.12, 0.16, 0.18, 0.14, 0.04, 0.05, 0.08,
                          0.15, 0.2, 0.2, 0.21, 0.26, 0.35])
    
    plot_example()
    plot_example(align=True)
