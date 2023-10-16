# coding: utf8

# import algo_data
algo_data = None
import pandas as pd
from datetime import datetime, timedelta
from PipeGraphPy.constants import DATATYPE, FARMTYPE
from PipeGraphPy.config import settings
from . import InputDataBase, day_flag_pattern
# from algo_data import ReadNc2D
ReadNc2D = None
# from algo_data import ReadNc2DTrain, ReadNc2DPredict
ReadNc2DTrain = None
ReadNc2DPredict = None


class GridWeather(InputDataBase):
    __version__ = "0.0.3"
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
            "value": -10,
            "desc": "",
        },
        {
            "key": "lon_index2",
            "name": "经度2",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 10,
            "desc": "",
        },
        {
            "key": "lat_index1",
            "name": "纬度1",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": -10,
            "desc": "",
        },
        {
            "key": "lat_index2",
            "name": "纬度2",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 10,
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
            "value": "['wspd_10m','wspd_100m']",
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
        {
            "key": "day_flag",
            "name": "气象预测天数标签",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "[1]",
            "desc": "day_flag",
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
        "day_flag": {
            "name": "气象预测天数标签",
            "type": list,
            "need": False,
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

    def _prase_day_flag(self):
        """解析day_flag"""
        if not self.params.get("day_flag"):
            return [1]
        day_flag = []
        for i in self.params["day_flag"]:
            i_str = str(i)
            m = day_flag_pattern.match(i_str)
            if m is None:
                raise ValueError("day_flag参数%s中的参数项%s格式错误" % (
                    self.params["day_flag"], i_str))
            if i_str.find("-") == -1:
                day_flag.append(int(i_str))
            else:
                i_split = [int(j) for j in i_str.split("-")]
                min_i, max_i = min(i_split), max(i_split) + 1
                day_flag.extend(list(range(min_i, max_i)))
        # 去重
        day_flag = list(set(day_flag))
        return day_flag or [1]

    def _get_nc_train_data(self, start_dt, end_dt, out_col, is_cal=0):
        """取nc数据"""
        st, et = pd.to_datetime(start_dt), pd.to_datetime(end_dt)
        # et = et + timedelta(days=1)
        st, et = st.strftime("%Y%m%d"), et.strftime("%Y%m%d")
        read_nc = ReadNc2DTrain(
            wfid=self.wfid,
            source=self.params["nwp_source"],
            kw={
                'lon_index1' : self.params["lon_index1"],
                'lon_index2' : self.params["lon_index2"],
                'lat_index1' : self.params["lat_index1"],
                'lat_index2' : self.params["lat_index2"],
            },
            col_list=self.params["col_list"])

        day_flags = self._prase_day_flag()

        grid_data = read_nc.generate_DataFrame_base(
                st=st,
                et=et,
                out_col=out_col,
                check_result=self.params["check_result"],
                is_cal=is_cal,
                day_flag=day_flags if day_flags else [1]
        )

        if self.params.get("limit_type"):
            # 获取实测数据
            obs_data = self._get_obs_data(
                    start_dt=start_dt,
                    end_dt=end_dt,
                    columns=[self.params["limit_type"]])

            if not obs_data.empty and self.params["limit_type"] in obs_data.columns:
                grid_data = grid_data.merge(obs_data, left_index=True, right_on='dtime', how='left').set_index("dtime")
                grid_data[self.params["limit_type"]] = grid_data[self.params["limit_type"]].fillna(-1)
        return grid_data


    def _get_nc_predict_data(self, start_dt, end_dt):
        """取nc数据"""
        st, et = pd.to_datetime(start_dt), pd.to_datetime(end_dt)
        st, et = st.strftime("%Y%m%d"), et.strftime("%Y%m%d")
        read_nc = ReadNc2DPredict(
            wfid=self.wfid,
            source=self.params["nwp_source"],
            kw={
                'lon_index1' : self.params["lon_index1"],
                'lon_index2' : self.params["lon_index2"],
                'lat_index1' : self.params["lat_index1"],
                'lat_index2' : self.params["lat_index2"],
            },
            col_list=self.params["col_list"],
            nctype='nc_wfid',
            env='aws' if settings.USE_119_PGP and not settings.IS_AWS_BAK else 'local')
        return read_nc.generate_DataFrame_base_predict(
                st=st, et=et, mark=self.params.get("clock", "12"))

    def _get_nc_data(self, start_dt, end_dt, phase="train"):
        """取nc数据"""
        st, et = pd.to_datetime(start_dt), pd.to_datetime(end_dt)
        st, et = st.strftime("%Y%m%d"), et.strftime("%Y%m%d")
        read_nc = ReadNc2D(
            wfid=self.wfid,
            source=self.params["nwp_source"],
            kw={
                'lon_index1' : self.params["lon_index1"],
                'lon_index2' : self.params["lon_index2"],
                'lat_index1' : self.params["lat_index1"],
                'lat_index2' : self.params["lat_index2"],
            },
            col_list=self.params["col_list"])
        if phase == "train":
            return read_nc.generate_DataFrame_base(
                    st=st,
                    et=et,
                    out_col=self.params["out_col"],
                    check_result=self.params["check_result"])
        elif phase == 'predict':
            return read_nc.generate_DataFrame_base_predict(st=st, et=et)
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
        train_data = self._get_nc_train_data(train_start, train_end, self.params.get("out_col"))
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
                data = self._get_nc_train_data(
                        period["s"], period["e"], out_col)
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            windows = self.params["windows"]
            evaluate_start, evaluate_end = self._prase_date(windows)
            evaluate_data = self._get_nc_train_data(evaluate_start, evaluate_end, out_col)
        else:
            raise Exception("评估起止时间和评估窗口必存在一个参数")
        if evaluate_data.empty:
            raise Exception("所选日期不存在评估数据，请修改训练数日期")
        evaluate_data = self.check_and_modify_index(evaluate_data)
        if self.params.get("day_flag") and "day_flag" in evaluate_data.columns:
            day_flags = [self.params["day_flag"]] if not isinstance(self.params["day_flag"], list) else self.params["day_flag"]
            evaluate_data = evaluate_data[evaluate_data["day_flag"].isin(day_flags)]
        return evaluate_data

    def predict(self):
        """预测"""
        try:
            this_day = lambda x:(pd.to_datetime(x)-timedelta(days=1)).strftime("%Y-%m-%d")
            # next_day = lambda x:(pd.to_datetime(x)+timedelta(days=1)).strftime("%Y-%m-%d")
            if self.params.get("predict_start_dt") and self.params.get("predict_end_dt"):
                start_day = this_day(self.params["predict_start_dt"])
                end_day = this_day(self.params["predict_end_dt"])
                predict_df = self._get_nc_train_data(
                        start_day, end_day, out_col=self.params["out_col"], is_cal=1)
            elif self.params.get("predict_date"):
                pred_dt = this_day(self.params["predict_date"])
                predict_df = self._get_nc_train_data(
                        pred_dt, pred_dt, self.params["out_col"], is_cal=1)
            else:
                """
                ec取未来1天到未来9天；gfs取未来1天到未来14天，时间分辨率1h
                例：2022-09-02预测的话,EC是
                st=2022-09-03   et=2022-09-11
                2022-09-02预测的话,GFS是
                st=2022-09-03   et=2022-09-16
                注意：取数据多时在预测时会造成内存过大
                """
                source=self.params["nwp_source"]
                pred_start_dt = (
                        (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=1)
                        ).strftime("%Y-%m-%d")
                if source == 'GFS':
                    pred_end_dt = (
                            (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=14) # 最大14,只取7
                            ).strftime("%Y-%m-%d")
                else:
                    pred_end_dt = (
                            (datetime.utcnow()+timedelta(hours=8)) + timedelta(days=8) # 最大9,只取7
                            ).strftime("%Y-%m-%d")
                predict_df = self._get_nc_predict_data(pred_start_dt, pred_end_dt)
            if not predict_df.empty:
                predict_df = predict_df[[i for i in predict_df.columns if not str(i).startswith("r_")]]
            predict_df = predict_df.dropna()
            if not isinstance(predict_df, pd.DataFrame) or predict_df.empty:
                raise Exception("未取到预测使用的网格数据")
            if not predict_df.index.name:
                predict_df.index.name = 'dtime'
            return predict_df
        except Exception as e:
            raise e

