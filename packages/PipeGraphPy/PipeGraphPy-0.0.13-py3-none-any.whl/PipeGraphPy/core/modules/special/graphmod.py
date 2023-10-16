# coding: utf8

import copy
from PipeGraphPy.constants import DATATYPE
from PipeGraphPy import Graph,Node,Module

from . import SpecialBase


class GraphMod(SpecialBase):
    INPUT = []
    OUTPUT = [DATATYPE.OBJECT]
    TEMPLATE = [{
        "key": "graphid",
        "name": "模型id",
        "type": "int",
        "plugin": "input",
        "need": True,
        "value": 1,
        "desc": ""
    }]
    params_rules = {
        'graphid': {
            'type': int,
            'need': True,
        }
    }

    def run(self):
        self.biz_info = self.params.get("biz_info")
        self.graph_info = self.params.get("graph_info")
        graph = Graph(id=self.params["graphid"])
        graphcopy = graph.copy()
        graphcopy.info["biz_info"] = self.biz_info
        graphcopy.run()
        self.node.model = graphcopy
        return self.node, self.node.id

    def evaluate(self):
        return self.node.model.model.get_evaluate_data(**self.params)

    def predict(self, head_res=None, **pred_kw):
        if head_res is not None:
            return self.node, self.node.model.model.predict(head_res, **pred_kw)
        else:
            return self.node, self.node.model.predict()
