# coding: utf8
import traceback
import pandas as pd
from PipeGraphPy.db.models import GraphsTB
from PipeGraphPy.storage import store
from PipeGraphPy.utils.examine import rmse
from PipeGraphPy.utils.check import node_is_passed
from PipeGraphPy.db.models.utils import get_farm_info
from PipeGraphPy.constants import GRAPHTYPE
from PipeGraphPy.constants import DATATYPE, MODULES, STATUS
from PipeGraphPy.logger import rlog
from . import SpecialBase


class Evaluate(SpecialBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "metrics",
            "name": "评估指标",
            "type": "string",
            "plugin": "select",
            "need": True,
            "value": "rmse",
            "source": ["rmse"],
            "desc": "使用方法",
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
    ]
    params_rules = {
        "metrics": {
            "name": "评估指标",
            "type": str,
            "need": True,
            "source": ["rmse"],
        },
        "label_columns": {
            "name": "标签列",
            "type": list,
            "need": True,
            "source": ["r_apower"],
        },
    }

    def __init__(self, node, **kw):
        SpecialBase.__init__(self, node, **kw)
        self.graph_info = GraphsTB.find_one(id=node.info["graph_id"])
        self.farm_info = get_farm_info(self.graph_info.get("biz_id"))
        self.theory_score = 50

    def update_score(self, graph_id, score):
        GraphsTB.set(score=round(float(score), 3)).where(id=graph_id)

    def _evaluate_by_rmse(self, pg_list):
        """rmse评估模型"""
        rmse_list = []
        predict_res_list = list()
        for i, pg in enumerate(pg_list):
            # 获取评估数据
            try:
                evaluate_data = pg.get_evaluate_data()
                head_res = {i: j[0] for i, j in evaluate_data.items()}
                # 取y值
                all_y = [
                    i[self.node.params.get("label_columns")] for i in head_res.values()
                ]
                y = all_y[0]
                y.append(all_y[1:], ignore_index=True)
                # 预测
                predict_res = pg.run(head_res=head_res, is_predict=True)
                # 取出预测结果
                predict_label = [
                    i + "_predict" for i in self.node.params.get("label_columns")
                ]
                # 拼接实测值
                predict_df = predict_res[predict_label]
                for i in self.node.params.get("label_columns"):
                    if i in y.columns:
                        predict_df[i] = y[i]
                # rmse
                if self.farm_info.get("powercap"):
                    rmse_value = rmse(
                        predict_res[predict_label].values,
                        y.values,
                        cap=int(self.farm_info["powercap"]),
                    )
                    # 更新分数
                    self.update_score(pg.graph_id, rmse_value)
                    rmse_list.append([pg.estor.id, rmse_value])
                else:
                    GraphsTB.add_log(self.node.info["graph_id"], "场站不存在装机容量，无法评分")
                    rmse_list.append([pg.estor.id, 0])
                # 返回值列名重命名
                predict_res = predict_res.rename(
                    columns={i: str(pg.graph_id) + "_" + i for i in predict_res.columns}
                )
                predict_res_list.append(predict_res)
            except Exception:
                rlog.error(traceback.format_exc(), graph_id=self.node.info["graph_id"])
        # 排序
        rmse_list.sort(key=lambda x: x[1])
        return predict_res_list, rmse_list

    def get_graph_ids(self):
        """获取评估模型同一实体下所有已训练完的图"""
        if not self.graph_info.get("biz_id"):
            raise Exception("该评估模型%s没有配置实体" % self.graph_info.get("id"))
        model_graph_info = GraphsTB.find(
            userid=self.graph_info.get("userid"),
            biz_id=self.graph_info.get("biz_id"),
            biz_type_code=self.graph_info.get("biz_type_code"),
            status=STATUS.SUCCESS,    # 训练不成功的，只要有上一个训练模型存在，就能评分
            available=1,
            category=GRAPHTYPE.TRAIN,
        )
        # 验证模型是否可用来评估
        model_graph_info = list(
            filter(lambda x: store.has_graph(x["id"]), model_graph_info)
        )
        if not model_graph_info:
            raise Exception("该实体下没有可用来评估的训练成功的模型")
        return [i["id"] for i in model_graph_info]

    def run(self):
        self.check_params()
        graph_ids = self.get_graph_ids()
        predict_data = pd.DataFrame()
        scores = list()
        for graph_id in graph_ids:
            graph_model = store.load_graph(graph_id)
            if self.node.params.get("show_passed"):
                pg_list = graph_model.multi_pg
            else:
                pg_list = [
                    graph_model.multi_pg.get(i)
                    for i in graph_model.estimator_set
                    if not node_is_passed(i)
                ]
            if len(pg_list) > 1:
                raise Exception("训练好的算法只能剩下一个,目前(%s)" % len(pg_list))
            if len(pg_list) == 0:
                raise Exception("不存在训练好的算法, 不能预测")

            # 理论功率模型直接赋分值
            if pg_list[0].head_list[0].module.info["cls_name"] == MODULES.THEORYDATA:
                self.update_score(graph_id, self.theory_score)
                continue

            # 根据不同的评估指标指行不同的评估方法
            if self.node.params.get("metrics").lower() == "rmse":
                predict_res_list, rmse_list = self._evaluate_by_rmse(pg_list)

            # 判断是否是有一个输出
            if len(predict_res_list) == 1:
                scores.append(rmse_list[0][1])
                if predict_data.empty:
                    predict_data = predict_res_list[0]
                else:
                    predict_data = predict_data.merge(
                        predict_res_list[0],
                        left_index=True,
                        right_index=True,
                        how="outer",
                    )
            else:
                continue
                # raise Exception('评估过程报错')
                # predict_data[graph_id]=(predict_res_list, rmse_list)
        # score_df = pd.DataFrame(scores, columns=['score'], index=graph_ids)
        # self.node.run_result=predict_data
        # rmse_df = pd.DataFrame(rmse_list, columns=['node_id', 'rmse'])
        return self.node, predict_data

    def predict(self, df):
        return self.node, df
