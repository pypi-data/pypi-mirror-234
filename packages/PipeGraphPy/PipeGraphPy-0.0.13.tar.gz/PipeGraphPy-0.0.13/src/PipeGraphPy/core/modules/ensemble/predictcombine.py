# coding: utf8

import pandas as pd
from PipeGraphPy.constants import DATATYPE
from PipeGraphPy.core.modules import MBase


class PredictCombine(MBase):
    TEMPLATE = [
        {
            "key": "replace",
            "name": "是否替换相同时间数据",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "是",
            "source": ["是", "否"],
            "desc": "是否替换基数据",
        },
        {
            "key": "is_add",
            "name": "是否增加不同时间数据",
            "type": "string",
            "plugin": "select",
            "need": False,
            "value": "是",
            "source": ["是", "否"],
            "desc": "是否合并不同时间数据",
        },
        {
            "key": "drop_unmatch",
            "name": "是否去掉不相同的列",
            "type": "string",
            "plugin": "select",
            "need": False,
            "value": "是",
            "source": ["是", "否"],
            "desc": "是否去掉不相同的列",
        },
    ]
    params_rules = {
        "replace": {
            "name": "是否替换相同时间数据",
            "type": str,
            "need": True,
            "source": ["是", "否"],
        },
        "is_add": {
            "name": "是否增加不同时间数据",
            "type": str,
            "need": False,
            "source": ["是", "否"],
        },
        "drop_unmatch": {
            "name": "是否去掉不相同的列",
            "type": str,
            "need": False,
            "source": ["是", "否"],
        },
    }

    def __init__(self, **kw):
        self.params = kw

    def predict(self, df, other_df:dict):
        combine_df = df.copy()
        df_list = list(other_df.values())
        if df_list:
            if self.params["replace"] == "是":
                combine_df = combine_df.append(df_list)
                if "day_flag" in combine_df.columns:
                    combine_df = combine_df.groupby([combine_df.index, 'day_flag']).last().reset_index('day_flag').sort_index()
                else:
                    combine_df = combine_df.groupby(combine_df.index).last().sort_index()
                if not self.params.get("drop_unmatch") or self.params["drop_unmatch"] == "是":
                    combine_df.dropna(axis=1, how='any', inplace=True)
            else:
                combine_df = combine_df.append(df_list).sort_index()
            if self.params.get("is_add") and self.params["is_add"] == "否":
                combine_df = combine_df[combine_df.index.isin(df.index)]

        return combine_df

