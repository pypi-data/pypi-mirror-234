
"""
根路径： /jtdata/products/data/
文件夹：
    JTLMOXVE: 收资数据csv文存储（供模型训练使用)
    JTC3WS8V: 历史gdfs抽点结果csv文件存储(供模型训练使用)
    JTE72HN5: 历史ec抽点结果csv文件存储（供模型训练使用)
    JT1A98G9: 实时ec
    JT6DE34S: 实时gdfs
"""
from functools import  reduce
import os
from math import ceil
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
stp = datetime.strptime
stf = datetime.strftime
DATE_F = '%Y-%m-%d'
import math
from dateutil.relativedelta import relativedelta

AVG_DAYS ={
    "cfs45": 0, "avg3d": 3, "avg5d": 5
}


#区域cfs45处理旬预测和月预测
# class Cfs45DataImportArea():
class Shan1XiAreaImport():
    __version__ = "v1.0.1"
    TEMPLATE = [
        {
            "key": "data_length",
            "name": "训练数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 10,
            "desc": "字段说明"
        },
        {
            "key": "wth_avg_type",
            "name": "数据平均天数类型",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "csf45",
            "source": ["cfs45", "avg3d", "avg5d"],
            "desc": "字段说明",
        },
        {
            "key": "batch_type",
            "name": "选择数据频次",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "By_1_hours",
            "source": ["By_1_hours", "By_6_hours", "By_1_day"],
            "desc": "字段说明",
        },
        {
            "key": "time_frequency",
            "name": "选择数据批次时间",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "10_20_30",
            "source": ["10_20_30", "5_15_25", "15"],
            "desc": "字段说明",
        },
        {
            "key": "data_source",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "select_multiple",
            "need": True,
            "value": "区域长期",
            "source": ["区域长期", "区域中期"],
            "desc": "字段说明",
        },
        {
            "key": "power_type",
            "name": "观测电量类型",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "风电",
            "source": ["风电", "光电", "负载"],
            "desc": "字段说明",
        },

    ]
    # ="
    params_rules = {}

    def __init__(self, **kw):
        # super().__init__(**kw)
        self.params = kw
        self.farm_info = kw.get("biz_info", {})
        self.data_path = ""
        self.datapath = "/mnt/d/use_data" # 本地测试使用
        # self.datapath = "/jtdata/products/data" # 线上的数据路径
        self.power_path = {
            "风电":"%s/JTLMOXVE/shan1xi/wind_power.csv",
            "光电":"%s/JTLMOXVE/%s/solar_power.csv",
            "负载":"%s/JTLMOXVE/%s/load_power.csv",
        }
        self.cfs45_path_predict = r""  # 要修改
        self.cfs45_path_train = r"/jtdata/products/data/JT1A98G9/"  # 要修改
        self.lon = self.farm_info.get("lon")
        self.lat = self.farm_info.get("lat")

    def cal_data_range(self, days, reserve=0, last_dt=None):
        """计算数据的开始时间和结束时间"""
        if last_dt:
            end_dt = last_dt
        else:
            end_dt = (datetime.utcnow() + timedelta(hours=8))
        if end_dt.hour != 23:
            end_dt = end_dt - timedelta(days=1)
        if reserve:
            train_end = end_dt - timedelta(days=int(reserve))
        else:
            train_end = end_dt
        train_start = train_end - timedelta(days=int(days) - 1)
        train_start = train_start.strftime(DATE_F)
        train_end = train_end.strftime(DATE_F)
        return train_start, train_end

    def interplocate_df(self, df):
        """线性插值15min"""
        not_inter_c = [i for i in df.columns if (str(i).startswith("wd") or str(i).startswith("WD"))]
        inter_c = list(set(df.columns.to_list()) - set(not_inter_c))
        not_inter_df = df[not_inter_c]
        inter_df = df[inter_c]
        inter_df = inter_df.sort_index()
        inter_df = inter_df.groupby(inter_df.index).last()
        inter_df = inter_df.resample("15min").interpolate()
        df_merge = pd.merge(inter_df, not_inter_df, how="left", left_index=True, right_index=True)
        df_merge.fillna(method='ffill', inplace=True)
        return df_merge

    def get_distance_wgs84(self, lon1, lat1, lon2, lat2):
        """
        #计算两个经纬度之间距离
        :param lon1: float 经度1
        :param lat1: float 纬度1
        :param lon2: float 经度2
        :param lat2: float 纬度2
        :return: 距离，单位为 米
        """
        lon1 = float(lon1)
        lat1 = float(lat1)
        lon2 = float(lon2)
        lat2 = float(lat2)
        earthR = 6378137.0
        pi180 = math.pi / 180
        arcLatA = lat1 * pi180
        arcLatB = lat2 * pi180
        x = (math.cos(arcLatA) * math.cos(arcLatB) * math.cos((lon1 - lon2) * pi180))
        y = math.sin(arcLatA) * math.sin(arcLatB)
        s = x + y
        if s > 1:
            s = 1
        if s < -1:
            s = -1
        alpha = math.acos(s)
        distance = alpha * earthR
        return distance

    def get_with_count(self, csv_name_list, fan_lon, fan_lat):
        # 抽取中心点经纬度
        import re
        min_distance = 0
        centre = None
        for csv_name in csv_name_list:
            pointId_list = re.findall(r"-?\d+\.\d+", csv_name)

            distance = self.get_distance_wgs84(pointId_list[0], fan_lat, pointId_list[-1], fan_lon)

            if min_distance == 0:
                centre = csv_name
                min_distance = distance
            if distance < min_distance:
                centre = csv_name
                min_distance = distance

        return centre

    def long_term_data(self, batch_list, batch_type, time_frequency):

        batch_list = sorted(batch_list)
        data_list = []
        data_con = pd.DataFrame([])
        for batch_path in batch_list:
            if os.path.exists(batch_path) == False:
                self.print(batch_path, ":不存在")
                continue
            batch_time = os.path.split(batch_path)[-1]
            if batch_time[-2:] == batch_type:
                cutting_time = (stp(batch_time[:6], "%Y%m") + relativedelta(months=+1)).strftime("%Y%m")  # 切割时间（年月）
                data = self.data_avg_days(batch_path, days_avg=0, time_frequency=time_frequency,
                                          is_centre_pointid=True)
                data = data[data["time"].apply(lambda x: str(x)[:6]) == cutting_time]
                data_list.append(data)
        data_con = pd.concat(data_list)

        return data_con

    def medium_term_data(self, batch_list, days_avg, batch_type, time_frequency):

        batch_type_list = list(batch_type.split("_"))
        if batch_type == "all":
            batch_type_list = []
        batch_list = sorted(batch_list)
        data_list = []
        data_con = pd.DataFrame([])
        for batch_path in batch_list:
            batch_time = os.path.split(batch_path)[-1]

            if batch_time[-2:] not in batch_type_list:
                continue
            if batch_time[-2:] > "20":
                cutting_time_start = (
                            datetime.datetime.strptime(batch_time[:6], "%Y%m") + relativedelta(months=+1)).strftime(
                    "%Y%m%d%H%M")
                cutting_time_end = (
                            datetime.datetime.strptime(cutting_time_start[:6], "%Y%m") + timedelta(days=10)).strftime(
                    "%Y%m%d%H%M")
            else:
                cutting_time_start = (datetime.datetime.strptime(batch_time[:8], "%Y%m%d") + datetime.timedelta(
                    days=10)).strftime("%Y%m%d%H%M")
                if batch_time[-2:] > "10" and batch_time[-2:] < "20":
                    cutting_time_end = (datetime.datetime.strptime(cutting_time_start[:6], "%Y%m") + timedelta(
                        days=10)).strftime("%Y%m%d%H%M")
                else:
                    cutting_time_end = (datetime.datetime.strptime(cutting_time_start[:6], "%Y%m") + timedelta(
                        days=10)).strftime("%Y%m%d%H%M")

            data = self.data_avg_days(batch_path, days_avg=days_avg, time_frequency=time_frequency,
                                      is_centre_pointid=False)
            data = data[(data["time"].apply(lambda x: str(x)[:6]) >= cutting_time_start) & (
                        data["time"].apply(lambda x: str(x)[:6]) < cutting_time_end)]
            data_list.append(data)
        data_con = pd.concat(data_list).drop_duplicates(["point_id", "time"], keep="last")
        return data_con

    def pointIdTransition(self, x):
        import re
        compileX = re.findall(r"-?\d+\.\d+", x)
        return '{:.3f}:{:.3f}'.format(float(compileX[0]), float(compileX[-1]))


    def data_avg_days(self, batch_path, days_avg, time_frequency, is_centre_pointid=True):
        """

        :param batch_path: 数据批次路径
        :param days_avg: 平均数据天数
        :param time_frequency: 数据为逐日的还是逐六小时的
        :param is_centre_pointid: 是否是单场数据
        :return:
        """
        batch_split_list = list(os.path.split(batch_path))
        batch = batch_split_list[-1]
        data_list = []
        for days in range(days_avg):
            batch_time_day = (stp(batch, "%Y%m%d") + timedelta(days=days)).strftime("%Y%m%d")
            current_batch_list = batch_split_list[:-1] + [batch_time_day]
            batch_path_day = reduce(lambda x, y: os.path.join(x, y), current_batch_list)
            data = pd.DataFrame([])
            if is_centre_pointid == True:
                centre_pointid = None
                # 筛选出单场站中心经纬度
                if centre_pointid == None:
                    csv_list = [i for i in os.listdir(batch_path_day)]
                    centre_pointid = self.get_with_count(csv_list, self.lon, self.lat)
                data = pd.read_csv(os.path.join(batch_path, centre_pointid), dtype={"time": str})
                data["point_id"] = self.pointIdTransition(centre_pointid)

            else:
                for csv_name in os.listdir(batch_path):
                    data = pd.read_csv(os.path.join(batch_path, csv_name), dtype={"time": str})

                    if time_frequency == "By_1_hours":
                        data["time"] = data["time"].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                        data.set_index("time", inplace=True)
                        data = data.resample("1H").interpolate().reset_index()
                        data["time"] = data["time"].apply(lambda x: stf(x, "%Y%m%d%H%M"))

                    data["point_id"] = self.pointIdTransition(csv_name)
            data_list.append(data)
        data_con = pd.concat(data_list)
        if time_frequency == "By_1_hours" or time_frequency == "By_6_hours":

            data_con = data_con.groupby(["point_id", "time"]).mean().reset_index()
        elif time_frequency == "By_1_day":
            data_con = data_con.groupby(
                ["point_id", data_con["time"].apply(lambda x: str(x)[:8] + "0000")]).mean().reset_index()

        data_con.rename(columns={"ws": "ws_10m"}, inplace=True)

        return data_con

    def get_power(self, time_frequency, start_time=None, end_time=None, ):
        """取功率数据"""
        filepath = self.power_path[self.params["power_type"]]
        if not os.path.isfile(filepath):
            raise Exception("功率收资数据文件不存在")
        data_power = pd.DataFrame()
        try:
            data_power = pd.read_csv(filepath, dtype={"time": str})
            data_power.columns = ["time", "power"]
        except Exception as e:
            raise Exception(f"在读取功率收资数据时报错\n{e}")
        if data_power.empty:
            raise Exception(f"{filepath}, 功率收资数据文件内数据为空")

        # data_strat, data_end = str(data_power["time"].min()), str(data_power["time"].max())
        # data_strat = data_strat[:8] + "0015"
        # time_index = pd.DataFrame(
        #     {
        #         "time": [i.strftime("%Y%m%d%H%M") for i in
        #                  pd.date_range(stp(data_strat, "%Y%m%d%H%M"), stp(data_end, "%Y%m%d%H%M"),
        #                                freq="15min")]
        #     }
        # )

        # data_power = pd.merge(time_index, data_power, on="time", how="left")

        # data_power_dirt = {"time": [], "power": []}
        # for i in range(0, len(data_power), 4):
        #     data = data_power.iloc[i:i + 4, :]

        #     data_power_dirt["time"].append(data["time"].iloc[-1])
        #     data_power_dirt["power"].append(data["power"].mean())

        # data_power = pd.DataFrame(data_power_dirt)
        # data_power_dirt_6H = {"time": [], "power": []}
        # if time_frequency == "By_6_hours":
        #     data_strat, data_end = str(data_power["time"].min()), str(data_power["time"].max())
        #     data_strat = data_strat[:8] + "0300"
        #     time_index = pd.DataFrame(
        #         {
        #             "time": [i.strftime("%Y%m%d%H%M") for i in
        #                      pd.date_range(stp(data_strat, "%Y%m%d%H%M"), stp(data_end, "%Y%m%d%H%M"),
        #                                    freq="1H")]
        #         }
        #     )
        #     data_power = pd.merge(time_index, data_power, on="time", how="left")
        #     for i in range(0, len(data_power), 6):
        #         data = data_power.iloc[i:i + 6, :]

        #         data_power_dirt_6H["time"].append(data["time"].iloc[-1])
        #         data_power_dirt_6H["power"].append(data["power"].sum())

        #     data_power = pd.DataFrame(data_power_dirt_6H)
        # data_power["time"] = pd.to_datetime(data_power["time"])

        # data_power = data_power.set_index("time").sort_index()

        if start_time and end_time:
            start_dt = pd.to_datetime(start_time)
            end_dt = pd.to_datetime(end_time) + timedelta(days=1)
            data_power = data_power[(data_power.index > start_dt) & (data_power.index <= end_dt)]
        return data_power

    def cfs45_predict(self, days_avg, time_frequency):
        """
        预测cfs45数据数据
        """
        file_tail_str = "%s.rb" % self.farm_info.get("biz_id")  # 风场或者区域farm_id
        data_con = pd.DataFrame([])
        now_time = datetime.utcnow()
        now_time_strf = now_time.strftime("%Y%m%d") + "0000"
        data_batch_list = []
        for day in range(days_avg):
            now_time = (now_time - timedelta(days=day)).strftime("%Y%m%d")
            if not os.path.exists(os.path.join(self.cfs45_path_predict, now_time)):
                raise ValueError("当前时间的%S改批次数据未到达!" % now_time)

            for rb_name in os.listdir(os.path.join(self.cfs45_path_predict, now_time)):
                if rb_name.split("-")[-1] == file_tail_str:  # 改动
                    data = pd.read_csv(os.path.join(self.cfs45_path_predict, now_time, rb_name), header=1,
                                       dtype={"time": str})  # rb文件读取
                    data = data.iloc[:-1, 1:]
                    data = data[data["time"] >= now_time_strf]
                    data_list = []

                    if time_frequency == "By_1_hours":
                        data["time"] = data["time"].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                        for pid, data_gr in data.groupby(["point_id"]):
                            data_gr.set_index("time", inplace=True)
                            data = data.resample("1H").interpolate().reset_index()
                            data["point_id"] = pid
                            data_list.append(data)

                        data = pd.concat(data_list)

                    data_batch_list.append(data)
                    break
            else:
                raise ValueError("当前批次rb数据数据没有到达!")
        data_con = pd.concat(data_batch_list)
        data_con = data_con.groupby(["point_id", "time"]).mean().reset_index()

        data_con['time'] = pd.to_datetime(data_con['time'])

        data_con.set_index('time', inplace=True)
        return data_con

    def flat_cfs45_feature(self, df):
        """
        cfs45点位展平特征
        """

        df["point_id"] = df["point_id"].str.replace(":", "_").str.replace(".", "_")
        df = df.pivot_table(index=df.index, columns="point_id").dropna()
        df.columns = ['%s_%s' % (c[0], c[1]) for c in df.columns]
        return df

    def func_add_time_features(self, df, time_col="time", i_astype=int):
        """
        增加时间特征
        """
        if time_col in df.columns:
            df = df.set_index(time_col)
        df['month'] = df.index.month.astype(i_astype)
        df['day'] = df.index.day.astype(i_astype)
        df['dayofyear'] = df.index.dayofyear.astype(i_astype)
        df['weekofyear'] = df.index.isocalendar().week
        df['weekofyear'] = df['weekofyear'].astype(i_astype)
        df['dayofweek'] = df.index.dayofweek.astype(i_astype)  # Monday=0, Sunday=6
        df['quarter'] = df.index.quarter.astype(i_astype)
        df['season'] = df['dayofyear'].apply(lambda x: np.cos(2 * x * np.pi / 366))
        if time_col in df.columns:
            df = df.reset_index()
        return df

    def get_train_dt(self, last_dt):
        """获取训练所使用的时间"""
        reserve = int(self.params.get('reserve_length', 0))
        data_length = int(self.params.get('data_length', 10))
        train_start_dt, validate_end_dt = self.cal_data_range(
            data_length, reserve, last_dt=last_dt)
        # 验证数据时长
        # proportion=float(self.params.get("train_validation_proportion", 0.1))
        # day_propor = ceil(data_length * proportion)
        # validate_start_dt = stf(stp(validate_end_dt, DATE_F)-timedelta(days=day_propor-1), DATE_F)
        # train_end_dt = stf(stp(validate_start_dt, DATE_F)-timedelta(days=1), DATE_F)
        return train_start_dt, validate_end_dt

    def run(self):

        data_alls = pd.DataFrame()

        batch_type = self.params.get("batch_type", [])
        data_source = self.params.get("data_source", [])
        wth_avg_type = self.params.get("wth_avg_type", [])
        time_frequency = self.params.get("time_frequency", [])

        # 省功率数据
        power_data = self.get_power(time_frequency=time_frequency, start_time=None, end_time=None)
        data_alls = data_alls.merge(power_data, left_index=True, right_index=True)

        train_data = pd.DataFrame([])

        last_dt = power_data.index[-1]
        train_start_dt, train_end_dt = self.get_train_dt(last_dt)
        batch_list = [os.path.join(self.cfs45_path_predict, dt) for dt in
                      pd.date_range(train_start_dt, train_end_dt, freq="1D")]
        data = pd.DataFrame([])
        if data_source == "月预测":
            data = self.long_term_data(batch_list=batch_list, batch_type=batch_type, time_frequency=time_frequency)
        if data_source == "旬预测":
            day = AVG_DAYS.get(wth_avg_type)
            data = self.medium_term_data(batch_list, days_avg=day, batch_type=batch_type, time_frequency=time_frequency)
        train_data = self.flat_cfs45_feature(data)
        train_data.columns = ["CFS45_%s" % i for i in train_data.columns]
        train_data["cfs45_data_type"] = "train"

        data_alls = data_alls.merge(train_data, left_index=True, right_index=True)

        data_alls = self.func_add_time_features(data_alls)

        data_alls.sort_index(inplace=True)
        return data_alls

    def predict(self):
        """
        预测气象数据主函数
        """
        data = pd.DataFrame([])
        last_bt = max(os.listdir(self.cfs45_path_predict))
        batch_type = self.params.get("batch_type", [])
        # data_source = self.params.get("data_source", [])
        wth_avg_type = self.params.get("wth_avg_type", [])
        avg_days = AVG_DAYS.get(wth_avg_type)

        time_frequency = self.params.get("time_frequency", [])
        data = pd.DataFrame()
        data = self.cfs45_predict(days_avg=avg_days, time_frequency=time_frequency)
        data = self.func_add_time_features(data)
        return data

        # data_source = self.params.get("data_source", [])
        # if "EC" in data_source:
        #     EC_data = self.EC_predict()
        #     EC_data = self.flat_EC_feature(EC_data)
        #     EC_data.columns = [(("EC_%s" % i) if i!="time" else i) for i in EC_data.columns]
        #     data = EC_data if data.empty else data.merge(EC_data, on="time")
        # if "GDFS" in data_source:
        #     GDFS_data = self.GDFS_predict()
        #     GDFS_data=self.flat_GDFS_feature(GDFS_data)
        #     GDFS_data.columns = [(("GDFS_%s" % i) if i!="time" else i) for i in GDFS_data.columns]
        #     data = GDFS_data if data.empty else data.merge(GDFS_data, on="time")
        # data = self.interplocate_df(data.resample("1H").first())
        # data = self.func_add_time_features(data)
        # return data
