# coding: utf8

from PipeGraphPy.constants import DATATYPE
from . import SpecialBase


class EmptyData(SpecialBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [{
        "key": "output_num",
        "name": "输出数量",
        "type": "int",
        "plugin": "input",
        "need": False,
        "value": 1,
        "desc": ""
    }]
    params_rules = {
        'output_num': {
            "name": "输出数据个数",
            'type': int,
            'need': False,
            'range': [1, 4],
        }
    }

    def run(self):
        if self.params.get('output_num') and self.params['output_num'] != 1:
            self.node.OUTPUT = [DATATYPE.DATAFRAME] * int(self.params['output_num'])
        return self.node, self.node.run_result

    def evaluate(self):
        return self.node, self.node.evaluate_result

    def predict(self):
        return self.node, self.node.predict_result
