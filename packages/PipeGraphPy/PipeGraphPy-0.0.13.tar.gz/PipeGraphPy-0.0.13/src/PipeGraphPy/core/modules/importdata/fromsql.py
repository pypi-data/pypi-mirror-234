# coding: utf8

import pandas as pd
from PipeGraphPy.constants import DATATYPE
from dbpoolpy import connect_db
from PipeGraphPy.constants import DATABASES_POOL
from . import InputDataBase


class FromSQL(InputDataBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [{
        "key": "dbserver",
        "name": "数据库服务",
        "type": "string",
        "plugin": "select",
        "need": True,
        "value": "179",
        "source": list(DATABASES_POOL.keys()),
        "desc": ""
    }, {
        "key": "sql",
        "name": "sql",
        "type": "string",
        "plugin": "text",
        "need": True,
        "value": "select * from PipeGraphPy.custom where mod_id=20",
        "desc": ""
    }, {
        "key": "index",
        "name": "索引字段",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": '',
        "desc": ""
    }]
    params_rules = {
        'dbserver': {
            "name": "数据库服务",
            'type': str,
            'need': True,
            "source": list(DATABASES_POOL.keys()),
        },
        'sql': {
            "name": "sql",
            'type': str,
            'need': True,
        },
        'index': {
            "name": "索引字段",
            'type': str,
            'need': False,
        },
    }

    def __init__(self, **kw):
        InputDataBase.__init__(self, **kw)

    def check_params(self):
        params = self.params
        if DATABASES_POOL.get(params['dbserver']) is None:
            self.stop_run('数据库服务值错误：[%s]' % list(DATABASES_POOL.keys()))
        # if not isinstance(params['where'], dict):
        #     self.stop_run('筛选条件必须是json')

    def run(self):

        # self.log(l_type='r', level='info', msg='检查参数合理性')
        self.check_params()
        # self.log(l_type='r', level='info', msg='导入数据')
        with connect_db(self.params['dbserver']) as db:
            data = db.query(self.params['sql'])
        if data:
            df = pd.DataFrame(data)
            if self.params.get('index'):
                df.set_index(self.params['index'])
        else:
            df = pd.DataFrame()
        # self.log(l_type='r', level='info', msg='导入数据成功')
        return df

    def evaluate(self):
        return self.run()

    def predict(self):
        self.stop_run('此模块无法执行预测')
