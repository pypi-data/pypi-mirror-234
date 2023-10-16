# coding: utf8

import pandas as pd
# import algo_data as ad
ad = None
from datetime import datetime, timedelta
from PipeGraphPy.constants import DATATYPE
from . import InputDataBase
from .totalpower_utils import get_jsondata
from dbpoolpy import connect_db
from PipeGraphPy.constants import DB

now_date = (datetime.utcnow()+timedelta(hours=8))
end_day = (now_date - timedelta(days=1)).strftime('%Y-%m-%d')
start_day = (now_date - timedelta(days=31)).strftime('%Y-%m-%d')
atp_publish_path = '/mnt/pub/extract_data_third_party/zuoliye/WPF/'
PipeGraphPy_publish_path = '/mnt/sources/PipeGraphPy/report_json/'

class TotalPower(InputDataBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "start_dt",
            "name": "起始日期",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": start_day,
            "desc": "",
        },
        {
            "key": "end_dt",
            "name": "结束日期",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": end_day,
            "desc": "",
        },
        {
            "key": "plat",
            "name": "平台",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "PipeGraphPy",
            "source": ["atp", "PipeGraphPy"],
            "desc": "",
        },
        {
            "key": "forecast_source",
            "name": "预测源",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "report_gw",
            "source": ["report_gw", "report_farm", "graph"],
            "desc": ""
        }
    ]
    params_rules = {
        "start_dt": {
            "name": "起始日期",
            "type": str,
            "need": True
        },
        "end_dt": {
            "name": "结束日期",
            "type": str,
            "need": True
        },
        "plat": {
            "name": "平台",
            "type": str,
            "need": True,
            "source": ["atp", "PipeGraphPy"],
        },
        "forecast_source": {
            "name": "预测源",
            "type": str,
            "need": True,
            "source": ["report_gw", "report_farm", "graph"],
        }
    }
    def __init__(self, **kw):
        InputDataBase.__init__(self, **kw)
        self.params = kw
        self.graph_info = kw.get("graph_info")
        self.farm_info = kw.get("biz_info")

    def run(self):
        """运行,取训练数据"""
        # 判断是否是全网的电场
        if str(self.farm_info["wfname"]).find("全网") == -1:
            raise Exception("此电场不是全网电场，不能用此组件")
        return self._get_train_data(self.params['start_dt'], self.params['end_dt'])

    def _get_train_data(self, start_dt, end_dt):
        if self.farm_info["dispatch_name"] == "山西电网":
            feature_data = self._get_feature_data(start_dt, end_dt)
            label_data = self._get_label_data(start_dt, end_dt)
            train_data = pd.merge(feature_data, label_data, left_index=True, right_index=True, how="inner")
            if train_data.empty:
                raise Exception("不存在训练数据")

            return train_data
        else:
            return pd.DataFrame()

    def _get_feature_data(self, start_dt, end_dt):
        """获取仓库中的训练数据 """
        info_w = ad.farm_info(
            dispatch_name=self.farm_info["dispatch_name"],
            f_type=self.farm_info['f_type'],
            dtype='df',
        )
        info_w = info_w[info_w["wfid"]!=self.params["biz_info"]['wfid']]
        wfids = info_w['wfid'].values.tolist()
        if not wfids:
            raise Exception("未找到电场")

        fd =ad.ForecastData(plat=self.params['plat'])
        drop_columns = ['forecast_source', 'day_flag', 'mark', 'updatetime']
        obsdata = fd.get_data(
            wfid=wfids,
            forecast_source=self.params['forecast_source'],
            mark="12",
            start_dt=start_dt,
            end_dt=end_dt,
            day_flag=1,
            columns=['dtime', 'p_apower', 'wfid'] + drop_columns
        )
        drop_columns = [i for i in drop_columns if i in obsdata.columns]
        if drop_columns:
            obsdata = obsdata.drop(columns=drop_columns)
        obsdata = pd.pivot_table(
                obsdata, index='dtime', columns='wfid', values='p_apower').dropna()

        obsdata = obsdata.rename(columns={i:'p_apower_'+str(i) for i in obsdata.columns})
        obsdata['power_sum'] = obsdata.sum(axis=1)

        return obsdata

    def _get_energy_actual_df(self, start_dt, end_dt):
        sql = """
select
    dtime, r_wind_power, r_solar_power
from
    ods_et.ods_shanxi_140_province_actual_v
where dtime>='{}' and dtime<='{}'
""".format(start_dt, end_dt)
        with connect_db(DB.dbrs) as rsdb:
            datas = rsdb.query(sql)
            return pd.DataFrame(datas)


    def _get_label_data(self, start_dt, end_dt):
        """ 获取标签数据 """
        energy_actual = self._get_energy_actual_df(start_dt, end_dt)
        if energy_actual.empty:
            raise Exception("所选时间段没有总功率的实测数据")
        if self.farm_info["f_type"] == "W":
            energy_actual = energy_actual[["dtime", "r_wind_power"]].set_index("dtime").dropna()
            energy_actual["r_wind_power"] = energy_actual["r_wind_power"] * 1000
            energy_actual = energy_actual.rename(columns={"r_wind_power": "r_apower"})
            energy_actual["r_apower"] = energy_actual["r_apower"].astype(float)
        elif self.farm_info["f_type"] == "S":
            energy_actual = energy_actual[["dtime", "r_solar_power"]].set_index("dtime").dropna()
            energy_actual["r_solar_power"] = energy_actual["r_solar_power"] * 1000
            energy_actual = energy_actual.rename(columns={"r_solar_power": "r_apower"})
            energy_actual["r_apower"] = energy_actual["r_apower"].astype(float)
        else:
            raise ValueError("f_type参数错误")

        if energy_actual.empty:
            raise Exception("所选时间段没有总功率的实测数据")

        return energy_actual

    def evaluate(self):
        if self.params.get("periods"):
            evaluate_data = pd.DataFrame()
            for period in self.params["periods"]:
                data = self._get_train_data(period["s"], period["e"])
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            now_date = (datetime.utcnow()+timedelta(hours=8))
            evaluate_start= (
                    now_date - timedelta(days=int(self.params["windows"]))
                    ).strftime('%Y-%m-%d')
            evaluate_end = (now_date - timedelta(days=1)).strftime('%Y-%m-%d')
            evaluate_data = self._get_train_data(evaluate_start, evaluate_end)
        else:
            raise Exception("评估起止时间和评估窗口必存在一个参数")
        if evaluate_data.empty:
            self.stop_run("所选日期不存在训练数据，请修改训练数日期")
        return evaluate_data

    def predict(self):
        try:
            if self.params["plat"] == "atp":
                publish_path = atp_publish_path
            elif self.params["plat"] == "PipeGraphPy":
                publish_path = PipeGraphPy_publish_path
            else:
                raise ValueError("plat参数错误: %s" % self.params["plat"])
            json_data = get_jsondata(
                self.farm_info["dispatch_name"],
                self.farm_info["f_type"],
                self.params["clock"],
                publish_path=publish_path
            )
            json_data["power_sum"] = json_data.sum(axis=1)
            return json_data
        except Exception as e:
            raise e

