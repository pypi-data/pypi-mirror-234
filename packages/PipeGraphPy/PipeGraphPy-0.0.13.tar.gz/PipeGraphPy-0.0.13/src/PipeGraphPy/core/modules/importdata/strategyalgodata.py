# coding: utf8

import json
import copy
import random
# import algo_data as ad
import pandas as pd
from PipeGraphPy.db.utils import update_node_params
from PipeGraphPy.constants import FARMTYPE, DB
from PipeGraphPy.constants import DATATYPE
from . import AlgodataBase
from dateutil.relativedelta import relativedelta
from dbpoolpy import connect_db, Select
from collections import defaultdict
from PipeGraphPy.logger import plog
from PipeGraphPy.config import settings
from PipeGraphPy.core.module import Module
from PipeGraphPy.core.node import Node
from PipeGraphPy.core.graph import Graph
from datetime import date, datetime

DATAWAREHOUSE = "数仓"


class STRATEGY_TYPE:
    AUTO = "auto"
    NWP = "nwp"

def get_df(wfid, now, date_limit):
    refer_sql = f"""
                SELECT
                    MAX(dtime) "end_db",
                    MIN(dtime) "start_db"
                FROM
                    ads.ads_nwp_indicator
                WHERE
                    wfid = {wfid} AND target_amount>=48
                    AND dtime BETWEEN '{date_limit}' AND '{now}'
                """

    with connect_db(DB.dbrs) as rsdb:
        datas = rsdb.query(refer_sql)
        return pd.DataFrame(datas)

def nwp_choose_nwp(wfid, source):
    try:
        nwp_auto = Select(DB.db119, "MeteInfo.PipeGraphPy_source_config").where(wfid=wfid, source=source).first()
        if not nwp_auto:
            raise Exception("从PipeGraphPy_source_config数据表中未取到对应电场的气象源配置")
        use_nwp_auto = json.loads(nwp_auto["use_nwp_auto"])
        assert isinstance(use_nwp_auto, dict), ValueError("PipeGraphPy_source_config配置的use_nwp_auto字段不是json")
        return use_nwp_auto
    except Exception as e:
        raise Exception("从PipeGraphPy_source_config数据表中取对应气象源配置时报错：\n %s" % e)


def auto_choose_nwp(self, wfid, days=30, reserve=0, start=None, end=None, **kwargs):
    try:
        # 自动气象择优参数
        if 'top_num' in kwargs.keys():
            kwargs['topn'] = kwargs.pop('top_num')
        top_num = kwargs.get('topn', 3)
        weight = kwargs.get('weight', 0.5)

        # 这一块是数仓 dwd.dwd_calaind_short_nwp_ind_di 中的字段
        # 对气象指标进行筛选
        day_flag = kwargs.get('day_flag', 1)
        mark = kwargs.get('mark', '12')
        indicator_classify = kwargs.get('indicator_classify', 'rmse_value')
        suit_day_period = kwargs.get('suit_day_period', '')

        # 禁用气象源参数
        if 'fsbl' in kwargs.keys():
            kwargs['forecast_source_blacklist'] = kwargs.pop('fsbl')
        forecast_source_blacklist = kwargs.get('forecast_source_blacklist', [])
        if 'sibl' in kwargs.keys():
            kwargs['stn_id_blacklist'] = kwargs.pop('sibl')
        stn_id_blacklist = kwargs.get('stn_id_blacklist', [])
        if 'nwpbd' in kwargs.keys():
            kwargs['nwp_blackdict'] = kwargs.pop('nwpbd')
        nwp_blackdict = kwargs.get('nwp_blackdict', {})

        # 气象择优的起止时间
        now = date.today()
        now = datetime.strptime(f'{now}' + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        if start and end:
            start_time = datetime.strptime(str(start) + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
            assert isinstance(start_time, datetime)
            end_time = datetime.strptime(str(end) + ' 23:45:00', "%Y-%m-%d %H:%M:%S")
            assert isinstance(end_time, datetime)

            date_limit = now - relativedelta(days=reserve)
            if end_time>date_limit:
                end_time = date_limit
                if end_time<start_time:
                    self.print("排除预留天数之后，发现 end_time < start_time，需要重新选择起止时间！")
                    return {"EC": "001"}
            # 格式转为 str
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # 先确定 end_time
            date_limit = now - relativedelta(months=3)
            refer_sql = f"""
                        SELECT
                            MAX(dtime) "end_db",
                            MIN(dtime) "start_db"
                        FROM
                            dwd.dwd_calaind_short_nwp_ind_di dcsnid
                        WHERE
                            wfid = {wfid} AND cal_data_length>=48
                            AND dtime BETWEEN '{date_limit}' AND '{now}'
                            AND mark = '{mark}' AND day_flag = {day_flag}
                            AND indicator_classify = '{indicator_classify}' AND suit_day_period = '{suit_day_period}'
                        """
            # api = ad.Api(connector='rs-read', db='dev')
            api = None
            df = api.read_sql(refer_sql)
            if df.dropna(how='all').empty:
                return {"EC":"001"}
            end_time = df['end_db'].iloc[0]

            date_flag = now - relativedelta(days=reserve)
            if end_time>date_flag:
                end_time = date_flag

            # 再确定 start_time
            start_time = end_time - relativedelta(days=days)
            # 格式转为 str
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

        # 气象数据量检查参数，保证筛选出的气象具有足够的数据
        start_nwpsize = kwargs.get('start_nwpsize', start_time.split()[0])
        start_nwpsize = datetime.strptime(str(start_nwpsize) + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        end_nwpsize = kwargs.get('end_nwpsize', end_time.split()[0])
        end_nwpsize = datetime.strptime(str(end_nwpsize) + ' 23:45:00', "%Y-%m-%d %H:%M:%S")
        nwpsize = kwargs.get('nwpsize', 30)


        # 自动气象选择 algo_data.ChooseNwp
        # cn = ad.ChooseNwp(wfid=wfid, start=start_time, end=end_time, topn=top_num,  day_flag=day_flag, mark=mark,
        #                   indicator_classify=indicator_classify, suit_day_period=suit_day_period,
        #                   forecast_source_blacklist=forecast_source_blacklist, stn_id_blacklist=stn_id_blacklist,
        #                   nwp_blackdict = nwp_blackdict, start_nwpsize=start_nwpsize, end_nwpsize=end_nwpsize,
        #                   nwpsize=nwpsize)
        cn = None
        nwp_choosen_df, _ = cn.choosen_weight(rank_weight=weight)

        nwp_dict = {}
        for nwp_and_point in nwp_choosen_df.iloc[0,1][:top_num]:
            nwp, point = nwp_and_point.split('_')
            if nwp in nwp_dict.keys():
                nwp_dict[nwp].append(point)
            else:
                nwp_dict[nwp] = [point]
        return nwp_dict
    except Exception as err:
        import traceback
        print(traceback.format_exc())
        self.print("【气象择优有误！】", err)
        return {"EC":"001"}


class StrategyAlgodata(AlgodataBase):
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
            "key": "strategy",
            "name": "策略",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "auto",
            "source": ["auto", "nwp"],
            "desc": "策略类型",
        },
        {
            "key": "strategy_params",
            "name": "策略传参",
            "type": "string",
            "plugin": "text",
            "need": False,
            "value": "{'days':30,\n'reserve':0,\n'topn':3,\n'nwpsize':30,\n'indicator_classify':'rmse_value'\n}",
            "desc": "",
        },
        {
            "key": "doc",
            "name": "auto气象择优参数说明文档",
            "type": "string",
            "plugin": "text",
            "need": False,
            "value": "http://confluence.goldwind.com.cn/pages/viewpage.action?pageId=111810326",
            "desc": "字段说明",
        },
        {
            "key": "nwp_config",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "input",
            "need": False,
            "value": "{}",
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
        "strategy": {
            "name": "策略",
            "type": str,
            "need": True,
            "range": [],
            "source": ["auto", "nwp"],
        },
        "strategy_params": {
            "name": "策略传参",
            "type": dict,
            "need": False,
            "range": [],
            "source": [],
        },
        "nwp_config": {
            "name": "预测数据气象源",
            "type": dict,
            "need": False,
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


    # def _gen_predict_weather_data(
    #     self,
    #     pub_date,
    #     nwp_config={},
    #     feature=["wspd_70"],
    #     mark="12",
    #     is_rt=True,
    #     is_except=False
    # ):
    #     # 取气象数据
    #     try:
    #         if is_rt:
    #             if settings.USE_RT_DB:
    #                 if settings.RT_DB_CONNECTOR:
    #                     algo_weather = ad.WeatherRT(connector=settings.RT_DB_CONNECTOR)
    #                 else:
    #                     algo_weather = ad.WeatherRT()
    #             else:
    #                 # algo_weather = ad.WeatherRT(connector="mysql-rt-test")
    #                 algo_weather = ad.WeatherRT()
    #         else:
    #             algo_weather = ad.WeatherWH()
    #         weather_data = algo_weather.multi_weather_forecast(
    #             self.wfid,
    #             pub_date=pub_date,
    #             nwp_config=nwp_config,
    #             feature=feature,
    #             mark=mark
    #         )
    #         if not weather_data.empty:
    #             weather_data = weather_data.set_index(keys="dtime")
    #         columns = feature if isinstance(feature, list) else feature
    #         nwp_config_features = []
    #         for wth, stnids in nwp_config.items():
    #             stnids = stnids if isinstance(stnids, list) else [stnids]
    #             for stnid in stnids:
    #                 column_names = ["%s_%s_%s" % (wth, c, stnid) for c in columns]
    #                 nwp_config_features.extend(column_names)
    #                 # 如果数据不存在则取tar包的气象，tar包也没有，则报错
    #                 if all([c not in weather_data.columns for c in column_names]):
    #                     try:
    #                         nwp_tar = self._read_nwp_tar(
    #                                     columns=columns,
    #                                     wfid=self.wfid,
    #                                     weather_source=wth,
    #                                     stn_id=stnid,
    #                                     pub_date=pub_date,
    #                                     clock=mark
    #                                 )
    #                     except Exception as e:
    #                         if is_except and self.params["strategy"] != 'nwp':
    #                             raise e
    #                         else:
    #                             nwp_tar = pd.DataFrame()
    #                     if nwp_tar.empty:
    #                         continue
    #                     if weather_data.empty:
    #                         weather_data = nwp_tar
    #                     else:
    #                         weather_data = weather_data.merge(
    #                                 nwp_tar,
    #                                 left_index=True,
    #                                 right_index=True,
    #                                 how="inner"
    #                                 )
    #         if self.params["strategy"] == 'nwp':
    #             nwp_auto = Select(
    #                     DB.db119,
    #                     "MeteInfo.PipeGraphPy_source_config"
    #                     ).where(
    #                             wfid=self.wfid,
    #                             source=self.params["strategy_params"]["source"]
    #                     ).first()
    #             backup_time = nwp_auto.get("backup_time")
    #             if not backup_time:
    #                 raise Exception(
    #                         "数据库MeteInfo.PipeGraphPy_source_config未配置backup_time")
    #             patch_nwp_time = None
    #             today = date.today()
    #             try:
    #                 patch_nwp_time = datetime.strptime(
    #                     str(today) + " %s" % backup_time,
    #                     "%Y-%m-%d %H:%M:%S")
    #             except:
    #                 raise Exception("backup_time参数格式错误")
    #             # nwp策略补气象
    #             now = (datetime.utcnow()+timedelta(hours=8))
    #             nwp_columns = [i for i in weather_data.columns if i != 'day_flag']
    #             if len(nwp_columns) == 0:
    #                 raise Exception("未取到任何气象源数据,nwp无法补气象源")
    #             if patch_nwp_time and now >= patch_nwp_time:
    #                 non_features = list(set(nwp_config_features)-set(nwp_columns))
    #                 if non_features:
    #                     self.print("缺失特征：%s" % non_features)
    #                     for column_name in non_features:
    #                         random_columns = random.choice(nwp_columns)
    #                         weather_data[column_name] = weather_data[random_columns]
    #                         self.print("%s气象值不存在，随机由%s气象值补" % (
    #                             column_name, random_columns))
    #             else:
    #                 for wth, stnids in nwp_config.items():
    #                     stnids = stnids if isinstance(stnids, list) else [stnids]
    #                     column_names = ["%s_%s_%s" % (wth, c, stnid) for c in columns for stnid in stnids]
    #                     if not any([c in nwp_columns for c in column_names]):
    #                         raise Exception("缺失气象源: %s数据, 未到补气象时间" % wth)

    #         # weather_data = weather_data.dropna()
    #         # 列名排序
    #         weather_data = weather_data.sort_index(axis=1)
    #         return weather_data
    #     except Exception as e:
    #         plog.info(e)
    #         if is_except:
    #             raise e
    #         else:
    #             return pd.DataFrame()

    def _sk_feature_select(self, nwp_auto, **kwargs):
        selector_graph = Graph.create(wfid=self.wfid)
        feature_selector_node = Node.create(Module.use('SkFeatureSelector'), selector_graph)
        if kwargs:
            feature_selector_node.params = {"params": kwargs}
        train_start, train_end = self._get_start_and_end_date()
        train_data, obs_data, weather_data = self._get_train_data(
            nwp_config=nwp_auto,
            out_col=self.params.get("out_col"),
            start_dt=train_start,
            end_dt=train_end,
            feature=self.feature,
            day_flag=self._prase_day_flag()
        )
        selected_data = feature_selector_node.run(train_data)
        if not isinstance(selected_data, pd.DataFrame) or selected_data.empty:
            raise Exception("调用SkFeatureSelector做特征筛选报错")
        train_nwp_config = defaultdict(list)
        for i in selected_data.columns:
            i_split = str(i).split("_")
            if len(i_split) == 4:
                train_nwp_config[i_split[0]].append(i_split[-1])
        return dict(train_nwp_config)

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
        algo_params = self.params.get("strategy_params") or dict()
        if str(self.params["strategy"]).lower() == STRATEGY_TYPE.AUTO:
            algo_params["start_nwpsize"] = train_start
            algo_params["end_nwpsize"] = train_end
            try:
                # self.params["nwp_config"] = ad.auto_choose_nwp(self.wfid, **algo_params)
                pass
            except Exception as err:
                self.print(err)
                self.print('auto气象择优有误，采用EC_001')
                self.params["nwp_config"] = {'EC':['001']}
            if not self.params["nwp_config"]:
                raise Exception("auto自动气象选择未选出任何气象源")
            self.print("预选气象源：%s" % self.params["nwp_config"])
            if self.params["nwp_config"]:
                if isinstance(self.graph_info["id"], int) and self.graph_info["id"] <99999999:
                    if isinstance(self.params["node_info"]["id"], int):
                        update_node_params(
                            self.params["node_info"]["id"], "nwp_config", str(self.params["nwp_config"])
                        )

            train_data, obs_data, weather_data = self._get_train_data(
                nwp_config=self.params.get("nwp_config"),
                out_col=self.params.get("out_col"),
                start_dt=train_start,
                end_dt=train_end,
                feature=self.feature,
                day_flag=self._prase_day_flag()
            )
            if train_data.empty:
                raise Exception("未取到训练数据")
            return train_data
        elif str(self.params["strategy"]).lower() == STRATEGY_TYPE.NWP:
            if "source" not in algo_params:
                raise Exception("source参数不在策略参数配置里面")
            selector_params = copy.deepcopy(algo_params)
            nwp_choose = nwp_choose_nwp(self.wfid, selector_params.pop("source"))
            self.print("特征选择使用的气象源：%s" % nwp_choose)

            selector_graph = Graph.create(wfid=self.wfid)
            feature_selector_node = Node.create(selector_graph, Module.use('filterFeature'))
            if selector_params:
                feature_selector_node.params = {"params": selector_params}
            train_data, obs_data, weather_data = self._get_train_data(
                nwp_config=nwp_choose,
                out_col=self.params.get("out_col"),
                start_dt=train_start,
                end_dt=train_end,
                feature=self.feature,
                day_flag=self._prase_day_flag(),
                is_except=False
            )
            self.print("有数据的特征：%s" % train_data.columns)
            selected_data = feature_selector_node.run(train_data)
            if not isinstance(selected_data, pd.DataFrame) or selected_data.empty:
                raise Exception("调用SkFeatureSelector做特征筛选报错")
            train_nwp_config = defaultdict(list)
            for i in selected_data.columns:
                i_split = str(i).split("_")
                if len(i_split) == 4:
                    train_nwp_config[i_split[0]].append(i_split[-1])
            self.params["nwp_config"] = dict(train_nwp_config)
            if not self.params["nwp_config"]:
                raise Exception("nwp自动气象选择未选出任何气象源")
            self.print("选出的气象源：%s" % self.params["nwp_config"])
            if self.params["nwp_config"]:
                if isinstance(self.graph_info["id"], int) and self.graph_info["id"]<99999999:
                    if isinstance(self.params["node_info"]["id"], int):
                        update_node_params(
                            self.params["node_info"]["id"], "nwp_config", str(self.params["nwp_config"])
                        )
            return selected_data
