# coding: utf8

import pandas as pd
from PipeGraphPy.constants import DATATYPE
from . import AlgodataBase


class NwpData(AlgodataBase):
    __version__ = "0.1.0"
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "训练数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 30,
            "desc": "字段说明"
        },
        {
            "key": "reserve_length",
            "name": "保留数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": False,
            "value": 20,
            "desc": "字段说明"
        },
        {
            "key": "start_dt",
            "name": "起始日期",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "字段说明",
        },
        {
            "key": "end_dt",
            "name": "结束日期",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "字段说明",
        },
        {
            "key": "day_flag",
            "name": "气象预测天数标签",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "[1]",
            "desc": "day_flag",
        },
        {
            "key": "nwp_config",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "{'EC':['001'],'CMA':['001'],'GFS':['001'],'METE':['001'],'SUP':['001'],'MIX':['001'],'OPT':['001']}",
            "desc": "字段说明",
        },
        {
            "key": "feature",
            "name": "特征",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "['wspd_70']",
            "desc": "特征参量",
        },
    ]
    params_rules = {
        "data_length": {
            "name": "训练数据长度(天)",
            "type": int,
            "need": False,
            "range": [1, 1000],
            "source": [],
        },
        "reserve_length": {
            "name": "保留数据长度(天)",
            "type": int,
            "need": False,
            "range": [0, 500],
        },
        "day_flag": {
            "name": "气象预测天数标签",
            "type": list,
            "need": False,
        },
        "nwp_config": {
            "name": "预测数据气象源",
            "type": dict,
            "need": True,
            "range": [],
            "source": [],
        },
        "feature": {
            "name": "特征",
            "type": list,
            "need": False,
        },
    }


    @property
    def wth_source(self):
        return (
            [self.params["wth_source"]]
            if isinstance(self.params["wth_source"], str)
            else self.params["wth_source"]
        )

    def run(self):
        train_start, train_end = self._get_start_and_end_date()
        # 取气象
        train_data = self._gen_weather_data(
                start_dt=train_start,
                end_dt=train_end,
                nwp_config=self.params.get("nwp_config"),
                feature=self.feature,
                day_flag=self._prase_day_flag(),
                is_except=True)
        if train_data.empty:
            raise Exception("所选日期不存在训练数据，请修改训练数日期")

        return train_data


    def evaluate(self):
        evaluate_data = pd.DataFrame()
        if self.params.get("pub_date"):
            # 取气象
            pub_datetime = pd.to_datetime(self.params["pub_date"])
            pub_date = pub_datetime.strftime("%Y%m%d")
            evaluate_data = self._gen_predict_data_opt(
                    nwp_config=self.params.get("nwp_config"),
                    feature=self.feature,
                    clock=self.params.get("clock","12"),
                    pub_date=pub_date,
                    is_rt=False)

            if evaluate_data.empty:
                raise Exception("气象数据和实测数据合并后为空")
        elif self.params.get("periods"):
            for period in self.params["periods"]:
                data = self._gen_weather_data(
                        start_dt=period["s"],
                        end_dt=period["e"],
                        nwp_config=self.params.get("nwp_config"),
                        feature=self.feature,
                        day_flag=self._prase_day_flag(),
                        is_except=True)
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            windows = self.params["windows"]
            evaluate_start, evaluate_end = self._prase_date(windows)
            evaluate_data = self._gen_weather_data(
                    start_dt=evaluate_start,
                    end_dt=evaluate_end,
                    nwp_config=self.params.get("nwp_config"),
                    feature=self.feature,
                    day_flag=self._prase_day_flag(),
                    is_except=True)
        else:
            raise ValueError("没达到取评估数据的条件")

        return evaluate_data

