# coding: utf8

import pandas as pd
from PipeGraphPy.constants import DATATYPE
from dbpoolpy import connect_db
from PipeGraphPy.constants import DATABASES_POOL
from . import InputDataBase


class FromDB(InputDataBase):
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
        "key": "fields",
        "name": "字段",
        "type": "string",
        "plugin": "input",
        "need": True,
        "value": "",
        "desc": ""
    }, {
        "key": "where",
        "name": "筛选条件",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": "id in (1196, 1194)",
        "desc": ""
    }, {
        "key": "limit",
        "name": "限制条数",
        "type": "int",
        "plugin": "input",
        "need": True,
        "value": 10000,
        "desc": "限制条数不能太大"
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
        'fields': {
            "name": "字段",
            'type': str,
            'need': True,
        },
        'where': {
            "name": "筛选条件",
            'type': str,
            'need': False,
        },
        'limit': {
            "name": "限制条数",
            'type': int,
            'need': True,
            'range': [1, 100000],
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
        if params['limit'] > 100000:
            self.stop_run('限制条数不能太大, 最大值100000')
        if all([
            params.get('index'),
            params['fields'].strip() != '*',
            params['fields'].find(params['index']) == -1]
        ):
            self.stop_run('所取字段不存包含索引字段')

    def run(self):
        # self.log(l_type='r', level='info', msg='检查参数合理性')
        self.check_params()
        # self.log(l_type='r', level='info', msg='导入数据')
        table = '%s.%s' % (self.params['db'], self.params['table'])
        sql = "select %s from %s" % (self.params['fields'], table)
        if self.params['where']:
            sql += ' where %s' % self.params['where']
        sql += ' limit %s' % self.params['limit']
        with connect_db(self.params['dbserver']) as db:
            data = db.query(sql)
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
