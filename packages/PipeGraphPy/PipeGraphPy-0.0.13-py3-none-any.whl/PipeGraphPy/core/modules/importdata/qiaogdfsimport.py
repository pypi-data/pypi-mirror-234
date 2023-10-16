# coding: utf8

"""
根路径： /jtdata/products/data/
文件夹：
    JTLMOXVE: 收资数据csv文存储（供模型训练使用)
    JTC3WS8V: 历史gdfs抽点结果csv文件存储(供模型训练使用)
    JTE72HN5: 历史ec抽点结果csv文件存储（供模型训练使用)
    JT1A98G9: 实时ec
    JT6DE34S: 实时gdfs
"""

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

GDFS_COLUMNS = ["point_id", "tcc", "hcc", "mcc", "lcc", "pre_15m", "snow_15m", "sr", "ws_10", "ws_30", "ws_50", "ws_70", "ws_90", "ws_120", "ws_150", "ws_200", "wd_10", "wd_30", "wd_50", "wd_70", "wd_90", "wd_120", "wd_150", "wd_200", "tem_10", "tem_30", "tem_50", "tem_70", "tem_90", "tem_120", "tem_150", "tem_200", "rhu_10", "rhu_30", "rhu_50", "rhu_70", "rhu_90", "rhu_120", "rhu_150", "rhu_200", "prs_10", "prs_30", "prs_50", "prs_70", "prs_90", "prs_120", "prs_150", "prs_200"]

class CLOCK:
    ZERO = "00"
    TWELVE = "12"

class QiaoGDFSImport():
    __version__="v1.17"
    TEMPLATE = [
        {   "key":"data_length",
            "name":"训练数据长度(天)",
            "type":"int",
            "plugin":"input",
            "need":True,
            "value":10,
            "desc":"字段说明"
        },
        {
             "key": "train_validation_proportion",
             "name": "训练集与验证集占比",
             "type": "string",
             "plugin": "input",
             "need": True,
             "value": "0.2",
             "desc": "字段说明"
        },
        {
            "key": "reserve_length",
            "name": "保留数据长度(天)",
            "type": "int",
            "plugin": "input",
            "need": False,
            "value": 10,
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
            "key": "wth_extract_type",
            "name": "气象数据提取方式" ,
            "type":"string",
            "plugin": "select",
            "need": True,
            "value": "滚动覆盖",
            "source": ["滚动覆盖", "业务版-00", "业务版-15"],
            "desc": "字段说明",
        },
        {
            "key": "data_source",
            "name": "预测数据气象源" ,
            "type":"list",
            "plugin": "select_multiple",
            "need": True,
            "value": ["EC", "GDFS"],
            "source": ["EC", "GDFS"],
            "desc": "字段说明",
        },
    ]
    params_rules = {}

    def __init__(self,**kw):
        # super().__init__(**kw)
        self.params = kw
        self.farm_info = kw.get("biz_info", {})
        self.datapath = "/mnt/d/use_data" # 本地测试使用
        # self.datapath = "/jtdata/products/data" # 线上的数据路径
        self.gdfs_path_history="/JTC3WS8V/GDFS/merge/%s/" % (self.datapath, self.farm_info.get("biz_id"))
        self.ec_path_history="%s/JTE72HN5/EC/merge/%s/" % (self.datapath, self.farm_info.get("biz_id"))
        self.gdfs_path_Realtime="%s/JT6DE34S/" % self.datapath
        self.ec_path_Realtime = "%s/JT1A98G9/" % self.datapath
        self.ws_path=r"%s/JTLMOXVE/%s/ws.csv" % (self.datapath, self.farm_info.get("biz_id"))
        self.sr_path=r"%s/JTLMOXVE/%s/sr.csv" % (self.datapath, self.farm_info.get("biz_id"))
        self.power_path = r"%s/JTLMOXVE/%s/power.csv" % (self.datapath, self.farm_info.get("biz_id"))
        self.farm_type = self.farm_info.get("ext_type_1")

    def cal_data_range(self,  days, reserve=0, last_dt=None):
        """计算数据的开始时间和结束时间"""
        if last_dt:
            end_dt = last_dt
        else:
            end_dt = (datetime.utcnow()+timedelta(hours=8))
        if end_dt.hour != 23:
            end_dt = end_dt - timedelta(days=1)
        if reserve:
            train_end = end_dt - timedelta(days=int(reserve))
        else:
            train_end = end_dt
        train_start = train_end - timedelta(days=int(days)-1)
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

    def read_GDFS_train_csv_data(self, folder_list, clock):
        "读取csv的训练数据"
        clock_folder_list = [i+clock for i in folder_list]
        train_df_list = []
        for clock_folder in clock_folder_list:
            if os.path.isdir(clock_folder):
                for csv_name in os.listdir(clock_folder):
                    csv_filepath = os.path.join(clock_folder, csv_name)
                    df_data=pd.read_csv(csv_filepath , dtype={"time":str})
                    df_data['time'] = df_data['time'].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                    df_data = df_data.set_index("time")
                    df_merge = self.interplocate_df(df_data)
                    date = os.path.basename(clock_folder)[:8]
                    if clock == CLOCK.ZERO:
                        start_time = stp(date + "20", "%Y%m%d%H")
                        end_time = stp(date + "08", "%Y%m%d%H") + timedelta(days=1)
                    elif clock == CLOCK.TWELVE:
                        start_time = stp(date + "08", "%Y%m%d%H") + timedelta(days=1)
                        end_time = stp(date + "20", "%Y%m%d%H") + timedelta(days=1)
                    df_merge = df_merge[(df_merge.index>=start_time)&(df_merge.index<end_time)]
                    df_merge["point_id"] = csv_name.split(".c")[0].replace('_', ":")
                    # df_merge["csv_filepath"] = csv_filepath
                    train_df_list.append(df_merge)
        data_all= pd.concat(train_df_list) if train_df_list else pd.DataFrame()
        # data_all["batch_clock"] = clock
        return data_all

    def read_GDFS_validate_csv_data(self, folder_list, clock=CLOCK.TWELVE):
        "读取csv的训练数据"
        clock_folder_list = [i+clock for i in folder_list]
        train_df_list = []
        for clock_folder in clock_folder_list:
            if os.path.isdir(clock_folder):
                for csv_name in os.listdir(clock_folder):
                    csv_filepath = os.path.join(clock_folder, csv_name)
                    df_data=pd.read_csv(csv_filepath , dtype={"time":str})
                    df_data['time'] = df_data['time'].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                    df_data = df_data.set_index("time")
                    df_merge = self.interplocate_df(df_data)
                    date = os.path.basename(clock_folder)[:8]
                    start_time = stp(date + "00", "%Y%m%d%H") + timedelta(days=2)
                    end_time = stp(date + "00", "%Y%m%d%H") + timedelta(days=3)
                    if str(self.params.get("wth_extract_type")).endswith("00"):
                        df_merge = df_merge[(df_merge.index>=start_time)&(df_merge.index<end_time)]
                    else:
                        df_merge = df_merge[(df_merge.index>start_time)&(df_merge.index<=end_time)]
                    df_merge["point_id"] = csv_name.split(".c")[0].replace('_', ":")
                    # df_merge["csv_filepath"] = csv_filepath
                    train_df_list.append(df_merge)
        data_all= pd.concat(train_df_list) if train_df_list else pd.DataFrame()
        # data_all["batch_clock"] = clock
        return data_all

    def get_GDFS_train_data(self, start_time, end_time):
        """取GDFS训练数据"""
        datas_start_dt = stf(stp(start_time, DATE_F)-timedelta(days=2), DATE_F)
        datas_end_dt = stf(stp(end_time, DATE_F)+timedelta(days=1), DATE_F)
        days_list = pd.date_range(datas_start_dt,datas_end_dt, freq="1D")
        batch_list = [os.path.join(self.gdfs_path_history,i.strftime("%Y%m%d")) for i in days_list]
        if self.params.get("wth_extract_type") != "滚动覆盖":
            train_12 = self.read_GDFS_validate_csv_data(batch_list, CLOCK.TWELVE)
            data_all= train_12.sort_index()
        else:
            train_00 = self.read_GDFS_train_csv_data(batch_list, CLOCK.ZERO)
            train_12 = self.read_GDFS_train_csv_data(batch_list, CLOCK.TWELVE)
            data_all= pd.concat([train_00, train_12]).sort_index()
        start_dt = pd.to_datetime(start_time)
        end_dt = pd.to_datetime(end_time) + timedelta(days=1)
        if str(self.params.get("wth_extract_type")).endswith("00"):
            data_all =  data_all[(data_all.index>=start_dt)&(data_all.index<end_dt)]
        else:
            data_all =  data_all[(data_all.index>start_dt)&(data_all.index<=end_dt)]
        return data_all

    def get_GDFS_validate_data(self, start_time, end_time):
        """取GDFS验证数据"""
        datas_start_dt = stf(stp(start_time, DATE_F)-timedelta(days=2), DATE_F)
        datas_end_dt = end_time
        days_list = pd.date_range(datas_start_dt,datas_end_dt, freq="1D")
        batch_list = [os.path.join(self.gdfs_path_history,i.strftime("%Y%m%d")) for i in days_list]
        train_12 = self.read_GDFS_validate_csv_data(batch_list, CLOCK.TWELVE)
        data_all= train_12.sort_index()
        start_time= stp(str(start_time),DATE_F)
        end_time = stp(str(end_time),DATE_F) + timedelta(days=1)
        if str(self.params.get("wth_extract_type")).endswith("00"):
            data_all =  data_all[(data_all.index>=start_time)&(data_all.index<end_time)]
        else:
            data_all =  data_all[(data_all.index>start_time)&(data_all.index<=end_time)]
        return data_all

    def read_EC_train_csv_data(self, folder_list, clock):
        "读取ec的csv的训练数据"
        clock_folder_list = [i+clock for i in folder_list]
        train_df_list = []
        for clock_folder in clock_folder_list:
            if os.path.isdir(clock_folder):
                for csv_name in os.listdir(clock_folder):
                    csv_filepath = os.path.join(clock_folder, csv_name)
                    df_data=pd.read_csv(csv_filepath , dtype={"time":str})
                    df_data['time'] = df_data['time'].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                    df_data = df_data.set_index("time")
                    df_merge = self.interplocate_df(df_data)
                    date = os.path.basename(clock_folder)[:8]
                    if clock == CLOCK.ZERO:
                        start_time = stp(date + "08", "%Y%m%d%H")
                        end_time = stp(date + "20", "%Y%m%d%H")
                    elif clock == CLOCK.TWELVE:
                        start_time = stp(date + "20", "%Y%m%d%H")
                        end_time = stp(date + "08", "%Y%m%d%H") + timedelta(days=1)
                    df_merge = df_merge[(df_merge.index>=start_time)&(df_merge.index<end_time)]
                    df_merge["point_id"] = csv_name.split(".c")[0].replace('_', ":")
                    # df_merge["csv_filepath"] = csv_filepath
                    train_df_list.append(df_merge)
        data_all= pd.concat(train_df_list) if train_df_list else pd.DataFrame()
        # data_all["batch_clock"] = clock
        return data_all

    def read_EC_validate_csv_data(self, folder_list, clock=CLOCK.TWELVE):
        "读取ec的训练数据"
        clock_folder_list = [i+clock for i in folder_list]
        train_df_list = []
        for clock_folder in clock_folder_list:
            if os.path.isdir(clock_folder):
                for csv_name in os.listdir(clock_folder):
                    csv_filepath = os.path.join(clock_folder, csv_name)
                    df_data=pd.read_csv(csv_filepath , dtype={"time":str})
                    df_data['time'] = df_data['time'].apply(lambda x: stp(str(x), "%Y%m%d%H%M"))
                    df_data = df_data.set_index("time")
                    df_merge = self.interplocate_df(df_data)
                    date = os.path.basename(clock_folder)[:8]
                    start_time = stp(date + "00", "%Y%m%d%H") + timedelta(days=2)
                    end_time = stp(date + "00", "%Y%m%d%H") + timedelta(days=3)
                    if str(self.params.get("wth_extract_type")).endswith("00"):
                        df_merge = df_merge[(df_merge.index>=start_time)&(df_merge.index<end_time)]
                    else:
                        df_merge = df_merge[(df_merge.index>start_time)&(df_merge.index<=end_time)]
                    df_merge["point_id"] = csv_name.split(".c")[0].replace('_', ":")
                    # df_merge["csv_filepath"] = csv_filepath
                    train_df_list.append(df_merge)
        data_all= pd.concat(train_df_list) if train_df_list else pd.DataFrame()
        # data_all["batch_clock"] = clock
        return data_all

    def get_EC_train_data(self, start_time, end_time):
        """取ED训练数据"""
        datas_start_dt = stf(stp(start_time, DATE_F)-timedelta(days=3), DATE_F)
        datas_end_dt = end_time
        days_list = pd.date_range(datas_start_dt,datas_end_dt, freq="1D")
        batch_list = [os.path.join(self.ec_path_history,i.strftime("%Y%m%d")) for i in days_list]
        if self.params.get("wth_extract_type") != "滚动覆盖":
            train_12 = self.read_EC_validate_csv_data(batch_list, CLOCK.TWELVE)
            data_all= train_12.sort_index()
        else:
            train_00 = self.read_EC_train_csv_data(batch_list, CLOCK.ZERO)
            train_12 = self.read_EC_train_csv_data(batch_list, CLOCK.TWELVE)
            data_all= pd.concat([train_00, train_12]).sort_index()

        # 改列名
        if not data_all.empty:
            change_columns = {
                "10_metre_u_wind_component_surface":"u_wind_component_surface_10_metre",
                "10_metre_v_wind_component_surface": "v_wind_component_surface_10_metre",
                "2_metre_temperature_surface": "temperature_surface_2_metre",
                "2_metre_dewpoint_temperature_surface": "dewpoint_temperature_surface_2_metre",
                "100_metre_u_wind_component_surface": "u_wind_component_surface_100_metre",
                "100_metre_v_wind_component_surface": "v_wind_component_surface_100_metre"
            }
            data_all = data_all.rename(columns=change_columns)

        start_dt = pd.to_datetime(start_time)
        end_dt = pd.to_datetime(end_time) + timedelta(days=1)
        if str(self.params.get("wth_extract_type")).endswith("00"):
            data_all =  data_all[(data_all.index>=start_dt)&(data_all.index<end_dt)]
        else:
            data_all =  data_all[(data_all.index>start_dt)&(data_all.index<=end_dt)]
        return data_all

    def get_EC_validate_data(self, start_time, end_time):
        """取EC验证数据"""
        datas_start_dt = stf(stp(start_time, DATE_F)-timedelta(days=3), DATE_F)
        datas_end_dt = end_time
        days_list = pd.date_range(datas_start_dt,datas_end_dt, freq="1D")
        batch_list = [os.path.join(self.ec_path_history,i.strftime("%Y%m%d")) for i in days_list]
        train_12 = self.read_EC_validate_csv_data(batch_list)
        data_all= train_12.sort_index()
        start_time= stp(str(start_time),DATE_F)
        end_time = stp(str(end_time),DATE_F) + timedelta(days=1)
        if str(self.params.get("wth_extract_type")).endswith("00"):
            data_all =  data_all[(data_all.index>=start_time)&(data_all.index<end_time)]
        else:
            data_all =  data_all[(data_all.index>start_time)&(data_all.index<=end_time)]
        return data_all


    def get_sr(self, start_time=None, end_time=None):
        """取实测辐照度数据"""
        if not os.path.isfile(self.sr_path):
            raise Exception("实测辐照度收资数据文件不存在")
        data_sr = pd.DataFrame()
        try:
            data_sr=pd.read_csv(self.sr_path ,dtype={"time":str})
        except Exception as e:
            raise Exception(f"在读取实测辐照度收资数据时报错\n{e}")
        if data_sr.empty:
            raise Exception(f"{self.sr_path}, 实测辐照度收资数据文件内数据为空")
        data_sr["time"] = pd.to_datetime(data_sr["time"])
        data_sr = data_sr.set_index("time").sort_index()
        if start_time and end_time:
            start_dt = pd.to_datetime(start_time)
            end_dt = pd.to_datetime(end_time) + timedelta(days=1)

            if str(self.params.get("wth_extract_type")).endswith("00"):
                data_sr =  data_sr[(data_sr.index>=start_dt)&(data_sr.index<end_dt)]
            else:
                data_sr =  data_sr[(data_sr.index>start_dt)&(data_sr.index<=end_dt)]
        return data_sr


    def get_ws(self, start_time=None, end_time=None):
        """取实测风速数据"""
        if not os.path.isfile(self.ws_path):
            raise Exception("实测风速收资数据文件不存在")
        data_ws = pd.DataFrame()
        try:
            data_ws=pd.read_csv(self.ws_path ,dtype={"time":str})
        except Exception as e:
            raise Exception(f"在读取实测风速收资数据时报错\n{e}")
        if data_ws.empty:
            raise Exception(f"{self.ws_path}, 实测风速收资数据文件内数据为空")
        data_ws["time"] = pd.to_datetime(data_ws["time"])
        data_ws = data_ws.set_index("time").sort_index()
        if start_time and end_time:
            start_dt = pd.to_datetime(start_time)
            end_dt = pd.to_datetime(end_time) + timedelta(days=1)
            if str(self.params.get("wth_extract_type")).endswith("00"):
                data_ws =  data_ws[(data_ws.index>=start_dt)&(data_ws.index<end_dt)]
            else:
                data_ws =  data_ws[(data_ws.index>start_dt)&(data_ws.index<=end_dt)]
        return data_ws

    def get_power(self, start_time=None, end_time=None):
        """取功率数据"""
        if not os.path.isfile(self.power_path):
            raise Exception("功率收资数据文件不存在")
        data_power = pd.DataFrame()
        try:
            data_power=pd.read_csv(self.power_path ,dtype={"time":str})
        except Exception as e:
            raise Exception(f"在读取功率收资数据时报错\n{e}")
        if data_power.empty:
            raise Exception(f"{self.power_path}, 功率收资数据文件内数据为空")
        data_power["time"] = pd.to_datetime(data_power["time"])
        data_power = data_power.set_index("time").sort_index()
        if start_time and end_time:
            start_dt = pd.to_datetime(start_time)
            end_dt = pd.to_datetime(end_time) + timedelta(days=1)
            if str(self.params.get("wth_extract_type")).endswith("00"):
                data_power =  data_power[(data_power.index>=start_dt)&(data_power.index<end_dt)]
            else:
                data_power =  data_power[(data_power.index>start_dt)&(data_power.index<=end_dt)]
        return data_power

    def get_power_wsr(self, start_time=None, end_time=None):
        """取收资数据"""
        assert self.farm_type in ["W", "S"], "没有设置电场类型"
        data_power = self.get_power(start_time, end_time)
        data_wsr = self.get_ws(start_time, end_time) if self.farm_type == "W" else self.get_sr(start_time, end_time)
        data_power_wsr  = pd.merge(data_power, data_wsr, left_index=True, right_index=True)
        return  data_power_wsr

    def GDFS_predict(self):
        """
        预测gdfs数据处理
        """
        file_tail_str = "%s.rb" % self.farm_info.get("biz_id")
        data =pd.DataFrame([])
        now_time= (datetime.utcnow()+timedelta(hours=8)).strftime("%Y%m%d")
        if not os.path.exists(os.path.join(self.gdfs_path_Realtime,now_time)):
            raise ValueError("数据未到达!")
        for rb_name in os.listdir( os.path.join(self.gdfs_path_Realtime,now_time) ):
            if rb_name.split("-")[1][8:10] == "08" and rb_name.split("-")[-1] == file_tail_str:
                data = pd.read_csv(
                        os.path.join(self.gdfs_path_Realtime, now_time, rb_name),
                        header=1,
                        dtype={"time":str}
                )   # rb文件读取
                data = data.iloc[:-1,1:]
                break
        else:
            raise ValueError("数据没有到达!")
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        return data

    def EC_predict(self):
        """
        预测EC数据数据
        """
        file_tail_str = "%s.rb" % self.farm_info.get("biz_id")
        data =pd.DataFrame([])
        now_time= ((datetime.utcnow()+timedelta(hours=8)) - timedelta(days=1) ).strftime("%Y%m%d")  # 获取上一天20批次数据
        if not os.path.exists(os.path.join(self.ec_path_Realtime,now_time)):
            raise ValueError("数据未到达!")
        for rb_name in os.listdir( os.path.join(self.ec_path_Realtime,now_time)):
            if rb_name.split("-")[1][8:10] == "20" and rb_name.split("-")[-1] == file_tail_str:
                data = pd.read_csv(
                        os.path.join( self.ec_path_Realtime, now_time, rb_name),
                        header=1 ,
                        dtype={"time":str})   # rb文件读取
                data = data.iloc[:-1,1:]
                break
        else:
            raise ValueError("数据没有到达!")
        data['time'] = pd.to_datetime(data['time'])
        data.set_index('time', inplace=True)
        return data

    def flat_GDFS_feature(self, df):
        """
        GDFS点位展平特征
        """
        df = df.loc[:,GDFS_COLUMNS]
        df["point_id"] = df["point_id"].str.replace(":", "_").str.replace(".", "_")
        df = df.pivot_table(index=df.index, columns="point_id").dropna()
        df.columns = ['%s_%s' % (c[0], c[1]) for c in df.columns]
        return df

    def flat_EC_feature(self, df):
        """
        EC点位展平特征
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
        proportion=float(self.params.get("train_validation_proportion", 0.1))
        day_propor = ceil(data_length * proportion)
        validate_start_dt = stf(stp(validate_end_dt, DATE_F)-timedelta(days=day_propor-1), DATE_F)
        train_end_dt = stf(stp(validate_start_dt, DATE_F)-timedelta(days=1), DATE_F)
        return train_start_dt, train_end_dt, validate_start_dt, validate_end_dt

    def get_train_dt_by_start_end(self, start_dt, end_dt):
        """通过开始时间和结束时间区分训练和测试"""
        try:
            sd = stp(start_dt, DATE_F)
            ed = stp(end_dt, DATE_F)
            if sd >= ed:
                raise Exception("时间范围选择不正确")
        except Exception:
            raise Exception("时间格式不正确，必须为:YYYY-mm-dd")
        train_start_dt, validate_end_dt = sd.strftime(DATE_F), ed.strftime(DATE_F)
        data_length = (ed - sd).days
        # 验证数据时长
        proportion=float(self.params.get("train_validation_proportion", 0.1))
        day_propor = ceil(data_length * proportion)
        validate_start_dt = stf(stp(validate_end_dt, DATE_F)-timedelta(days=day_propor-1), DATE_F)
        train_end_dt = stf(stp(validate_start_dt, DATE_F)-timedelta(days=1), DATE_F)
        return train_start_dt, train_end_dt, validate_start_dt, validate_end_dt

    def run(self):
        """
        取训练数据和验证数据
        """
        # 取功率数据
        power_wsr_data = self.get_power_wsr()

        if self.params.get("start_dt") and self.params.get("end_dt"):
            train_start_dt,train_end_dt,validate_start_dt,validate_end_dt = self.get_train_dt_by_start_end(self.params["start_dt"], self.params["end_dt"])
        else:
            # 解析时间范围
            last_dt = power_wsr_data.index[-1]
            train_start_dt,train_end_dt,validate_start_dt,validate_end_dt = self.get_train_dt(last_dt)

        all_datas = power_wsr_data

        data_source = self.params.get("data_source", [])
        # 获取EC数据
        if "EC" in data_source:
            # 取训练数据
            train_data = self.get_EC_train_data(train_start_dt, train_end_dt)
            train_data = self.flat_EC_feature(train_data)
            train_data.columns = ["EC_%s" % i for i in train_data.columns]
            train_data["EC_data_type"]="train"

            # 取验证数据
            verify_data = self.get_EC_validate_data(validate_start_dt, validate_end_dt)
            verify_data = self.flat_EC_feature(verify_data)
            verify_data.columns = ["EC_%s" % i for i in verify_data.columns]
            verify_data["EC_data_type"]="validation"

            #训练集与验证集合和覆盖重复数据。
            EC_data = pd.concat([train_data, verify_data])
            EC_data = EC_data[~EC_data.index.duplicated()]
            all_datas = all_datas.merge(EC_data, left_index=True, right_index=True)

        # 获取GDFS数据
        if "GDFS" in data_source:
            # 取训练数据
            train_data = self.get_GDFS_train_data(train_start_dt, train_end_dt)
            train_data.columns = [i.lower().replace(":","_")  for i in train_data.columns]
            train_data = self.flat_GDFS_feature(train_data)
            train_data.columns = ["GDFS_%s" % i for i in train_data.columns]
            train_data["GDFS_data_type"]="train"

            # 取验证数据
            verify_data = self.get_GDFS_validate_data(validate_start_dt, validate_end_dt)
            verify_data.columns = [i.lower().replace(":","_")  for i in verify_data.columns]
            verify_data = self.flat_GDFS_feature(verify_data)
            verify_data.columns = ["GDFS_%s" % i for i in verify_data.columns]
            verify_data["GDFS_data_type"]="validation"

            #训练集与验证集合和覆盖重复数据。
            GDFS_data = pd.concat([train_data, verify_data])
            GDFS_data = GDFS_data[~GDFS_data.index.duplicated()]
            all_datas = all_datas.merge(GDFS_data, left_index=True, right_index=True)

        all_datas = self.func_add_time_features(all_datas)
        drop_columns = []
        for i in ["EC_data_type","GDFS_data_type"]:
            if i in all_datas.columns:
                if "data_type" not in all_datas.columns:
                    all_datas["data_type"] = all_datas[i]
                drop_columns.append(i)
        if drop_columns:
            all_datas.drop(columns=drop_columns, inplace=True)

        all_datas.sort_index(inplace=True)
        return all_datas

    def get_evaluate_data(self, start_time, end_time):
        # 取功率数据
        power_wsr_data = self.get_power_wsr(start_time, end_time)
        if power_wsr_data.empty:
            raise Exception(f'对应时间范围({start_time}, {end_time})未取到收资功率数据')
        all_datas = power_wsr_data

        data_source = self.params.get("data_source", [])
        # 获取EC数据
        if "EC" in data_source:
            # 取验证数据
            EC_data = self.get_EC_validate_data(start_time, end_time)
            EC_data.columns = [i.lower().replace(":","_")  for i in EC_data.columns]
            EC_data = self.flat_EC_feature(EC_data)
            EC_data.columns = ["EC_%s" % i for i in EC_data.columns]
            all_datas = all_datas.merge(EC_data, left_index=True, right_index=True)

        # 获取GDFS数据
        if "GDFS" in data_source:
            # 取验证数据
            GDFS_data = self.get_GDFS_validate_data(start_time, end_time)
            GDFS_data.columns = [i.lower().replace(":","_")  for i in GDFS_data.columns]
            GDFS_data = self.flat_GDFS_feature(GDFS_data)
            GDFS_data.columns = ["GDFS_%s" % i for i in GDFS_data.columns]
            all_datas = all_datas.merge(GDFS_data, left_index=True, right_index=True)

        all_datas = self.func_add_time_features(all_datas)

        return all_datas

    def evaluate(self):
        """
        评估模型回测预测准确
        """
        evaluate_data = pd.DataFrame()
        if self.params.get("periods"):
            for period in self.params["periods"]:
                data = self.get_evaluate_data(period["s"], period['e'])
                evaluate_data = evaluate_data.append(data)
        elif self.params.get("windows"):
            # 取功率数据
            power_wsr_data = self.get_power_wsr()
            # 解析时间范围
            last_dt = power_wsr_data.index[-1]
            windows = self.params["windows"]
            evaluate_start, evaluate_end = self.cal_data_range(windows, last_dt=last_dt)
            evaluate_data = self.get_evaluate_data(evaluate_start, evaluate_end)
        else:
            raise ValueError("没达到取评估数据的条件")
        evaluate_data.sort_index(inplace=True)
        return evaluate_data

    def predict(self):
        """
        预测气象数据主函数
        """
        data= pd.DataFrame()
        data_source = self.params.get("data_source", [])
        if "EC" in data_source:
            EC_data = self.EC_predict()
            EC_data = self.flat_EC_feature(EC_data)
            EC_data.columns = [(("EC_%s" % i) if i!="time" else i) for i in EC_data.columns]
            data = EC_data if data.empty else data.merge(EC_data, on="time")
        if "GDFS" in data_source:
            GDFS_data = self.GDFS_predict()
            GDFS_data=self.flat_GDFS_feature(GDFS_data)
            GDFS_data.columns = [(("GDFS_%s" % i) if i!="time" else i) for i in GDFS_data.columns]
            data = GDFS_data if data.empty else data.merge(GDFS_data, on="time")
        data = self.interplocate_df(data.resample("1H").first())
        data = self.func_add_time_features(data)
        return data
