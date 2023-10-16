# coding:utf-8

import json
import datetime
import pandas as pd
from decimal import Decimal


def replace_json(data):
    """替换json数据

    Example: >>> data = u'[{"rid": "46", "cap": "30000", \
        "nwp_config": {"GFS": "001"}, "layer": "70"}, \
            {"rid": "46", "cap": "30000", \
                "nwp_config": {"GFS": "001"}, "layer": "70"}]'
             >>> replace_json(data)

    Return: >>>
    """

    for k, v in data.items():
        try:
            row = json.loads(v)
            data[k] = row
        except Exception:
            pass

    return data


def binary_to_utf8(data):
    """
    二进制编码转成utf-8编码
    >>> binary_to_utf8(b'example')
    'example'
    >>> binary_to_utf8([b'aa', b'bb', b'cc'])
    ['aa', 'bb', 'cc']
    """
    if isinstance(data, list):
        return [binary_to_utf8(i) for i in data]
    else:
        try:
            return str(data, 'utf-8')
        except Exception:
            return data


def filter_keys(data, keys):
    """
    字典过滤keys
    """
    if isinstance(data, list):
        return [filter_keys(i, keys) for i in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k in keys}
    else:
        return data


def filter_keys_pass(data, keys):
    """
    字典过滤掉keys
    """
    if isinstance(data, list):
        return [filter_keys_pass(i, keys) for i in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k not in keys}
    else:
        return data


#  LOG = logging.getLogger('ATP.WebApi')
#
#  def log(func):
#      """log wrapper"""
#      def wrapper(*args, **kw):
#          try:
#              res = func(*args, **kw)
#              return res
#          except Exception as e:
#              errInfo = '(%s),详细错误:%s'%(func.__name__, e)
#              err_msg = '%s --- 错误代码 --- %s'%(errInfo, traceback.format_exc())
#              LOG.error(err_msg)
#              return json.dumps({'message':'接口异常请联系管理员', 'status':0})
#      return wrapper
#
#  def sql_filter(sql, max_length=1000):
#      dirty_stuff = ["select", "delete", "update", "insert"]
#      for stuff in dirty_stuff:
#          sql = sql.replace(stuff, "")
#      return sql[:max_length]

def pretty_data(obj):
    '''转换数据'''
    if isinstance(obj, float):
        return round(obj, 4)
    elif isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Decimal):
        return round(float(obj), 4)
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, dict):
        return dict((pretty_data(k), pretty_data(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return [pretty_data(i) for i in obj]
    return obj


def format_response(data, index_as_column=False):
    '''格式化rpc和http返回数据, DataFrame转dict'''
    if isinstance(data, pd.DataFrame):
        data = data.where(pd.notnull(data), None)
        if index_as_column:
            data = data.reset_index()
        data = data.to_dict(orient='index')
    return pretty_data(data)


if __name__ == '__main__':
    data = {'algo_param': u'{"C":10, "gamma":20}',
            'region': u'[{"rid": "46", "cap": "30000", "nwp_config": \
                {"GFS": "001"}, "layer": "70"}, {"rid": "46", "cap": \
                    "30000", "nwp_config": {"GFS": "001"}, "layer": "70"}]'}
    replace_json(data)
