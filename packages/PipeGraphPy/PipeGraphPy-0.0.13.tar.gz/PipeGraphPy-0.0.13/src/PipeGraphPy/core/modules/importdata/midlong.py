# coding: utf8

import copy
import datetime
import pandas as pd
# from algo_data.utils import uv2wswd
uv2wswd = None
from functools import reduce

from PipeGraphPy.constants import DATATYPE, DB, dbrt
from .algodata import Algodata
from dbpoolpy import Select, connect_db

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

def one_weather(
     wfid,
     forecast_source:str,
     stn_id:str,
     feature:str,
     start_dt=None,
     end_dt=None,
     mark='12',
     is_predict=False
    ):
    if not is_predict and not (start_dt and end_dt):
        raise Exception("取训练数据要存在start_dt和end_dt")

    inp_feature = set(feature) & set(["wspd_10", "wdir_10"])
    all_feature = copy.copy(feature)
    index_feature = ['day_flag', 'dtime']

    if inp_feature:
        all_feature.extend(["v_10", "u_10"])
        all_feature = list(set(all_feature) - inp_feature)

    if is_predict:
        # 预测取实时库
        table = "nwpdb.farm_%s" % wfid
        with connect_db(DB.dbrt) as rtdb:
            # 取最新的nwp_start_time
            nwp_info = rtdb.select(table).where(
                    forecast_source=forecast_source,
                    stn_id=stn_id,
                    mark=mark
                    ).order_by("nwp_start_time desc").first()
            if not nwp_info:
                return pd.DataFrame()
            recent_nwp_start_time = nwp_info["nwp_start_time"]
            weather_data = rtdb.select(table).where(
                    forecast_source=forecast_source,
                    nwp_start_time=recent_nwp_start_time,
                    stn_id=stn_id,
                    mark=mark
                    ).fields(*list(all_feature+index_feature)).all()
    else:
        # 训练取数仓
        table = "ods_nwp.ods_nwp_%s" % wfid
        weather_data = Select(DB.dbrs, table).where(
                forecast_source=forecast_source,
                mark=mark,
                day_flag=("between", [1, 200]),
                stn_id=stn_id,
                dtime=("between", [start_dt, end_dt]),
                ).fields(*list(all_feature+index_feature)).all()
    weather_df = pd.DataFrame(weather_data)
    if weather_df.empty:
        return weather_df

    # 按dtime一样的取day_flag最小的
    nwp_df = weather_df.sort_values(["dtime", "day_flag"]).groupby(
            ["dtime"], as_index=False).first()

    if inp_feature:
        wspd_10, wdir_10 = uv2wswd(nwp_df["u_10"],nwp_df["v_10"])
        if "wspd_10" in feature:
            nwp_df["wspd_10"] = wspd_10
        if "wdir_10" in feature:
            nwp_df["wdir_10"] = wdir_10
        if "u_10" not in feature:
            nwp_df.drop("u_10", axis=1, inplace=True)
        if "v_10" not in feature:
            nwp_df.drop("v_10", axis=1, inplace=True)

    # 重命名列名
    columns_rename = {c:'%s_%s_%s' % (forecast_source, c, stn_id) for c in feature}
    nwp_df = nwp_df.rename(columns=columns_rename)
    return nwp_df

def multi_weather(
         wfid,
         feature:str,
         nwp_config:dict,
         start_dt=None,
         end_dt=None,
         mark="12",
         is_predict=False
        ):
    datas = []
    for forecast_source, stn_id in nwp_config.items():
        stnids = stn_id if isinstance(stn_id, list) else [stn_id]
        for stnid in stnids:
            data = one_weather(
                wfid=wfid,
                start_dt=start_dt,
                end_dt=end_dt,
                forecast_source=forecast_source,
                stn_id=stnid,
                feature=feature,
                mark=mark,
                is_predict=is_predict
                )
            datas.append(data)
    if len(datas) == 1:
        df = datas[0]
    elif len(datas) == 0:
        return pd.DataFrame()
    else:
        df = reduce(
            lambda left,right: pd.merge(left, right, how='outer', on=["dtime", "day_flag"]),
            datas)
    return df


class MidLong(Algodata):
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "训练数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 180,
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
            "name": "实测数据列名称",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "['r_apower', 'r_wspd']",
            "desc": "字段说明",
        },
        {
            "key": "obs_source",
            "name": "实测数据源",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "数仓",
            "source": ["数仓"],
            "desc": "字段说明",
        },
        {
            "key": "nwp_config",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "{'CFS01':['001']}",
            "desc": "字段说明",
        },
        {
            "key": "feature",
            "name": "特征",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "['u_10', 'v_10', 'wspd_10']",
            "desc": "特征参量",
        },
        {
            "key": "is_defect",
            "name": "去除有缺陷数据",
            "type": "string",
            "plugin": "select",
            "need": False,
            "value": "是",
            "source": ["是", "否"],
            "desc": "字段说明",
        },
    ]
    params_rules = {}

    def _get_rt_data(
        self,
        feature=["wspd_70"],
        nwp_config=None,
        mark="12",
    ):
        rt_df = multi_weather(
                self.wfid, feature, nwp_config, mark=mark, is_predict=True)
        if rt_df.empty:
            raise Exception("未取到预测数据")
        rt_df = rt_df.set_index("dtime")
        return rt_df



    def _gen_weather_data(
        self,
        start_dt,
        end_dt,
        nwp_config,
        feature=["wspd_10"],
        day_flag=1,
        is_except=True
    ):
        weather_data =  multi_weather(
                self.wfid, feature, nwp_config, start_dt, end_dt)
        if weather_data.empty:
            raise Exception("未取到气象数据")
        weather_data = weather_data.set_index("dtime")
        return weather_data


    def predict(self):
        try:
            nwp_data = self._get_rt_data(
                nwp_config=self.params.get("nwp_config"),
                feature=self.feature,
                mark=self.params.get("clock", "12"),
            )
            if nwp_data.empty:
                raise Exception("读取气象文件失败")
            return nwp_data
        except Exception as e:
            raise e

