# coding: utf8
"""
作者: 郑水清
组件说明：
    组件通过sqlFilter组件过滤, 过滤到的数据走左边分支，过滤不到的组件走右边分支
参数示例：
    参考sqlFilter组件
"""

import pandas as pd
from custom.preprocessor.sqlfilter import SqlFilter


class SqlBranchSelect():
    OUTPUT = ["DataFrame", "DataFrame"]

    def __init__(self, **kw):
        self.params = kw

    def run(self, df):
        self.sql_filter = SqlFilter(**self.params)
        df_left = self.sql_filter.fit_transform(df)
        df_right = df[~df.index.isin(df_left.index)]
        return df_left, df_right

    def predict(self, df):
        df_left = self.sql_filter.transform(df)
        df_right = df[~df.index.isin(df_left.index)]
        return df_left, df_right

