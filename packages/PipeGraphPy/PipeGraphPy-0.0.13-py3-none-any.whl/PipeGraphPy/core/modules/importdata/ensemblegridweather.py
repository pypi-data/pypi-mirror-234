# coding: utf8

import pandas as pd
# import algo_data
algo_data = None
from PipeGraphPy.config import settings
from datetime import datetime, timedelta
from PipeGraphPy.constants import DATATYPE, FARMTYPE
from . import InputDataBase
# from algo_data import Ensemble_Grid_Reader
Ensemble_Grid_Reader = None


class EnsembleGridWeather(InputDataBase):
    __version__ = "ensemble_grid_reader V0.0.11"
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 10,
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
            "name": "开始日期",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "",
        },
        {
            "key": "end_dt",
            "name": "结束日期",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "",
            "desc": "",
        },
        {
            "key": "lon_index1",
            "name": "经度1",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": -5,
            "desc": "",
        },
        {
            "key": "lon_index2",
            "name": "经度2",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 5,
            "desc": "",
        },
        {
            "key": "lat_index1",
            "name": "纬度1",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": -5,
            "desc": "",
        },
        {
            "key": "lat_index2",
            "name": "纬度2",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 5,
            "desc": "",
        },
        {
            "key": "nwp_source",
            "name": "气象源",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "EC",
            "source": ["EC", "GFS"],
            "desc": "",
        },
        {
            "key": "col_list",
            "name": "特征列",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "['wspd_10','wspd_100']",
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
            "key": "check_result",
            "name": "实测数据异常类型",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "[0]",
            "desc": "",
        },
    ]
    params_rules = {
        "data_length": {
            "name": "数据长度(天)",
            "type": int,
            "need": True,
            "range": [1, 1000],
            "source": [],
        },
        "reserve_length": {
            "name": "保留数据长度(天)",
            "type": int,
            "need": False,
            "range": [0, 500],
        },
        "lon_index1": {
            "name": "经度1",
            "type": int,
            "need": True,
            "range": [-180, 180],
        },
        "lon_index2": {
            "name": "经度2",
            "type": int,
            "need": True,
            "range": [-180, 180],
        },
        "lat_index1": {
            "name": "纬度1",
            "type": int,
            "need": True,
            "range": [-90, 90],
        },
        "lat_index2": {
            "name": "纬度2",
            "type": int,
            "need": True,
            "range": [-90, 90],
        },
        "nwp_source": {
            "name": "气象源",
            "type": str,
            "need": True,
            "source": ["EC", "GFS"],
        },
        "col_list": {
            "name": "特征列",
            "need": True,
        },
        "out_col": {
            "name": "返回数据列名称",
            "type": list,
            "need": True,
            "source": ["r_apower", "r_wspd", "r_tirra"],
        },
        "check_result": {
            "name": "实测数据异常类型",
            "type": list,
            "need": True,
        },
    }

    def __init__(self, **kw):
        InputDataBase.__init__(self, **kw)
        graph_info = kw["graph_info"]
        self.wfid = graph_info["biz_id"]
        self.farm_info = self.params["biz_info"]

    def _get_obs_data(self, start_dt, end_dt, columns=["r_apower"]):
        """调用algo_data接口，获取数据库obs_data实测数据"""
        columns = ["dtime"] + columns if "dtime" not in columns else columns
        obs_where = dict(
            wfid=self.wfid,
            layer='dwd',
            start_dt=start_dt,
            end_dt=end_dt,
            columns=','.join(columns)
        )
        if self.params.get("check_result"):
            obs_where["check_result"] = self.params.get("check_result")
        return algo_data.obs_15min(**obs_where)

    def _get_nc_data(self, start_dt, end_dt, out_col, phase="train", is_cal=0):
        """取nc数据"""
        st, et = pd.to_datetime(start_dt), pd.to_datetime(end_dt)
        st, et = st.strftime("%Y%m%d"), et.strftime("%Y%m%d")
        if phase == "train":
            read_nc = Ensemble_Grid_Reader(
                wfid=self.wfid,
                nwp_soure=self.params["nwp_source"],
                kw={
                    'lon_index1' : self.params["lon_index1"],
                    'lon_index2' : self.params["lon_index2"],
                    'lat_index1' : self.params["lat_index1"],
                    'lat_index2' : self.params["lat_index2"],
                },
                col_list=self.params["col_list"])
            grid_data = read_nc.generate_DataFrame_train(
                    st=st,
                    et=et,
                    out_col=out_col,
                    check_result=self.params["check_result"],
                    is_cal=is_cal)
            if self.params.get("limit_type"):
                # 获取实测数据
                obs_data = self._get_obs_data(
                        start_dt=start_dt,
                        end_dt=end_dt,
                        columns=[self.params["limit_type"]])

                if not obs_data.empty and self.params["limit_type"] in obs_data.columns:
                    grid_data = grid_data.merge(
                            obs_data,
                            left_index=True,
                            right_on='dtime',
                            how='left').set_index("dtime")
                    grid_data[self.params["limit_type"]] = grid_data[self.params["limit_type"]].fillna(-1)
            return grid_data
        elif phase == 'predict':
            read_nc = Ensemble_Grid_Reader(
                wfid=self.wfid,
                nwp_soure=self.params["nwp_source"],
                kw={
                    'lon_index1' : self.params["lon_index1"],
                    'lon_index2' : self.params["lon_index2"],
                    'lat_index1' : self.params["lat_index1"],
                    'lat_index2' : self.params["lat_index2"],
                },
                col_list=self.params["col_list"],
                env='aws' if settings.USE_119_PGP and not settings.IS_AWS_BAK else 'local')
            return read_nc.generate_DataFrame_predict(
                    st=st, et=et, mark=self.params.get("clock", "12"))
        else:
            raise ValueError("phase值错误")

    def check_and_modify_index(self, data:pd.DataFrame):
        """检查df的索引是否为dtime，如不是，则进行修改

        Args:
            data (pd.DataFrame): 需要检查和修改的df
        """

        if data.index.name != 'dtime':
            print("f{self.__class__.__name__} -> index 修改为'dtime'，原为{data.index.name}")
            data.index.name = 'dtime'

        return data

    def run(self):
        """运行"""
        # 判断是否用理论功率
        train_start, train_end = self._get_start_and_end_date()
        train_data = self._get_nc_data(
                train_start, train_end, self.params.get("out_col"))
        train_data = self.check_and_modify_index(train_data)
        return train_data

    def evaluate(self):
        out_col = self.params.get("out_col")
        if self.params.get("limit_type") in ["limit_auto", "limit_artificial"]:
            if self.farm_info["f_type"] == FARMTYPE.WIND and "r_wspd" not in out_col:
                out_col.append("r_wspd")
            elif self.farm_info["f_type"] == FARMTYPE.PV and "r_tirra" not in out_col:
                out_col.append("r_tirra")
        if self.params.get("periods"):
            evaluate_data = pd.DataFrame()
            for period in self.params["periods"]:
                data = self._get_nc_data(period["s"], period["e"], out_col=out_col)
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            windows = self.params["windows"]
            evaluate_start, evaluate_end = self._prase_date(windows)
            evaluate_data = self._get_nc_data(
                    evaluate_start, evaluate_end, out_col=out_col)
        else:
            raise Exception("评估起止时间和评估窗口必存在一个参数")
        if evaluate_data.empty:
            raise Exception("所选日期不存在训练数据，请修改训练数日期")
        evaluate_data = self.check_and_modify_index(evaluate_data)
        if self.params.get("day_flag") and "day_flag" in evaluate_data.columns:
            day_flags = [self.params["day_flag"]] if not isinstance(self.params["day_flag"], list) else self.params["day_flag"]
            evaluate_data = evaluate_data[evaluate_data["day_flag"].isin(day_flags)]
        return evaluate_data

    def predict(self):
        """预测"""
        try:
            this_day = lambda x:(pd.to_datetime(x)-timedelta(days=1)).strftime("%Y-%m-%d")
            if self.params.get("predict_start_dt") and self.params.get("predict_end_dt"):
                start_day = this_day(self.params["predict_start_dt"])
                end_day = this_day(self.params["predict_end_dt"])
                predict_df = self._get_nc_data(
                        start_day, end_day, self.params.get("out_col"),  is_cal=1)
            elif self.params.get("predict_date"):
                pred_dt = this_day(self.params["predict_date"])
                predict_df = self._get_nc_data(
                        pred_dt, pred_dt, self.params.get("out_col"), is_cal=1)
            else:
                """
                例：2022-09-02预测的话,EC是
                根据需求来，st=2022-09-03 ，et=（2022-09-03 到 2022-09-12 中间的任意)
                注意：取数据多时在预测时会造成内存过大
                """
                source=self.params["nwp_source"],
                pred_start_dt = (
                        (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=1)
                        ).strftime("%Y-%m-%d")
                predict_days = 2 if self.params.get("clock") == "00" else 1
                if source == 'GFS':
                    pred_end_dt = (
                            (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=predict_days)  # 最大9,只取1
                            ).strftime("%Y-%m-%d")
                else:
                    pred_end_dt = (
                            (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=predict_days) # 最大9天, 只取1
                            ).strftime("%Y-%m-%d")
                predict_df = self._get_nc_data(
                        pred_start_dt, pred_end_dt, out_col=None, phase='predict')
            if not predict_df.empty:
                predict_df = predict_df[[i for i in predict_df.columns if not str(i).startswith("r_")]]
            predict_df = predict_df.dropna()
            if not isinstance(predict_df, pd.DataFrame) or predict_df.empty:
                raise Exception("未取到预测使用的集合网格数据")
            if not predict_df.index.name:
                predict_df.index.name = 'dtime'
            return predict_df
        except Exception as e:
            raise e

