# -*- coding: utf-8 -*-

# 强化学习-多臂老虎机问题（《动手学强化学习》第一章）


import numpy as np
import matplotlib.pyplot as plt


class BernoulliBandit(object):
    '''伯努利多臂老虎机'''
    
    def __init__(self, n_arm, random_seed=5262):
        '''输入n_arm表示拉杆个数'''
        self.n_arm = n_arm
        self.random_seed = random_seed
        np.random.seed(self.random_seed)
        # 随机生成每根拉杆的获奖概率
        self.probs = np.random.uniform(size=self.n_arm)
        self.best_idx = np.argmax(self.probs) # 获奖概率最大的拉杆
        self.best_prob = self.probs[self.best_idx] # 最大的获奖概率
        
        np.random.seed(None) # 恢复随机数种子

    def play(self, k):
        # 当玩家选择了k号拉杆后，根据拉杆获得奖励的概率返回1（获奖）或0（未获奖）
        p = np.random.rand()
        if p < self.probs[k]:
            return 1
        else:
            return 0
        
        
class MabBase(object):
    '''多臂老虎机算法基本框架'''
    
    def __init__(self, bandit):
        '''bandint为BernoulliBandit类实例'''
        self.bandit = bandit
        self.actions = [] # 记录每一步的动作
        self.counts = np.zeros(self.bandit.n_arm) # 记录每根拉杆的操作次数
        self.regret = 0.0 # 记录累积懊悔值
        self.regrets = [] # 记录每一步完成后的累积懊悔值

    def update_regret(self, k):
        '''更新懊悔值，k为操作的拉杆编号'''
        self.regret += self.bandit.best_prob - self.bandit.probs[k]
        self.regrets.append(self.regret)

    def run_1step(self):
        '''选择拉杆，自定义策略函数，必须返回选择的拉杆编号'''
        raise NotImplementedError

    def run(self, n_steps):
        '''玩n_steps次'''
        for _ in range(n_steps):
            k = self.run_1step()
            self.counts[k] += 1
            self.actions.append(k)
            self.update_regret(k)
            
            
class EpsilonGreedy(MabBase):
    '''
    | epsilon-贪婪算法
    | epsilon-贪婪算法的懊悔值一般是呈线性递增的
    '''
    
    def __init__(self, bandit, epsilon=0.01):
        super(EpsilonGreedy, self).__init__(bandit)
        self.epsilon = epsilon
        # 存放所有拉杆的期望奖励估值
        self.estimates = np.ones(self.bandit.n_arm)

    def run_1step(self):
        if np.random.random() < self.epsilon:
            # 随机选择一根拉杆
            k = np.random.randint(0, self.bandit.n_arm)
        else:
            # 选择期望奖励估值最大的拉杆
            k = np.argmax(self.estimates)
        r = self.bandit.play(k) # 拉动拉杆，获取奖励
        # 增量更新期望奖励估值
        self.estimates[k] += (r-self.estimates[k]) / (self.counts[k]+1)
        return k
    
    
class DecayingEpsilonGreedy(MabBase):
    '''
    | 探索概率随时间衰减epsilon-贪婪算法
    | 衰减epsilon-贪婪算法在大多数情况下可以使懊悔值得增加趋于平稳（不像线性那么快）
    | 不过有一定概率退化到普通epsilon-贪婪算法的效果（懊悔值呈线性增长）
    | （在前期探索时没有找到最好的拉杆，导致越往后找到最好拉杆的概率越来越小）
    '''
    
    def __init__(self, bandit):
        super(DecayingEpsilonGreedy, self).__init__(bandit)
        self.estimates = np.ones(self.bandit.n_arm)
        self.total_count = 0 # 记录总操作次数

    def run_1step(self):
        self.total_count += 1
        # 探索概率随着操作次数的增加而衰减
        if np.random.random() < 1/self.total_count:
            k = np.random.randint(0, self.bandit.n_arm)
        else:
            k = np.argmax(self.estimates)
        r = self.bandit.play(k)
        self.estimates[k] += (r-self.estimates[k]) / (self.counts[k]+1)
        return k
    
    
class UCB(MabBase):
    '''
    UCB算法
    '''
    
    def __init__(self, bandit, c=1):
        '''c为控制不确定性比重的系数'''
        super(UCB, self).__init__(bandit)
        self.estimates = np.ones(self.bandit.n_arm)
        self.total_count = 0
        self.c = c

    def run_1step(self):
        self.total_count += 1
        # 计算上置信界
        ucb = self.estimates + \
              self.c * np.sqrt(
                  np.log(self.total_count) / (2*(self.counts+1))
                  )
        k = np.argmax(ucb) # 选出上置信界最大的拉杆
        r = self.bandit.play(k)
        self.estimates[k] += (r-self.estimates[k]) / (self.counts[k]+1)
        return k
    
    
class ThompsonSampling(MabBase):
    '''汤普森采样算法'''
    
    def __init__(self, bandit):
        super(ThompsonSampling, self).__init__(bandit)
        self.n1 = np.ones(self.bandit.n_arm) # 存放每根拉杆奖励为1的次数
        self.n0 = np.ones(self.bandit.n_arm) # 存放每根拉杆奖励为0的次数

    def run_1step(self):
        # 按照Beta分布采样一组奖励样本
        samples = np.random.beta(self.n1, self.n0)
        k = np.argmax(samples) # 选出采样奖励最大的拉杆
        r = self.bandit.play(k)
        self.n1[k] += r # 更新Beta分布的第一个参数
        self.n0[k] += (1-r) # 更新Beta分布的第二个参数
        return k
    
    
def plot_results(players, player_names):
    '''
    对多个策略作图比较懊悔值的变化情况
    '''
    plt.figure(figsize=(10, 6))
    for idx, player in enumerate(players):
        time_list = range(len(player.regrets))
        plt.plot(time_list, player.regrets, label=player_names[idx])
    plt.xlabel('Time steps')
    plt.ylabel('Cumulative regrets')
    plt.title('%d-armed bandit' % players[0].bandit.n_arm)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    from dramkit import TimeRecoder
    tr = TimeRecoder()
    
    n_arm = 10
    random_seed = 0
    n_steps = 10000
    
    # 生成多臂老虎机
    bandit = BernoulliBandit(n_arm, random_seed=random_seed)
    print('获奖概率最大拉杆编号和概率:', 
          bandit.best_idx, round(bandit.best_prob, 4))
    
    # epsilon-贪婪策略
    epsilon = 0.01
    epsilon_greedy_player = EpsilonGreedy(bandit, epsilon=epsilon)
    epsilon_greedy_player.run(n_steps)
    print('epsilon-贪婪算法的累积懊悔为:',
          epsilon_greedy_player.regret)
    plot_results([epsilon_greedy_player], ['EpsilonGreedy'])
    
    epsilons = [1e-4, 0.01, 0.1, 0.25, 0.5]
    players = [EpsilonGreedy(bandit, epsilon=e) for e in epsilons]
    player_names = ['epsilon={}'.format(e) for e in epsilons]
    for player in players:
        player.run(n_steps)    
    plot_results(players, player_names)
    
    # 随时间衰减的epsilon-贪婪策略
    decaying_epsilon_greedy_player = DecayingEpsilonGreedy(bandit)
    decaying_epsilon_greedy_player.run(n_steps)
    print('epsilon衰减的贪婪算法的累积懊悔为：',
          decaying_epsilon_greedy_player.regret)
    plot_results([decaying_epsilon_greedy_player],
                 ['DecayingEpsilonGreedy'])
    
    # UCB算法
    ucb_palyer = UCB(bandit, c=1)
    ucb_palyer.run(n_steps)
    print('上置信界算法UCB的累积懊悔为：', ucb_palyer.regret)
    plot_results([ucb_palyer], ['UCB'])
    
    # 汤普森采样算法
    thompson_sampling_player = ThompsonSampling(bandit)
    thompson_sampling_player.run(n_steps)
    print('汤普森采样算法的累积懊悔为：',
          thompson_sampling_player.regret)
    plot_results([thompson_sampling_player], ['ThompsonSampling'])
    
    
    tr.used()
                  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

