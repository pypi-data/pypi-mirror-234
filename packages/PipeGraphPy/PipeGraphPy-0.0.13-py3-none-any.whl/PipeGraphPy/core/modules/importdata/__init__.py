# from .algodata import Algodata

from PipeGraphPy.core.modules import MBase
import pandas as pd
import re
# from PipeGraphPy.utils.read_nwp_tar import read_nwp_tar
from PipeGraphPy.constants import FARMTYPE
# from algo_data.utils import inp_heights
# import algo_data
from PipeGraphPy.logger import plog
from collections import namedtuple
from PipeGraphPy.config import settings
from datetime import datetime, timedelta

replace_over_dayflag_wth = {"MIX":2}
DATAWAREHOUSE = "数仓"
PatchSource = namedtuple("PatchSource", ["nwp_source", "stn_id", "clock"])

PATCH_SOURCE = {
        "12":[
            PatchSource("MO", "001", "12"),
            PatchSource("GFS", "001", "12"),
            PatchSource("MO", "001", "00"),
            PatchSource("GFS", "001", "00"),
        ],
        "00":[
            PatchSource("MO", "001", "00"),
            PatchSource("GFS", "001", "00"),
            PatchSource("MO", "001", "12"),
            PatchSource("GFS", "001", "12"),
        ],
}

day_flag_pattern = re.compile(r"^\d{1,2}$|^\d{1,2}-\d{1,2}$")

class InputDataBase(MBase):
    def get_obs_table(self):
        ops_source = self.params["obs_source"]
        if ops_source == "exportdb":
            return "exportdb.factory_%s" % self.wfid
        elif ops_source == "oms":
            return "short_%s" % self.wfid
        elif ops_source == "Actual15Min":
            return "Actual15Min.actual_15min_%s" % self.wfid
        else:
            self.stop_run("配置obs_source不正确")

    def resent_dt(self, end_dt):
        """查找某一时间之前的最近的实测时间"""
        where = dict(
            wfid=self.wfid,
            end_dt=end_dt,
            layer='dwd',
            columns="dtime",
            dtype='dict',
            sort='desc',
            limit=1
        )
        if self.params.get("check_result"):
            where["check_result"] = self.params.get("check_result")

        obs_data = algo_data.obs_15min(**where)
        if not obs_data:
            raise Exception("在查找最新一条实测数据时，发现此场站不存在实测数据")
        return obs_data["dtime"]

    def last_dt(self):
        where = dict(
            wfid=self.wfid,
            layer='dwd',
            columns="dtime",
            dtype='dict',
            sort='desc',
            limit=1
        )
        if self.params.get("check_result"):
            where["check_result"] = self.params.get("check_result")

        obs_data = algo_data.obs_15min(**where)
        if not obs_data:
            raise Exception("在查找最新一条实测数据时，发现此场站不存在实测数据")
        return obs_data["dtime"]

    def _prase_date(self, days, reserve=0):
        """解析训练数据和测试数据的时间范围"""
        end_dt = self.last_dt()
        if end_dt.hour != 23:
            end_dt = end_dt - timedelta(days=1)
        if reserve:
            end_dt = end_dt - timedelta(days=int(reserve))
            train_end = self.resent_dt(end_dt=end_dt.strftime("%Y-%m-%d 23:59:59"))
            if train_end.hour != 23:
                train_end = train_end - timedelta(days=1)
        else:
            train_end = end_dt
        train_start = train_end - timedelta(days=int(days)-1)
        train_start = train_start.strftime("%Y-%m-%d")
        train_end = train_end.strftime("%Y-%m-%d")
        return train_start, train_end

    def _get_start_and_end_date(self):
        """获取开始时间和结果时间"""
        if self.params.get("start_dt") and self.params.get("end_dt"):
            try:
                sd = datetime.datetime.strptime(self.params["start_dt"], '%Y-%m-%d')
                ed = datetime.datetime.strptime(self.params["end_dt"], '%Y-%m-%d')
                if sd >= ed:
                    raise Exception("时间范围选择不正确")
            except Exception:
                raise Exception("时间格式不正确，必须为:YYYY-mm-dd")
            train_start = self.params["start_dt"]
            train_end = self.params["end_dt"]
        elif self.params.get('data_length'):
            reserve = self.params.get('reserve_length', 20)
            train_start, train_end = self._prase_date(
                    self.params["data_length"], reserve=reserve)
        else:
            raise Exception('没有选择训练数据日期范围')
        self.print("数据时间范围：%s" % [train_start, train_end])
        return train_start, train_end

class AlgodataBase(InputDataBase):
    def __init__(self, **kw):
        InputDataBase.__init__(self, **kw)
        self.params = kw
        self.graph_info = kw.get("graph_info")
        self.wfid = self.graph_info["biz_id"]
        self.farm_info = kw.get("biz_info")
        default_feature = (
            "ghi_sfc"
            if self.farm_info["f_type"] == FARMTYPE.PV
            else ("wspd_70" if self.farm_info["f_type"] == FARMTYPE.WIND else None)
        )
        self.feature = self.params.get("feature") or [default_feature]
        assert isinstance(self.feature,list)
        self.max_count = 960
#
#
#     def _prase_day_flag(self):
#         """解析day_flag"""
#         if not self.params.get("day_flag"):
#             return [1]
#         day_flag = []
#         for i in self.params["day_flag"]:
#             i_str = str(i)
#             m = day_flag_pattern.match(i_str)
#             if m is None:
#                 raise ValueError("day_flag参数%s中的参数项%s格式错误" % (
#                     self.params["day_flag"], i_str))
#             if i_str.find("-") == -1:
#                 day_flag.append(int(i_str))
#             else:
#                 i_split = [int(j) for j in i_str.split("-")]
#                 min_i, max_i = min(i_split), max(i_split) + 1
#                 day_flag.extend(list(range(min_i, max_i)))
#         # 去重
#         day_flag = list(set(day_flag))
#         return day_flag or [1]
#
#     def _get_obs_data(self, start_dt, end_dt, columns=["r_apower"]):
#         """调用algo_data接口，获取数据库obs_data实测数据"""
#         columns = ["dtime"] + columns if "dtime" not in columns else columns
#         obs_where = dict(
#             wfid=self.wfid,
#             layer='dwd',
#             start_dt=start_dt,
#             end_dt=end_dt,
#             columns=','.join(columns)
#         )
#         if self.params.get("check_result"):
#             obs_where["check_result"] = self.params.get("check_result")
#         # if self.params.get("limit_type"):
#         #     obs_where[self.params["limit_type"]] = 0
#         return algo_data.obs_15min(**obs_where)
#
#
#     def run(self):
#         # 判断是否用理论功率
#         self.check_params()
#         res = self._get_data()
#         return res
#
#     def evaluate(self, **kwargs):
#         """获取评估数据"""
#         if (
#             self.farm_info["f_type"] == FARMTYPE.WIND
#             and "r_tirra" in self.params["out_col"]
#         ):
#             raise Exception("风电场%s不能配置辐照度实测值" % self.graph_info["id"])
#         elif (
#             self.farm_info["f_type"] == FARMTYPE.PV
#             and "r_wspd" in self.params["out_col"]
#         ):
#             raise Exception("光伏电场%s不能配置风速实测值" % self.graph_info["id"])
#         out_col = self.params.get("out_col")
#         # if self.params.get("limit_type") in ["limit_auto", "limit_artificial"]:
#         #     if self.farm_info["f_type"] == FARMTYPE.WIND and "r_wspd" not in out_col:
#         #         out_col.append("r_wspd")
#         #     elif self.farm_info["f_type"] == FARMTYPE.PV and "r_tirra" not in out_col:
#         #         out_col.append("r_tirra")
#         evaluate_data = pd.DataFrame()
#         if self.params.get("pub_date"):
#             # 取气象
#             pub_datetime = pd.to_datetime(self.params["pub_date"])
#             pub_date = pub_datetime.strftime("%Y%m%d")
#             weather_data = self._gen_predict_data_opt(
#                     nwp_config=self.params.get("nwp_config"),
#                     feature=self.feature,
#                     clock=self.params.get("clock","12"),
#                     pub_date=pub_date,
#                     is_rt=False)
#
#             # 取实测
#             index_list = weather_data.index.to_list()
#             if not index_list:
#                 raise Exception("不存在评估数据")
#             start_dt = (index_list[0] - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
#             end_dt = (index_list[-1] + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
#             obs_data = self._gen_obs_data(start_dt, end_dt, out_col)
#
#             # 合并obs_data和weather_data
#             evaluate_data = pd.merge(
#                     obs_data, weather_data, left_index=True, right_index=True, how="inner"
#                     ).sort_index()
#             if evaluate_data.empty:
#                 raise Exception("气象数据和实测数据合并后为空")
#         elif self.params.get("periods"):
#             for period in self.params["periods"]:
#                 data, obs_data, weather_data = self._get_train_data(
#                     nwp_config=self.params.get("nwp_config"),
#                     out_col=out_col,
#                     start_dt=period["s"],
#                     end_dt=period["e"],
#                     feature=self.feature,
#                     day_flag=self._prase_day_flag(),
#                     is_except=kwargs.get("is_except", False)
#                 )
#                 evaluate_data = evaluate_data.append(data)
#         elif self.params.get("windows"):
#             windows = self.params["windows"]
#             evaluate_start, evaluate_end = self._prase_date(windows)
#             evaluate_data, obs_data, weather_data = self._get_train_data(
#                 nwp_config=self.params.get("nwp_config"),
#                 out_col=out_col,
#                 start_dt=evaluate_start,
#                 end_dt=evaluate_end,
#                 feature=self.feature,
#                 day_flag=self._prase_day_flag(),
#                 is_except=kwargs.get("is_except", False)
#             )
#         else:
#             raise ValueError("没达到取评估数据的条件")
#
#         return evaluate_data
#
#     def _gen_obs_data(
#             self,
#             start_dt,
#             end_dt,
#             out_col=["r_apower"],
#             ):
#         """取实测数据"""
#
#         # if not set(out_col).issubset({"r_apower", "r_tirra", "r_wspd"}):
#         #     raise KeyError("out_col not in {'r_apower', 'r_tirra', 'r_wspd'} ")
#         if self.params.get("limit_type"):
#             out_col.append(self.params["limit_type"])
#
#         # 获取实测数据
#         obs_data = self._get_obs_data(start_dt=start_dt, end_dt=end_dt, columns=out_col)
#
#         if self.params.get("limit_type") and self.params["limit_type"] in obs_data.columns:
#             obs_data[self.params["limit_type"]] = obs_data[self.params["limit_type"]].fillna(-1)
#
#         # 取小于powercap * 1.1的数据 (此步骤放在了前处理里)
#         # if self.farm_info.get("powercap"):
#         #     obs_data = obs_data[obs_data["r_apower"]<=1.1*int(self.farm_info["powercap"])]
#         # 小于0 的功率置为0 (此步骤放在了前处理里)
#         # obs_data["r_apower"] = obs_data["r_apower"].apply(lambda x: 0 if x < 0 else x)
#         # 去nan值
#         obs_data = obs_data.dropna()
#
#         # 判断取的实测数据是否为空
#         if obs_data.empty:
#             raise Exception("所选日期(%s,%s)不存在实测数据,"
#                             "建议修改取数据时间范围" % (start_dt, end_dt))
#         obs_data = obs_data.set_index(keys="dtime")
#
#         # 判断是否某列实测数据未取到
#         for col in obs_data.columns:
#             if obs_data[col].isnull().all():
#                 raise Exception("所选日期(%s,%s)未取到实测数据列(%s)值" % (start_dt, end_dt, col))
#         return obs_data
#
#     def _read_nwp_tar(self, columns, **kwargs):
#         nwp_df = read_nwp_tar(**kwargs)
#         if nwp_df.empty:
#             return nwp_df
#         nwp_df["dtime"] = pd.to_datetime(nwp_df["dtime"])
#         nwp_df.set_index("dtime", inplace=True)
#         if not (set(['u_100', 'u_10', 'v_100', 'v_10']) - set(nwp_df.columns.to_list())):
#             inp_res = inp_heights(
#                     nwp_df['u_10'],
#                     nwp_df['v_10'],
#                     nwp_df['u_100'],
#                     nwp_df['v_100'],
#                     [10, 20, 30, 40, 50, 60, 80, 90, 100]
#                     )
#             for k, v in inp_res.items():
#                 nwp_df[k] = v
#         columns = [i for i in columns if i in nwp_df.columns]
#         rename_columns = {i:(
#             "%s_%s_%s" % (kwargs["weather_source"], i, kwargs["stn_id"])
#             ) for i in columns}
#         if "day_flag" in nwp_df.columns:
#             nwp_df = nwp_df[columns+["day_flag"]]
#         else:
#             nwp_df = nwp_df[columns]
#         nwp_df = nwp_df.rename(columns=rename_columns)
#         return nwp_df
#
#     def _gen_predict_weather_data(
#         self,
#         pub_date,
#         nwp_config={},
#         feature=["wspd_70"],
#         mark="12",
#         is_rt=True,
#         is_except=False
#     ):
#         # 取气象数据
#         try:
#             if is_rt:
#                 if settings.USE_RT_DB:
#                     if settings.RT_DB_CONNECTOR:
#                         algo_weather = algo_data.WeatherRT(connector=settings.RT_DB_CONNECTOR)
#                     else:
#                         algo_weather = algo_data.WeatherRT()
#                 else:
#                     # algo_weather = algo_data.WeatherRT(connector="mysql-rt-test")
#                     algo_weather = algo_data.WeatherRT()
#                 weather_data = algo_weather.multi_weather_forecast(
#                     self.wfid,
#                     pub_date=pub_date,
#                     nwp_config=nwp_config,
#                     feature=feature,
#                     mark=mark
#                 )
#             else:
#                 algo_weather = algo_data.WeatherWH()
#                 the_day = datetime.datetime.strptime(pub_date, '%Y%m%d')
#                 last_day = (the_day - timedelta(days=1)).strftime('%Y%m%d')
#                 nwp_start_time = last_day + mark
#                 start_dt = (the_day - timedelta(days=2)).strftime('%Y-%m-%d')
#                 end_dt = (the_day + timedelta(days=13)).strftime('%Y-%m-%d')
#                 weather_data = algo_weather.multi_weather_forecast(
#                     self.wfid,
#                     nwp_start_time=nwp_start_time,
#                     nwp_config=nwp_config,
#                     feature=feature,
#                     mark=mark,
#                     start_dt=start_dt,
#                     end_dt=end_dt
#                 )
#             if not weather_data.empty:
#                 weather_data = weather_data.set_index(keys="dtime")
#             columns = feature if isinstance(feature, list) else feature
#             for wth, stnids in nwp_config.items():
#                 stnids = stnids if isinstance(stnids, list) else [stnids]
#                 for stnid in stnids:
#                     column_names = ["%s_%s_%s" % (wth, c, stnid) for c in columns]
#                     # 如果数据不存在则取tar包的气象，tar包也没有，则报错
#                     if all([c not in weather_data.columns for c in column_names]):
#                         nwp_tar = self._read_nwp_tar(
#                                     columns=columns,
#                                     wfid=self.wfid,
#                                     weather_source=wth,
#                                     stn_id=stnid,
#                                     pub_date=pub_date,
#                                     clock=mark
#                                 )
#                         if nwp_tar.empty:
#                             raise Exception('气象源(%s)无预测数据, tar包也没有' % str([wth, stnid]))
#                         if weather_data.empty:
#                             weather_data = nwp_tar
#                         else:
#                             weather_data = weather_data.merge(
#                                     nwp_tar,
#                                     left_index=True,
#                                     right_index=True,
#                                     how="inner"
#                                     )
#
#             # if "day_flag" in weather_data.columns:
#             #     weather_data = weather_data.drop(columns=["day_flag"]).dropna(axis=1, how='all')
#
#             # weather_data = weather_data.dropna()
#             # 列名排序
#             weather_data = weather_data.sort_index(axis=1)
#             return weather_data
#         except Exception as e:
#             plog.info(e)
#             if is_except:
#                 raise e
#             else:
#                 return pd.DataFrame()
#
#
#     def _gen_weather_data(
#         self,
#         start_dt=None,
#         end_dt=None,
#         nwp_config=None,
#         feature=["wspd_70"],
#         day_flag=[1],
#         is_except=True
#     ):
#         # 取气象数据
#         weather_data = algo_data.WeatherWH().multi_weather_forecast(
#             self.wfid,
#             nwp_config=nwp_config,
#             feature=feature,
#             start_dt=start_dt,
#             end_dt=end_dt,
#             mark='12',
#             day_flag=day_flag
#         )
#         weather_data = weather_data.dropna()
#
#         if len(weather_data.columns) <= 1:
#             raise Exception("所选日期(%s,%s)不存在气象(%s)数据,"
#                             "建议修改取数据时间范围" % (start_dt, end_dt, nwp_config))
#         weather_data = weather_data.set_index(keys="dtime")
#         # 列名排序
#         weather_data = weather_data.sort_index(axis=1)
#         # 不存在气象源报错
#         if is_except:
#             columns = feature if isinstance(feature, list) else feature
#             for wth, stnids in nwp_config.items():
#                 stnids = stnids if isinstance(stnids, list) else [stnids]
#                 for stnid in stnids:
#                     column_names = ["%s_%s_%s" % (wth, i, stnid) for i in columns]
#                     # 如果数据不存在则直接报错，回为如果缺少数据，预测会报错
#                     if not any([(c in weather_data.columns) for c in column_names]):
#                         raise Exception('所选日期(%s)不存在气象源(%s)数据' % (
#                             str([start_dt, end_dt]), str([wth, stnid])))
#
#         return weather_data
#
#     def _patch_predict_data(self, patch_df, nwp_df, feature, nwp_config, patch_source, patch_stn_id):
#         """补气象"""
#         # 通过其他气象补时长
#         features = feature if isinstance(feature, list) else [feature]
#         patch_columns, nwp_columns = [], []
#         patch_df_copy = patch_df.copy()
#
#         # 根据nwp气象的列复制patch的列
#         for wth, stnids in nwp_config.items():
#             stnids = stnids if isinstance(stnids, list) else [stnids]
#             for stnid in stnids:
#                 for field in features:
#                     patch_column = "%s_%s_%s" % (patch_source, field, patch_stn_id)
#                     nwp_column = "%s_%s_%s" % (wth, field, stnid)
#                     if nwp_column not in patch_df_copy.columns:
#                         patch_df_copy[nwp_column] = patch_df_copy[patch_column]
#                     patch_columns.append(patch_column)
#                     nwp_columns.append(nwp_column)
#
#         # 去掉patch列
#         drop_patch_columns = list(set(patch_columns) - set(nwp_columns))
#         if drop_patch_columns:
#             patch_df_copy.drop(columns=drop_patch_columns, inplace=True)
#
#         # 连接去重
#         df_append = nwp_df.append(patch_df_copy)
#         patched_df = df_append.groupby(df_append.index).first()
#
#         # MIX气象day_flag>=2的都使用补气象
#         for wth, stnids in nwp_config.items():
#             if wth not in replace_over_dayflag_wth:
#                 continue
#             stnids = stnids if isinstance(stnids, list) else [stnids]
#             for stnid in stnids:
#                 for field in features:
#                     patch_column = "%s_%s_%s" % (patch_source, field, patch_stn_id)
#                     nwp_column = "%s_%s_%s" % (wth, field, stnid)
#                     over_dayflag_df = patch_df.loc[patch_df["day_flag"]>=replace_over_dayflag_wth[wth]][patch_column]
#                     patched_df.loc[over_dayflag_df.index, nwp_column] = over_dayflag_df
#         return patched_df
#
#     def _get_train_data(
#         self,
#         start_dt,
#         end_dt,
#         nwp_config=None,
#         out_col=["r_apower"],
#         feature=["wspd_70"],
#         day_flag=[1],
#         is_except=True
#     ):
#         """
#         取训练数据和评估数据
#         """
#         # 取实测
#         obs_data = self._gen_obs_data(start_dt, end_dt, out_col)
#
#         # 取气象
#         weather_data = self._gen_weather_data(
#                 start_dt=start_dt,
#                 end_dt=end_dt,
#                 nwp_config=nwp_config,
#                 feature=feature,
#                 day_flag=day_flag,
#                 is_except=is_except)
#
#         # 合并obs_data和weather_data
#         merge_data = pd.merge(
#                 obs_data, weather_data, left_index=True, right_index=True, how="inner"
#                 ).sort_index()
#
#         if merge_data.empty:
#             self.print("实测数据:\n %s" % obs_data)
#             self.print("气象数据:\n %s" % weather_data)
#             raise Exception("气象数据和实测数据合并后为空")
#
#         return merge_data, obs_data, weather_data
#
#     def _gen_predict_data_opt(self, nwp_config, feature, clock, pub_date, is_rt=True):
#         try:
#             nwp_data = self._gen_predict_weather_data(
#                 pub_date=pub_date,
#                 nwp_config=nwp_config,
#                 feature=feature,
#                 mark=clock,
#                 is_rt=is_rt,
#                 is_except=True
#             )
#             if nwp_data.empty:
#                 raise Exception("无气象%s数据" % nwp_config)
#
#             # 补气象
#             clock_order = ["12", "00"] if clock=="12" else ["00", "12"]
#             patch_data = pd.DataFrame()
#             patch_data_success = 0
#             for patch_clock in clock_order:
#                 try:
#                     if patch_clock == "00" and clock=="12":
#                         yesterday = (
#                                 datetime.datetime.strptime(
#                                     pub_date, '%Y%m%d'
#                                     ) - timedelta(days=1)
#                                 ).strftime('%Y%m%d')
#                         pub_date = yesterday
#                     for patch_nwp, patch_stnid in [("IBM", "001"), ("MO", "001"), ("GFS", "001")]:
#                         try:
#                             patch_data = self._gen_predict_weather_data(
#                                 pub_date=pub_date,
#                                 nwp_config={patch_nwp: [patch_stnid]},
#                                 feature=feature,
#                                 mark=patch_clock,
#                                 is_rt=is_rt
#                             )
#                             for i in feature:
#                                 if patch_data["%s_%s_%s" % (patch_nwp, i, patch_stnid)].isnull().any():
#                                     patch_data = pd.DataFrame()
#                                     break
#                             if patch_data.empty:
#                                 continue
#                             # 补时长
#                             nwp_data = self._patch_predict_data(
#                                     patch_data,
#                                     nwp_data,
#                                     feature,
#                                     nwp_config,
#                                     patch_nwp,
#                                     patch_stnid
#                                     )
#                             if patch_nwp in ["IBM", "GFS"]:
#                                 patch_data_success = 1
#                         except:
#                             pass
#                     if patch_data_success:
#                         break
#                 except:
#                     pass
#             if not patch_data_success:
#                 raise Exception("补气象失败")
#             if nwp_data.empty:
#                 raise Exception("读取气象数据失败")
#             nwp_data = nwp_data.dropna()
#             # 生成day_flag=15的数据
#             nwp_data = self._patch_15_day_flag(nwp_data)
#             return nwp_data
#         except Exception as e:
#             raise e
#
#     def _patch_15_day_flag(self, nwp_data):
#         # 判断是否有day_flag字段
#         if "day_flag" not in nwp_data.columns:
#             raise Exception("气象未取到day_flag字段")
#         day_13_df = nwp_data[nwp_data["day_flag"]==13].drop(columns=["day_flag"])
#         day_14_df = nwp_data[nwp_data["day_flag"]==14].drop(columns=["day_flag"])
#         if day_13_df.shape[0] != day_14_df.shape[0]:
#             raise Exception("day_flag(13和14)的数据长度不同(%s, %s)" % (day_13_df.shape[0], day_14_df.shape[0]))
#         new_nwp_data = nwp_data[nwp_data["day_flag"]<15]
#         day_15_df = pd.DataFrame(
#                 (day_13_df.values + day_14_df.values)/2,
#                 columns = day_14_df.columns,
#                 index = day_14_df.index.map(lambda x:x+timedelta(days=1))
#             )
#         day_15_df["day_flag"] = 15
#         new_nwp_data = new_nwp_data.append(day_15_df)
#         return new_nwp_data
#
#     def _get_predict_weather_data_from_rs(
#         self,
#         pub_dates,
#         nwp_config={},
#         feature=["wspd_70"],
#         mark="12",
#         is_except=False
#     ):
#         # 取气象数据
#         try:
#             algo_weather = algo_data.WeatherWH()
#             weather_data = []
#             for pubdate in pub_dates:
#                 _data = algo_weather.multi_weather_forecast(
#                     self.wfid,
#                     pub_date=pubdate,
#                     nwp_config=nwp_config,
#                     feature=feature,
#                     mark=mark,
#                 )
#                 weather_data.append(_data)
#             weather_df = pd.concat(weather_data, axis=0)
#
#             if not weather_df.empty:
#                 weather_df = weather_df.set_index(keys="dtime")
#             weather_df = weather_df.dropna()
#             # 列名排序
#             weather_df = weather_df.sort_index(axis=1)
#             return weather_df
#         except Exception as e:
#             plog.info(e)
#             if is_except:
#                 raise e
#             else:
#                 return pd.DataFrame()
#
#
#     def predict(self):
#         """预测数据"""
#         if self.params.get("predict_start_dt") and self.params.get("predict_end_dt"):
#             date_list = pd.date_range(
#                     self.params["predict_start_dt"],
#                     self.params["predict_end_dt"],
#                     freq="D")
#             aim_dates = [(i-timedelta(days=1)).strftime("%Y%m%d") for i in date_list]
#             predict_df = self._get_predict_weather_data_from_rs(
#                     nwp_config=self.params.get("nwp_config"),
#                     pub_dates=aim_dates,
#                     feature=self.feature,
#                     mark=self.params.get("clock","12"),
#                     )
#         elif self.params.get("predict_date"):
#             aim_dates = [(pd.to_datetime(self.params["predict_date"]) - timedelta(days=1)).strftime("%Y%m%d")]
#             predict_df = self._get_predict_weather_data_from_rs(
#                     nwp_config=self.params.get("nwp_config"),
#                     pub_dates=aim_dates,
#                     feature=self.feature,
#                     mark=self.params.get("clock","12"),
#                     )
#         else:
#             today_str = ((datetime.utcnow()+timedelta(hours=8))).strftime("%Y%m%d")
#             predict_df = self._gen_predict_data_opt(
#                     nwp_config=self.params.get("nwp_config"),
#                     feature=self.feature,
#                     clock=self.params.get("clock","12"),
#                     pub_date=today_str,
#                     is_rt=True
#                     )
#         if predict_df.empty:
#             raise Exception("未取到预测数据")
#         return predict_df
#
