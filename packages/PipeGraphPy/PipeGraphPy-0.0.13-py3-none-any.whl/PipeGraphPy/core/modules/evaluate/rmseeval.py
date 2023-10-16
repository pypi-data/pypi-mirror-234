# coding: utf8
import traceback
import pandas as pd
import numpy as np
from collections import defaultdict
from PipeGraphPy.constants import MODULES, STATUS
from PipeGraphPy.core.graph_base import GraphBase
from PipeGraphPy.core.graph import Graph
from PipeGraphPy.core.node import Node
from PipeGraphPy.core.module import Module
from PipeGraphPy.utils.core import cal_score_by_groupby


POWERCAP = 99
ALGODATA = "Qiao"
STRATEGYALGODATA = "StrategyAlgodata"

def rmse(y_true, y_pred, cap=POWERCAP):
    s = 1 - np.sqrt(np.mean((y_true - y_pred) ** 2))/cap
    return s*100

class TotalEvaluateData():
    def __init__(self, graphs, evaluate_graph_info, **params):
        self.graphs = graphs
        self.evaluate_graph_info = evaluate_graph_info
        self.params = params
        self.datas = dict()

    def get_algodata_evaluate(self, nodes):
        out_col = []
        day_flag = []
        nwp_config = defaultdict(list)
        feature = []
        check_result = []
        for n in nodes:
            out_col = list(set(out_col) | set(n.params["out_col"]))
            day_flag = list(set(day_flag) | set(n.params.get("day_flag") or [1]))
            for k, v in n.params["nwp_config"].items():
                v = v if isinstance(v, list) else [v]
                nwp_config[k] = list(set(nwp_config[k]) | set(v))
            feature = list(set(feature) | set(n.params["feature"]))
            check_result = list(set(check_result) | set(n.params.get("check_result")))
        graph = Graph.create(wfid=self.evaluate_graph_info['biz_id'])
        algo_data_node = Node.create(Module.use("Algodata"), graph)
        algo_data_node.params = {
                "out_col": out_col,
                "day_flag": day_flag,
                "nwp_config": dict(nwp_config),
                "feature": feature,
                "check_result": check_result
                }
        evaluate_data = algo_data_node.get_evaluate_data(**self.params)
        self.datas[ALGODATA] = evaluate_data

    def build_total_evaluate_data(self):
        """统一获取评估数据"""
        # 收集所有导入数据模块
        import_nodes = defaultdict(list)
        for g in self.graphs:
            for n in g.nodes:
                if n.module.parent.info["cls_name"] == MODULES.IMPORT:
                    import_nodes[n.module.info["cls_name"]].append(n)
        if import_nodes.get(ALGODATA) or import_nodes.get(STRATEGYALGODATA):
            self.get_algodata_evaluate(import_nodes[ALGODATA] + import_nodes[STRATEGYALGODATA])

    def _parse_head_node(self, node):
        if node.module.parent.info["cls_name"] != MODULES.IMPORT:
            return
        evaluate_data = None
        if node.module.info["cls_name"] in [ALGODATA, STRATEGYALGODATA]:
            if self.datas.get(ALGODATA) is not None:
                if not isinstance(self.datas.get(ALGODATA), pd.DataFrame):
                    raise Exception("总评估数据类型错误，不是DataFrame")
                # 取特征列
                feature_columns = []
                for wth, v in node.params["nwp_config"].items():
                    stn_ids = v if isinstance(v, list) else [v]
                    for stnid in stn_ids:
                        for f in node.params["feature"]:
                            feature_columns.append("%s_%s_%s" % (wth, f, stnid))
                # 取标签列
                out_col = node.params["out_col"]
                # 使用day_flag过滤
                all_columns = feature_columns + out_col + ["day_flag"]
                evaluate_data = self.datas[ALGODATA][list(set(self.datas[ALGODATA].columns)&set(all_columns))]
                evaluate_data = evaluate_data[
                        evaluate_data["day_flag"].isin(node.params.get("day_flag") or [1])]
        return evaluate_data

    def parse_evaluate_data(self, graph):
        model = graph.model
        if (len(model.a.start_nodes) == 1
            and model.a.start_nodes[0].module.parent.info["cls_name"] == MODULES.ENSEMBLE):
            head = model.a.start_nodes[0]
            graph_node = model.graph.a.nodes_dict.get(head.id)
            _cls = graph_node.module.parent.cls(graph_node, **self.params)
            return _cls.evaluate(**self.params)
        else:
            res_dict = dict()
            for head in model.a.start_nodes:
                head_node = graph.a.nodes_dict.get(head.id)
                evaluate_data = self._parse_head_node(head_node)
                if evaluate_data is not None:
                    res_dict[head] = evaluate_data
                else:
                    res = head_node.module.parent.cls(head_node, **self.params).evaluate()
                    res = res[-1] if isinstance(res, tuple) else res
                    if not isinstance(res, pd.DataFrame):
                        raise Exception("评估返回值必须是DataFrame数据")
                    res_dict[head] = res
        return res_dict

class EvaluateBase():
    def __init__(self, farm_info, train_graph, log, **params):
        self.farm_info = farm_info
        self.train_graph = train_graph
        self.log = log
        self.params = params
        self.powercap = self.farm_info.get("powercap", POWERCAP)

    def _calculate_score(self, y_real, y_pred):
        """计算评分"""
        score_value = 0
        if self.powercap:
            try:
                score_value = rmse(y_real, y_pred, int(self.powercap))
            except:
                pass
        if not score_value:
            score_value = rmse(y_real, y_pred)
        return score_value

    def evaluate(self, evaluate_data=None):
        score_value = 0
        predict_res = pd.DataFrame()

        # 取出模型
        model = self.train_graph.model

        # 取评估数据
        if evaluate_data is None:
            evaluate_data = model.get_evaluate_data(**self.params)
        self.log("评估数据:\n%s" % str(evaluate_data))

        # 预测
        predict_res = model.predict(head_res=evaluate_data)
        if predict_res is None:
            raise Exception("预测结果为None")

        # 取出预测结果
        label_columns = (self.params["label_columns"]
                if isinstance(self.params["label_columns"], list)
                else [self.params["label_columns"]])
        predict_label = [i + "_predict" for i in label_columns]

        # 取评估的原始实测
        y_df = pd.DataFrame()
        for i in evaluate_data.values():
            for c in i.columns:
                if c in label_columns:
                    y_df[c] = i[c]

        # 判断评估字段是否存在预测结果
        for i in predict_label:
            if i not in predict_res.columns:
                raise Exception("要评估的字段%s不存在预测结果里" % i)

        # 取出预测
        predict_df = predict_res[predict_label]

        # 取出后处理的实测
        post_real_df = pd.DataFrame()
        for i in predict_res.columns:
            if i in label_columns:
                post_real_df[i] = predict_res[i]

        # 后处理的实测优化使用
        real_df = y_df if post_real_df.empty else post_real_df

        if predict_df.empty:
            raise Exception("error!!! 预测结果有误! 不存在预测数据，无法评估")
        if real_df.empty:
            raise Exception("error!!! 预测结果有误！不存在实测数据，无法评估")
        if predict_df.isna().sum()[0]:
            raise Exception("error!!! 预测结果有误！存在空值，无法评估")
        if real_df.isna().sum()[0]:
            raise Exception("error!!! 预测结果有误！实测数据存在空值，无法评估")
        if len(predict_df) != len(real_df):
            merge_df = pd.merge(predict_df, real_df, left_index=True, right_index=True)
            predict_df = merge_df[predict_df.columns.to_list()]
            real_df = merge_df[real_df.columns.to_list()]
        # 评分
        score_value = self._calculate_score(real_df.values, predict_df.values)

        # 增加实测数据
        for i in label_columns:
            if i in real_df.columns:
                predict_res[i] = real_df[i]

        # 排序
        return predict_res, score_value


class RmseEval():
    TEMPLATE = [
        {
            "key": "windows",
            "name": "评估时间跨度(天)",
            "type": "int",
            "plugin": "input",
            "need": True,
            "value": 20,
            "desc": "字段说明",
        },
        {
            "key": "label_columns",
            "name": "标签列",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "['r_apower']",
            "desc": "要传递的标签列(多选)",
        },
        {
            "key": "wth_extract_type",
            "name": "气象数据提取方式" ,
            "type":"string",
            "plugin": "select",
            "need": True,
            "value": "业务版-15",
            "source": ["业务版-00", "业务版-15"],
            "desc": "字段说明",
        },
    ]
    params_rules = {
        "windows": {
            "type": int,
            "need": True,
            "range": [1, 100],
            "source": [],
        },
    }
    def __init__(self, **kw):
        self.params = kw
        self.farm_info = self.params.get('biz_info', {})
        self.graph_info = self.params.get('graph_info', {})
        self.powercap = self.farm_info.get('powercap', POWERCAP)
        self.theory_score = 50

    def run(self, graphs, return_daily_score=False):
        # 统一取评估数据
        total_evaluate_data = TotalEvaluateData(graphs, self.graph_info, **self.params)
        try:
            total_evaluate_data.build_total_evaluate_data()
        except:
            self.print(traceback.format_exc())

        evaluate_res, score_res = list(), list()
        daily_score_df = pd.DataFrame()
        for g in graphs:
            graph_id = g.id
            evaluate_df = pd.DataFrame()
            score = -999999
            try:
                self.print("正在评估graph_id:%s" % graph_id)
                if not isinstance(g, GraphBase):
                    raise Exception('传值graph不是Graph类')
                if g.status != STATUS.SUCCESS:
                    raise Exception('不能评估未训练成功的模型')

                # 理论功率模型直接赋分值
                if g.model.a.start_nodes[0].module.info["cls_name"] == MODULES.THEORYDATA:
                    evaluate_df = pd.DataFrame()
                    score = self.theory_score
                    continue

                # 取评估数据
                evaluate_datas = total_evaluate_data.parse_evaluate_data(g)

                evaluate_df, score = EvaluateBase(
                        self.farm_info,
                        g,
                        self.print,
                        **self.params
                        ).evaluate(evaluate_datas)

                if return_daily_score:
                    labels = self.params.get('label_columns')
                    label = str(labels[0] if isinstance(labels, list) else labels)
                    daily_score = cal_score_by_groupby(
                        evaluate_df,
                        rmse,
                        unit="day",
                        y_ture_col=label,
                        y_pred_col=label + "_predict",
                        cap=self.powercap
                    )
                    df = pd.DataFrame(
                            {g.id:[i[1] for i in daily_score]},
                            index=[i[0] for i in daily_score],
                            )
                    if daily_score_df.empty:
                        daily_score_df = df
                    else:
                        daily_score_df = daily_score_df.merge(
                                df, left_index=True, right_index=True)
                self.print("评估完成graph_id:%s\n" % graph_id)

            except Exception as e:
                # 回测时报错要返回错误信息
                if len(graphs) == 1:
                    raise e
                self.print("graph_id: %s error %s" % (graph_id, traceback.format_exc()))
            finally:
                evaluate_res.append(evaluate_df)
                score_res.append(score)

        if return_daily_score and not daily_score_df.empty:
            return evaluate_res, score_res, daily_score_df
        else:
            return evaluate_res, score_res


