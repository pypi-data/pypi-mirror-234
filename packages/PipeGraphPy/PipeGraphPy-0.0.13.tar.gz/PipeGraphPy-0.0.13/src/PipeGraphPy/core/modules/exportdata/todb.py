# coding: utf8

from PipeGraphPy.constants import DATATYPE
from PipeGraphPy.constants import DB
from PipeGraphPy.utils.str_handle import filter_fields
from PipeGraphPy.db.utils import df_to_db


class ToDB():
    INPUT = [DATATYPE.DATAFRAME]
    OUTPUT = []
    TEMPLATE = [{
        "key": "dbserver",
        "name": "数据库服务",
        "type": "string",
        "plugin": "select",
        "need": True,
        "value": "179",
        "source": DB.tolist(),
        "desc": ""
    }, {
        "key": "db",
        "name": "库名",
        "type": "string",
        "plugin": "input",
        "need": True,
        "value": "jobs",
        "desc": ""
    }, {
        "key": "table",
        "name": "表名",
        "type": "string",
        "plugin": "input",
        "need": True,
        "value": "schedule_record",
        "desc": ""
    }, {
        "key": "selected_columns",
        "name": "选择的列",
        "type": "string",
        "plugin": "input",
        "need": True,
        "value": "__all__",
        "desc": ""
        # }, {
        #     "key": "if_exists",
        #     "name": "存在则",
        #     "type": "string",
        #     "plugin": "input",
        #     "need": False,
        #     "value": "replace",
        #     "desc": "fail, replace, append, ignore"
    }, {
        "key": "index",
        "name": "索引是否入库",
        "type": "int",
        "plugin": "select",
        "need": True,
        "value": 0,
        "source": [0, 1],
        "desc": "是否保存索引"
    }, {
        "key": "index_label",
        "name": "索引对应列名",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": "dtime",
        "desc": "保存索引时所使用的字段名"
    }]
    params_rules = {
        'dbserver': {
            "name": "数据库服务",
            'type': str,
            'need': True,
            "source": DB.tolist(),
        },
        'db': {
            "name": "库名",
            'type': str,
            'need': True,
        },
        'table': {
            "name": "表名",
            'type': str,
            'need': True,
        },
        'selected_columns': {
            "name": "选择的列",
            'type': str,
            'need': True,
        },
        'index': {
            "name": "索引字段",
            'type': int,
            'need': True,
            "source": [0, 1],
        },
        'index_label': {
            "name": "索引对应列名",
            'type': str,
            'need': False,
        },
    }

    def __init__(self, node, **kw):
        self.node = node
        self.params = kw
        self.params.update(node.params)

    def check_params(self):
        params = self.params
        if params['dbserver'] not in DB.tolist():
            raise Exception('数据库服务必须选(%s)中其中一个' % DB.tolist())
        if params['index'] and not params['index_label']:
            raise Exception('缺少索引对应列名')

    def run(self, df):
        self.check_params()
        selected_columns = df[filter_fields(
            df.columns, self.params['selected_columns'])]
        if self.params['index']:
            df[self.params['index_label']] = df.index
        table = '%s.%s' % (self.params['db'], self.params['table'])
        df_to_db(self.params['dbserver'], table, selected_columns)
        return self.node, None

    def evaluate(self):
        return self.node, None

    def predict(self):
        return self.node, None
