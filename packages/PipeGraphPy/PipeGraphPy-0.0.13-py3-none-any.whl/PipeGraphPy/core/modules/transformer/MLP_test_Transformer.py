# coding:utf-8

import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator


class MLPTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, **kw):
        self.selector_param = kw
        self.__author__ = 'Song Dian'

    def Rmse(self, obs, pre):
        return np.sqrt(np.mean((obs - pre)**2))

    def transform(self, X):
        return X

    def fit(self, X, y=None):
        df = X.copy()
        obs = pd.DataFrame(columns=['r_wspd'])
        obs['r_wspd'] = y['r_wspd']
        del y['r_wspd']
        wth_list = list(df)
        wth_val = pd.DataFrame(columns=['name', 'val'])
        rmse_record = []
        for i in range(len(wth_list)):
            try:
                Data_Rmse = self.Rmse(
                    obs['r_wspd'].values, df[wth_list[i]].values)
                rmse_record.append(Data_Rmse)
            except Exception:
                rmse_record.append(None)
        wth_val['val'] = rmse_record
        wth_val['name'] = wth_list
        wth_val.sort_values('val', inplace=True)
        wth_val.reset_index(drop=True, inplace=True)
        wth_name = wth_val['name'][0:self.selector_param['Num']]
        X = X[wth_name]
        return self
