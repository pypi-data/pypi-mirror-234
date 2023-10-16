# -*- coding: utf-8 -*-


'''
| 重要性采样
| https://zhuanlan.zhihu.com/p/629016302
| https://zhuanlan.zhihu.com/p/258384070
| https://zhuanlan.zhihu.com/p/259389498
| https://blog.csdn.net/bigheadyushan/article/details/80623249
| https://zhuanlan.zhihu.com/p/41217212
'''

if __name__ == '__main__':
    # 导入所需要的库
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import matplotlib
    import scipy.stats as stats
    
    # Sympy Stuff
    import sympy
    from sympy import erf
    from sympy.utilities.lambdify import lambdify
    ## 首先计算问题的解析解
    xs=sympy.Symbol('xs')
    fz = sympy.exp(-xs**2/2)/sympy.sqrt(2*sympy.pi)
    Pz = sympy.integrals.integrate(fz,(xs,4.5,sympy.oo)).evalf()
    print("Analytical solution")
    print(Pz)
    # 定义蒙特卡洛sample 函数，为后续准备
    def monte_carlo(num_samples, sample_generator, g_evaluator, cumsum=False):
        """
        函数详情可以参考 https://zhuanlan.zhihu.com/p/250282313
        输入:
        -----
        num_samples: 定义样本数量
        sample_generator: 根据给定的概率分布生成样本，对应上文的X,
        调用方式 sample_generator(num_samples)，返回samples,可以是多个维度，
        但是第一个维度必须是num_samples    
        g_evaluator(samples): 计算 g(X)
        cumsum:如果 cumsum=True, 那么对于1个，2个，……n个样本，都进行monte_carlo估计
        输出
        estimator:蒙特卡洛估计值（对应给定的num_samples）
        samples: 对应的样本 Xs
        evaluations: 对应的 g(X)s    
        """
        samples = sample_generator(num_samples)
        evaluations = g_evaluator(samples)
        if cumsum is False:
            estimate = np.sum(evaluations,axis=0)/float(num_samples)
        else:
            estimate = np.sum(evaluations,axis=0)/np.arange(1,num_samples+1,dtype=np.float)
    
        return estimate, samples, evaluations
    # 利用蒙特卡洛方法对 Pz 进行估计
    sampler = np.random.randn
    gfun_mc = lambda x:x>4.5 #定义了 ”标记函数“（indicator function 1(Z>4.5)
    num_samples = 10000
    Pz_mc,_,_ = monte_carlo(num_samples,sampler,gfun_mc)
    print('''Monte Carlo estimation of {:d} samples of P(Z>4.5)={:5E}
          \n\t Truth: {:5E}'''.format(num_samples,Pz_mc,Pz))
          
          
    
    ## 指数概率分布 q_X()可以由scipy的stats.expon定义
    ## 对比一下 q_X(x) 与 f_X(x)
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(14,5))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    x = np.linspace(4.5,10,1000)
    qx = stats.expon.pdf(x)
    fx = stats.norm.pdf(x)
    ax1.plot(x,qx,label='Exponential')
    ax1.plot(x,fx,label='Standard Normal')
    ax1.set_xlabel('Z',fontsize=14)
    ax1.set_ylabel('PDF',fontsize=14)
    ax1.set_title('normal scale')
    
    ax2.semilogy(x,qx,label='Exponential')
    ax2.semilogy(x,fx,label='Standard Normal')
    ax2.set_xlabel('Z',fontsize=14)
    ax2.set_ylabel('PDF',fontsize=14)
    ax2.set_title('log scale')
    plt.show()
    
    
    ## 利用 q_X(x)对问题进行重点抽样(important sampling, 简记为is)
    sampler = lambda ns: stats.expon.rvs(size=ns,loc=4.5)
    gfun_is = lambda x:gfun_mc(x)*stats.norm.pdf(x)/stats.expon.pdf(x,loc=4.5)
    
    Pz_is,samples,weights = monte_carlo(num_samples,sampler,gfun_is)
    print('''Important sample with {:d} samples Pz_is={:5E}
            \n\t True is {:5E}'''.format(num_samples,Pz_is,Pz))
          
            
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(15,5))
    ax1.semilogy(samples,weights,'o')
    ax1.set_xlabel('Z',fontsize=14)
    ax1.set_ylabel(r'$f_X(x)/q_X(x)$, (weight)',fontsize=14)
    ax2.hist(weights,bins=50,density=True)
    ax2.set_title('Histogram of weight')
    plt.show()



    import math
    var_mc = (Pz*(1-Pz))/num_samples
    std_mc = math.sqrt(var_mc)
    print('Standard deviation of MC sample:{:5E}'.format(std_mc))
    
    
    ## 通过上文计算的 weights估计重点采样的标准差
    var_is = np.var(weights) # 因为上边计算中，根据指数概率分布定义，只有 Z>4.5 才产生 weight，所以隐含了indactor 函数
    std_is = math.sqrt(var_is)
    print('Standard deviation of important sample:{0}'.format(std_is))
    
    
    
    epsilon=0.1
    require_num_samples = Pz*(1-Pz)/(epsilon*Pz)**2
    print(require_num_samples)
    print('Required {0} samples for Monte Carlo sampling to have standard deviation=epsilon*p'
          .format(require_num_samples))
    
    
    
    require_num_samples_is = var_is/(epsilon*Pz)**2
    print(require_num_samples_is)
    print('Required {0} samples for Monte Carlo sampling to have standard deviation=epsilon*p'
          .format(require_num_samples_is))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    