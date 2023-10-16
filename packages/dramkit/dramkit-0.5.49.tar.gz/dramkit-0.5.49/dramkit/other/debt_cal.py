# -*- coding: utf-8 -*-

import numpy as np
import numpy_financial as npf
import pandas as pd
from typing import Union, List


def calc_perfect_house_price(month_income,
                             area=40,
                             rate=0.3,
                             debt_year=30):
    '''
    | 不考虑其它因素，根据人均月收入month_income、人均住房面积area（平米）、
    | 房价占收入比rate和还款年限debt_year计算合理的房价（元/平米）
    '''
    return ((month_income*12*debt_year)*rate) / area


class DebtCal():
    '''
    贷款计算器
    '''
    
    def __init__(self,
                 corpus: float,
                 r_year: float,
                 n_period: int,
                 periods_1y: int = 12):
        '''
        Parameters
        ----------
        corpus : float
            本金总额
        r_year : float
            年利率，如4/100
        n_period : int
            还款期数(例: 按月还款，分三年还，则n_period=36)
        periods_1y : int
            1年有多少个还款期(例: 按月还款，则periods_1y=12)
        '''
        self.corpus = corpus
        self.r_year = r_year
        self.n_period = n_period
        self.periods_1y = periods_1y
        self.r_period = self.r_year / self.periods_1y
        self.cols = ['期号', '还款额', '其中本金', '其中利息',
                     '已还总额', '已还利息', '已还本金', '剩余本金']

    @property
    def mean_all_plan(self):
        '''
        | 计算等额本息还款计划表
        | 计算公式推导(本金为C, 月利率为r, 分n月还款, 每期还款x)：
        | 按终值推导：
        |   本息总额终值 = C * (1+r)^n
        |   每期还款额终值序列: x * (1+r)^n, x * (1+r)^(n-1), ···, x * (1+r), x
        |   每期还款额终值之和 = (x * ((1+r)^n - 1)) / r
        |   求解: C * (1+r)^n = x * ((1+r)^n - 1) / r
        |   得到: x = (C * (1+r)^n * r) / ((1+r)^n - 1)
        | 按递推公式：
        |   参考: https://zhuanlan.zhihu.com/p/390581715
        |   记第t期的还款后的代还总额为Q_(t)，则有递推公式:
        |   Q_(t+1) = Q_(t) * (1+r) - x
        |   Q_(1) = C * (1+R) - x
        |   Q_(2) = Q_(1) * (1+R) - x
        |         = C * (1+r)**2 - x*(1+(1+r))
        |   ...
        '''
        total_to_pay = self.corpus * ((1+self.r_period)**self.n_period)
        period_pay = (total_to_pay * self.r_period) / ((1+self.r_period)**self.n_period - 1)
        df = pd.DataFrame(columns=self.cols)
        df['期号'] = range(1, self.n_period+1)
        df['还款额'] = np.ones((self.n_period,)) * period_pay
        df['已还总额'] = df['还款额'].cumsum()
        left_corpus = self.corpus # 记录剩余本金
        for k in range(df.shape[0]):
            df.loc[k, '其中利息'] = left_corpus * self.r_period
            period_corpus = df.loc[k, '还款额'] - df.loc[k, '其中利息']
            left_corpus -= period_corpus
            df.loc[k, '其中本金'] = df.loc[k, '还款额'] - df.loc[k, '其中利息']
            df.loc[k, '剩余本金'] = left_corpus
        df['已还本金'] = df['其中本金'].cumsum()
        df['已还利息'] = df['其中利息'].cumsum()
        return df
    
    @staticmethod
    def calc_r_year_by_period_pay(corpus: float,
                                  periods_pay: Union[float, List[float]],
                                  n_period: int,
                                  periods_1y: int = 12,
                                  rtype: str = 'exp'):
        '''根据本金corpus、每期还款额periods_pay、期数n_period、每年有多少期periods_1y反推年利率'''
        rtype = rtype.lower()
        assert rtype in ['exp', 'mult']
        if isinstance(periods_pay, list):
            values = [-corpus] + periods_pay
        else:
            values = [-corpus] + [periods_pay] * n_period
        r = npf.irr(values)
        if rtype == 'exp':
            return pow(1+r, periods_1y) - 1
        elif rtype == 'mult':
            return r * periods_1y

    @property
    def mean_corpus_plan(self):
        '''
        计算等额本息金还款计划表
        '''
        df = pd.DataFrame(columns=self.cols)
        df['期号'] = range(1, self.n_period+1)        
        df['其中本金'] = self.corpus / self.n_period
        df['其中利息'] = (self.corpus - df['其中本金'].shift(1).fillna(0).cumsum()) * self.r_period
        df['还款额'] = df['其中本金'] + df['其中利息']
        df['已还总额'] = df['还款额'].cumsum()
        df['已还本金'] = df['其中本金'].cumsum()
        df['已还利息'] = df['其中利息'].cumsum()
        df['剩余本金'] = self.corpus - df['已还本金']
        return df


if __name__ == '__main__':
    corpus, r_year, n_period = 6000, 24/100, 3
    self = DebtCal(corpus, r_year, n_period)
    mean_all_plan1 = self.mean_all_plan
    # print(mean_all_plan1)
    mean_corpus_plan1 = self.mean_corpus_plan
    # print(mean_corpus_plan1)
    rtype = 'exp'
    print(self.calc_r_year_by_period_pay(corpus,
                                         mean_all_plan1['还款额'].tolist(),
                                         n_period,
                                         rtype=rtype))
    print(DebtCal.calc_r_year_by_period_pay(corpus,
                                            mean_corpus_plan1['还款额'].tolist(),
                                            n_period,
                                            rtype=rtype))
    
    
    corpus, r_year, n_period = 500*10000, 4/100, 30*12
    self = DebtCal(corpus, r_year, n_period)
    mean_all_plan = self.mean_all_plan
    mean_corpus_plan = self.mean_corpus_plan
    rtype = 'mult'
    print(self.calc_r_year_by_period_pay(corpus,
                                         mean_all_plan['还款额'].tolist(),
                                         n_period,
                                         rtype=rtype))
    print(DebtCal.calc_r_year_by_period_pay(corpus,
                                            mean_corpus_plan['还款额'].tolist(),
                                            n_period,
                                            rtype=rtype))
    




