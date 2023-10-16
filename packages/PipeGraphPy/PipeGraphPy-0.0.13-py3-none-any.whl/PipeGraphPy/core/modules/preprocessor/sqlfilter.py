# coding:utf8
"""
作者: 郑水清
组件说明：
    组件使用pandasql三方库对X和y做sql的过滤处理

参数示例：
    {'sql': 'select * from X where day_flag=1', 'fit_sql': 'select * from X where day_flag=2', 'predict_sql': 'select * from X'}

参数说明：
    1.params中需要有sql参数，否则起不到过滤的作用
    2.sql可以使用表名X和y, 其他的无效
    3.训练时优先使用fit_sql参数，fit_sql不存在再使用sql参数
    4.预测时优先使用predict_sql参数, predict_sql不存在再使用sql参数

"""
import pandas as pd
from pandasql import sqldf

class SqlFilter():
    __version__ = '0.0.1'
    def __init__(self, **kw):
        self.params = kw
        self.farm_info = kw.get('biz_info')

    def _sqlfilter(self, sql, X, y=None):
        X, y = X, pd.DataFrame() if y is None else y
        if sql:
            filter_X = sqldf(sql, locals())
            filter_X = filter_X.set_index(X.index.name)
            filter_X.index = filter_X.index.astype(X.index.dtype)
            X = filter_X
        return X

    def transform(self, X):
        sql = self.params.get('predict_sql') or self.params.get('sql')
        return self._sqlfilter(sql, X)

    def fit_transform(self, X, y=None):
        sql = self.params.get('fit_sql') or self.params.get('sql')
        return self._sqlfilter(sql, X, y)
