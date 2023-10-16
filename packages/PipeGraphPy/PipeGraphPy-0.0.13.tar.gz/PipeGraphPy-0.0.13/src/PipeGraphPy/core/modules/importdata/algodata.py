# coding: utf8

# from collections import defaultdict
from PipeGraphPy.constants import FARMTYPE
from PipeGraphPy.constants import DATATYPE
from . import AlgodataBase

DATAWAREHOUSE = "数仓"

"""
feature = [
    "ghi_sfc",
    "tskin_sfc",
    "tdew2m_sfc",
    "rain_sfc",
    "snow_sfc",
    "clflo_sfc",
    "clfmi_sfc",
    "clfhi_sfc",
    "wspd_10",
    "wspd_30",
    "wspd_50",
    "wspd_70",
    "wdir_10",
    "wdir_30",
    "wdir_50",
    "wdir_70",
    "rh_2",
    "p_sfc",
    "rhoair_2",
    "t_2",
    "clfal_sfc",
]
"""


class Algodata(AlgodataBase):
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
            "key": "out_col",
            "name": "返回数据列名称",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "['r_apower', 'r_wspd']",
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
            "value": "{'EC':['001'],'CMA':['001'],'GFS':['001']}",
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
        {
            "key": "check_result",
            "name": "实测数据异常类型",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "[0]",
            "desc": "字段说明",
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
        "out_col": {
            "name": "返回数据列名称",
            "type": list,
            "need": True,
            "range": [],
            "source": ["r_apower", "r_wspd", "r_tirra"],
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
        "check_result": {
            "name": "实测数据异常类型",
            "type": list,
            "need": False,
        },
    }

    def _get_data(self):
        """获取训练数据和测试数据"""
        # 判断是否是自动获取气象源
        if (
            self.farm_info["f_type"] == FARMTYPE.WIND
            and "r_tirra" in self.params["out_col"]
        ):
            raise Exception("风电场%s不能配置辐照度实测值" % self.graph_info["id"])
        elif (
            self.farm_info["f_type"] == FARMTYPE.PV
            and "r_wspd" in self.params["out_col"]
        ):
            raise Exception("光伏电场%s不能配置风速实测值" % self.graph_info["id"])

        train_start, train_end = self._get_start_and_end_date()
        train_data, obs_data, weather_data = self._get_train_data(
            nwp_config=self.params.get("nwp_config"),
            out_col=self.params.get("out_col"),
            start_dt=train_start,
            end_dt=train_end,
            feature=self.feature,
            day_flag=self._prase_day_flag()
        )
        if train_data.empty:
            raise Exception("所选日期不存在训练数据，请修改训练数日期")

        return train_data
