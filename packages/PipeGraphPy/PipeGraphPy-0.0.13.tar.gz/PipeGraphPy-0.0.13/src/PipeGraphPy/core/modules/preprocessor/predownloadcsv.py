# coding: utf8
"""
文件名可加变量：
    %Y 四位数的年份表示（0000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %M 分钟数（00-59）
    %S 秒（00-59）
    %f Microsecond为十进制数，左侧为零填充。
"""
import os
from datetime import datetime, timedelta
from PipeGraphPy.config import settings

class PreDownloadCSV():
    __version__ = 'v1.1'
    TEMPLATE = [{
        "key": "run_filename",
        "name": "训练数据保存csv文件名",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": "",
        "desc": ""
    },{
        "key": "run_file_down",
        "name": "下载训练保存的csv文件",
        "type": "string",
        "plugin": "run_file_down",
        "need": False,
        "value": "",
        "desc": ""
    },{
        "key": "predict_filename",
        "name": "预测数据保存csv文件名",
        "type": "string",
        "plugin": "input",
        "need": False,
        "value": "",
        "desc": ""
    },{
        "key": "predict_file_down",
        "name": "下载预测保存的csv文件",
        "type": "string",
        "plugin": "predict_file_down",
        "need": False,
        "value": "",
        "desc": ""
        }
    ]
    params_rules = {}

    def __init__(self, **kw):
        self.params = kw

    def check_path(self, filepath):
        "校验路径的合理性"
        if filepath:
            if not str(filepath).endswith(".csv"):
                raise Exception("%s必须以.csv结尾")
            folder_path = os.path.dirname(filepath)
            if not os.path.isdir(folder_path):
                raise Exception("%s路径不存在" % folder_path)

    def trans_date(self, filepath):
        "解析时间变量"
        filepath = str(filepath).strip()
        if filepath.find("%") != -1:
            now = datetime.utcnow() + timedelta(hours=+8)
            replace_str = {
                "%Y": str(now.year),
                "%m": str(now.month).rjust(2,"0"),
                "%d": str(now.day).rjust(2, "0"),
                "%H": str(now.hour).rjust(2, "0"),
                "%M": str(now.minute).rjust(2, "0"),
                "%S": str(now.second).rjust(2, "0"),
                "%f": str(now.microsecond).rjust(6, "0"),
            }
            for k,v in replace_str.items():
                filepath = filepath.replace(k,v)
        return filepath

    def save_csv(self, df, filename, file_type):
        "保存csv文件"
        savepath = settings.TEMP_SAVE_PATH
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        save_filename = "node_%s_%s_%s" % (self.params["node_info"]["id"], file_type, filename)
        filepath = os.path.join(savepath, save_filename)
        filepath = self.trans_date(filepath)
        self.check_path(filepath)
        df.to_csv(filepath)


    def fit_transform(self, df):
        if self.params.get("run_filename"):
            self.save_csv(df, self.params.get("run_filename"), 'run')
        return df

    def transform(self, df):
        if self.params.get("asyn"):
            return df
        if self.params.get("predict_filename"):
            self.save_csv(df, self.params.get("predict_filename"), 'predict')
        return df
