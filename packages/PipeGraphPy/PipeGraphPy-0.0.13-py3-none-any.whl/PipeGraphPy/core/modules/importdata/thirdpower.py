# coding: utf8

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PipeGraphPy.constants import DATATYPE
from dbpoolpy import connect_db
from PipeGraphPy.constants import DB, dbrt
from . import AlgodataBase

DATAWAREHOUSE = "数仓"

# 三方数据tar包保存地址: /data/algo/data_file
this_year = (datetime.utcnow()+timedelta(hours=8)).strftime("%Y")

wth2file_path = {
    "ML": "/data/algo/data_file/third_ML/%s/Goldwind-{thirdparty_id}/Goldwind-{thirdparty_id}-{aim_date}0600.csv" % this_year,
    "CONWX": "/data/algo/data_file/conwx/Goldwind-{thirdparty_id}/Goldwind-{thirdparty_id}-{aim_date}0530.csv",
    "MF": "/data/algo/data_file/third_MF/Goldwind-{thirdparty_id}/meteoforce_Goldwind-{thirdparty_id}_{aim_date}06_power.csv",
    # "GOA": "/mnt/correct/GOA/Goldwing-{thirdparty_id}/Goldwind-{thirdparty_id}-{aim_date}0600.csv",
    "XZ": "/data/algo/data_file/XZ/Goldwind-{thirdparty_id}/Goldwind-{thirdparty_id}-{aim_date}0630.csv",
}
datetime_format = "%Y-%m-%d %H:%M:%S"
wth2dateformat = {
    "ML": "%Y-%m-%d %H:%M",
    "CONWX": "%Y-%m-%d %H:%M",
    "MF": "%Y-%m-%d %H:%M:%S",
    # "GOA": "%Y-%m-%d %H:%M:%S",
    "XZ": "%Y-%m-%d %H:%M:%S",
}
x_field_name = "{wth}_power"
y_field_name = "r_apower"


class ThirdPower(AlgodataBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "训练数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 100,
            "desc": "字段说明",
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
            "key": "has_r_apower",
            "name": "是否取实测功率",
            "type": "string",
            "plugin": "select",
            "need": False,
            "value": "否",
            "source": ['否', '是'],
            "desc": "字段说明",
        },
        {
            "key": "wth_source",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "MF",
            "source": ['ML', 'CONWX', 'MF', 'XZ'],
            "desc": "字段说明",
        },
        {
            "key": "day_flag",
            "name": "气象预测天数标签",
            "type": "int",
            "plugin": "select",
            "need": True,
            "value": 1,
            "source": [1,2,3,4,5,6,7,8,9,10],
            "desc": "day_flag",
        },
        {
            "key": "data_clock",
            "name": "时间点",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "06",
            "source": ["00", "05", "06", "12"],
            "desc": "字段说明"
        },
    ]
    params_rules = {
        "data_length": {
            "name": "训练数据长度(天)",
            "type": int,
            "need": False,
            "range": [1, 1000],
        },
        "reserve_length": {
            "name": "保留数据长度(天)",
            "type": int,
            "need": False,
            "range": [0, 500],
        },
        "has_r_apower": {
            "name": "是否取实测功率",
            "type": str,
            "need": False,
        },
        "wth_source": {
            "name": "预测数据气象源",
            "type": str,
            "need": True,
            "source": ['ML', 'CONWX', 'MF', 'XZ'],
        },
        "day_flag": {
            "name": "气象预测天数标签",
            "type": int,
            "need": True,
            "source": [1,2,3,4,5,6,7,8,9,10],
        },
        "data_clock": {
            "name": "时间点",
            "type": str,
            "need": True,
            "source": ["00", "05", "06", "12"],
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
        train_data = self.get_thirdpower_data(train_start, train_end)
        if train_data.empty:
            raise Exception("所选日期不存在训练数据，请修改训练数日期")
        return train_data

    def evaluate(self):
        if self.params.get("periods"):
            evaluate_data = pd.DataFrame()
            for period in self.params["periods"]:
                data = self.get_thirdpower_data(period["s"], period["e"])
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            windows = self.params["windows"]
            evaluate_start, evaluate_end = self._prase_date(windows)
            evaluate_data = self.get_thirdpower_data(evaluate_start, evaluate_end)
        else:
            raise Exception("评估起止时间和评估窗口必存在一个参数")
        if evaluate_data.empty:
            self.stop_run("所选日期不存在训练数据，请修改训练数日期")
        return evaluate_data


    def _get_predict_df_from_rt(self, aim_date):
        # 取实时库的第三方数据
        nwp_start_time = aim_date + self.params["data_clock"]
        third_df = pd.DataFrame()
        with connect_db(dbrt) as rtdb:
            third_forecast_data = rtdb.select(
                           "ods_json.ods_short_third_forecast"
                       ).fields(
                           "dtime, p_apower, day_flag"
                       ).where(
                           wfid=self.wfid,
                           nwp_start_time=nwp_start_time,
                           forecast_source=("in", self.wth_source),
                           mark=self.params["data_clock"]
                       ).all()
            if not third_forecast_data:
                raise Exception(
                        "数据库ods_json.ods_short_third_forecast不存在"
                        "nwp_start_time:%s, forecast_source: %s, mark: %s 的三方数据" % (
                            nwp_start_time, self.wth_source, self.params["data_clock"]
                            ))
            if third_forecast_data:
                third_forecast_df = pd.DataFrame(third_forecast_data)
                renames = {"p_apower":x_field_name.format(wth=self.params["wth_source"])}
                third_df = third_forecast_df.rename(columns=renames).set_index("dtime")
        return third_df

    def _get_predict_df(self, aim_date):
        """获取第三方数据"""
        predict_df = self._get_predict_df_from_rt(aim_date)
        if predict_df.empty:
            try:
                predict_df = self.get_thirdpower_file_data(aim_date)
            except:
                pass
        if predict_df.empty:
            raise Exception("没取到预测数据")
        return predict_df

    def predict(self):
        if self.params.get("predict_start_dt") and self.params.get("predict_end_dt"):
            date_list = pd.date_range(
                    self.params["predict_start_dt"],
                    self.params["predict_end_dt"],
                    freq="D")
            if self.params["data_clock"] in ["00", "05", "06"]:
                aim_dates = [(i-timedelta(days=1)).strftime("%Y%m%d") for i in date_list]
            else:
                aim_dates = [(i-timedelta(days=2)).strftime("%Y%m%d") for i in date_list]
        elif self.params.get("predict_date"):
            if self.params["data_clock"] in ["00", "05", "06"]:
                aim_dates = [(pd.to_datetime(self.params["predict_date"])-timedelta(days=1)).strftime("%Y%m%d")]
            else:
                aim_dates = [(pd.to_datetime(self.params["predict_date"]
                    )-timedelta(days=2)).strftime("%Y%m%d")]
        else:
            if self.params["data_clock"] in ["00", "05", "06"]:
                aim_dates = [((datetime.utcnow()+timedelta(hours=8))).strftime("%Y%m%d")]
            else:
                aim_dates = [((datetime.utcnow()+timedelta(hours=8)) - timedelta(days=1)
                    ).strftime("%Y%m%d")]
        predict_df = pd.DataFrame()
        for d in aim_dates:
            data = self._get_predict_df(d)
            predict_df = predict_df.append(data)
        if predict_df.empty:
            raise Exception("未取到预测数据")
        return predict_df

    def _get_third_from_db(self, start_time, end_time):
        thirdpower_df = pd.DataFrame()
        # 获取第三方功率数据
        table = "ods_forecast.ods_short_forecast_di"
        end_time = pd.to_datetime(end_time) + timedelta(hours=23, minutes=59)

        with connect_db(DB.dbrs) as rsdb:
            thirdpower_data = rsdb.select(table).where(
                wfid=self.wfid,
                dtime=("between", [str(start_time), str(end_time)]),
                mark=self.params.get("data_clock", "12"),
                forecast_source=("in", ["third_%s" % i for i in self.wth_source]),
                day_flag = self.params["day_flag"]
                ).all()
            thirdpower_df = pd.DataFrame(thirdpower_data)
        if thirdpower_df.empty:
            return thirdpower_df

        third_df = thirdpower_df.pivot_table(
                index=["dtime", "day_flag"], columns='forecast_source', values="p_apower").reset_index()
        renames = {f"third_{i}":x_field_name.format(wth=i) for i in self.wth_source}
        third_df = third_df.rename(columns=renames)
        return third_df

    def get_thirdpower_data(self, start_time, end_time):
        """从数据库获取第三方功率数据"""

        # 获取三方预测
        thirdpower_df = self._get_third_from_db(start_time, end_time)
        if thirdpower_df.empty:
            raise Exception("所选日期(%s,%s), 不存在第三方功率数据" % (start_time, end_time))
        thirdpower_df = thirdpower_df.set_index("dtime")

        if self.params.get("has_r_apower") and self.params["has_r_apower"] == "是":
            # 获取实测数据
            obs_data = self._get_obs_data(start_time, end_time)
            if obs_data.empty:
                raise Exception("所选日期(%s,%s), 不存在实测功率数据" % (start_time, end_time))
            obs_data = obs_data.set_index("dtime")

            # 合并预测和实测数据
            thirdpower_df = pd.merge(
                thirdpower_df, obs_data, left_index=True, right_index=True, how="inner"
            )
        return thirdpower_df

    def open_csv_as_df(self, file_path):
        try:
            return pd.read_csv(file_path)
        except Exception:
            # self.log(l_type="p", level="warning", msg=traceback.format_exc())
            return pd.DataFrame()

    def get_thirdpower_file_data(self, aim_date):
        """获取预测所需数据"""
        thirdpower_df = pd.DataFrame()
        thirdparty_id = self.farm_info["thirdparty_id"]
        for wth in self.wth_source:
            file_path = wth2file_path[wth].format(
                thirdparty_id=thirdparty_id, aim_date=aim_date
            )
            df = self.open_csv_as_df(file_path)
            if df.empty:
                # self.log(l_type="p", level="warning", msg="未获取到要预测的文件：%s" % file_path)
                continue
            col = [i for i in df.columns if i.startswith("Date")] + [
                i for i in df.columns if i.startswith("Power")
            ]
            # 列名重命名
            df = df[col].rename(
                columns={col[0]: "dtime", col[1]: x_field_name.format(wth=wth)}
            )
            # 修改dtime的日期格式
            df["dtime"] = pd.to_datetime(df["dtime"], format=wth2dateformat[wth])
            # df["dtime"] = df["dtime"].dt.strftime(datetime_format)
            # 设置dtime为索引
            df = df.set_index("dtime")
            if thirdpower_df.empty:
                thirdpower_df = df
            else:
                thirdpower_df = pd.merge(
                    thirdpower_df, df, left_index=True, right_index=True, how="inner"
                )
        # 如果列不存在则使用其他列补上
        for wth in self.wth_source:
            col = x_field_name.format(wth=wth)
            if col not in thirdpower_df.columns:
                thirdpower_df[col] = thirdpower_df[thirdpower_df.columns[0]]

        return thirdpower_df
