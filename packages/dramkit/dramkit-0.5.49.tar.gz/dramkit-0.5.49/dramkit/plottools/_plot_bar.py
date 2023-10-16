# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm  #导入库
    result = pd.DataFrame({'系数': [0.2, 0.3, 0.5, -0.4, 0.6],
                           'P值': [0.0001, 0.2, 0.03, 0.5, 0.000001]},
                          index=['f1', 'f2', 'f3', 'f4', 'f5'])
    plt.barh(result.index, result['系数'], height=0.1,
             color=cm.ScalarMappable().to_rgba(result['P值'])) # 以回归系数均值为高度，P值均值为颜色绘制条形图
    # sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=result['P值'].min(), vmax=result['P值'].max()))  
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=0, vmax=1))  
    clb = plt.colorbar(sm) # 根据P值的大小显示颜色
    clb.set_label('P值', fontdict={'size': 15})
    plt.title('用回归系数和P值绘制多重显示条形图', 
              fontdict={'size': 50}) # 设置标题
    plt.ylabel('因子名称', fontdict={'size': 50})
    plt.xlabel('系数大小', fontdict={'size': 50})
    plt.show()

