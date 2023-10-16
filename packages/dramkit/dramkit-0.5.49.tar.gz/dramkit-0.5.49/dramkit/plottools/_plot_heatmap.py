# -*- coding: utf-8 -*-

import seaborn as sns
import matplotlib.pyplot as plt


def plot_heatmap(df, figsize, title, fig_save_path,
                 **kwargs):
    plt.figure(figsize=(12, 10))
    h = sns.heatmap(df, annot=True, #cmap='RdBu',
                xticklabels=1, yticklabels=1,
                annot_kws={'fontsize': 15},
                cbar=False,
                vmin=-1, vmax=1,
                )
    cb = h.figure.colorbar(h.collections[0]) # 显示colorbar
    cb.ax.tick_params(labelsize=10) # 设置colorbar刻度字体大小
    plt.title(title, fontdict={'size': 20})
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)
    plt.savefig(fig_save_path)
    plt.show()