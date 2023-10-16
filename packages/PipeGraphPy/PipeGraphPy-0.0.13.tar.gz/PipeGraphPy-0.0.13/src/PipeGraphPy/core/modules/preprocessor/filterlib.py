# -*- coding: utf-8 -*-
"""
@author: Jinji Piao
"""
import pandas as pd
import numpy as np
import math
from scipy import optimize


def abnormal(data, cap, k_up, k_down):
    # 异常剔除
    df = data.copy()
    df.loc[math.tan(k_up)*df['radiation_norm'].values <
           df['power_norm'].values, 'flag'] = 1
    df.loc[math.tan(k_down)*df['radiation_norm'].values >
           df['power_norm'].values, 'flag'] = 1
    df.loc[df['radiation'].values > 1500, 'flag'] = 1
    df.loc[df['power'].values > cap*2, 'flag'] = 1
    df = df[np.isnan(df['flag']) == True]
    del df['flag']
    df = df.reset_index(drop=True)
    return df


def f_fit(x, A, n):
    return A*x**n


def autofit_line(data):
    # 曲线拟合
    x = data['radiation_norm'].tolist()
    y = data['power_norm'].tolist()
    A, n = optimize.curve_fit(f_fit, x, y)[0]
    return A, n


def fit_line(data):
    # 曲线拟合-直线
    a_para = np.tan(np.math.pi/np.linspace(2.5, 15, 20))
    para = pd.DataFrame(columns=['a', 'Distance'])
    para['a'] = a_para
    para['Distance'] = 0.0

    for i in range(len(a_para)):
        a = a_para[i]
        Distance_record = []
        for j in range(len(data)):
            Distance = distance(data['radiation_norm']
                                [j], data['power_norm'][j], a)
            Distance_record.append(Distance)
        Distance_sum = sum(Distance_record)
        para['Distance'][i] = Distance_sum
    a_best = para.loc[para['Distance'] == para['Distance'].min()]['a'].values
    n = 1
    return a_best, n


def distance(m, n, a):
    # 距离计算
    # 点：(m,n)，直线：ax-y+0=0
    b, c = -1, 0
    v1 = np.mat([m, n])
    v2 = np.mat([(b*b*m-a*b*n-a*c)/(a*a+b*b), (a*a*n-a*b*m-b*c)/(a*a+b*b)])
    Distance = np.sqrt((v1-v2)*((v1-v2).T))
    return Distance


def filter_limit(A, n, data, rate):
    # 异常数据剔除
    count, c = 0.0, 0.02
    df = data.copy()
    while (c < 0.3 and count < rate):
        df['flag'] = 0
        df['flag'].loc[(
            A*df['radiation_norm']**n + c > df['power_norm']
            ) & (A*df['radiation_norm']**n - c < df['power_norm'])] = 1

        count = float(sum(df['flag'].values))/len(df)
        c = c+0.02
    c = c-0.02
    df = df.loc[df['flag'] == 1]

    del df['flag'], df['radiation_norm'], df['power_norm']
    df = df.reset_index(drop=True)
    return df


def filter_AFF(A, n, data, rate):
    # 异常数据赋值
    count, c = 0.0, 0.02
    df = data.copy()
    while (c < 0.3 and count < rate):
        df['flag'] = 0
        df['flag'].loc[(A*df['radiation_norm']**n + c > df['power_norm'])
                       & (A*df['radiation_norm']**n - c < df['power_norm'])] = 1

        count = float(sum(df['flag'].values))/len(df)
        c = c+0.02
    c = c-0.02

    df.loc[df['flag'] == 0, 'power_norm'] = A*df['radiation_norm']**n

    del df['flag']
    df = df.reset_index(drop=True)
    return df
