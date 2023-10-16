# coding: utf-8

"""
特征选择模块
"""

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


def fscore_select(model):
    X = model.train_data[model.feature_columns]
    y = model.train_data[model.out_col]

    X_new = SelectKBest(f_regression, k=model.n_feature).fit(
        StandardScaler().fit_transform(X.values.reshape(X.shape[0], -1)),
        StandardScaler().fit_transform(y.values.reshape(y.shape[0], -1)))
    # print(X_new.get_support())
    # X_new = SelectKBest(f_regression, k=self.n_feature).fit(X, y)
    return X.loc[:, X_new.get_support()]


def rmse_select(model):
    X = model.train_data[model.feature_columns]
    if model.feature == ['speed']:
        y = model.train_data[['wspd']]
    else:
        y = model.train_data[['radiations']]

    def _rmse(x): return np.sqrt(np.mean((x[0] - x[1]) ** 2))
    rmse_score = []
    for col, cols in X.items():
        rmse_score.append(
            [col, _rmse((cols.values, y.values.reshape(y.shape[0], -1)))])
    rmse_score = pd.DataFrame(rmse_score, columns=['col', 'value'])
    rmse_score = rmse_score.sort_values(by='value')
    # print(rmse_score)
    return X.loc[:, rmse_score.head(model.n_feature)['col'].tolist()]
