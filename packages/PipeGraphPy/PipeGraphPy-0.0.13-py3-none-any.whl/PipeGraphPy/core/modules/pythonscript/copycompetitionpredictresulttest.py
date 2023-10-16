import os
import json
import traceback
import pandas as pd
from datetime import datetime, timedelta
from PipeGraphPy.config import settings
from PipeGraphPy.constants import STATUS, GRAPHTYPE
from PipeGraphPy.db.models import OnlineGraphsPredictRecordTB, PredictRecordTB, GraphsTB

class CopyCompetitionPredictResultTest():
        __version__ = 'v1.0.7'
    def __init__(self, **kw):
        self.params = kw
        report_order = self.params.get("report_order")
        self.replace = self.params.get("replace")
        if report_order == "point1_power":
            ##### 比赛风功率
            self.biz_id = "d21849c986a14bbbab8f0c9d54cd988d"
            self.biz_type_code = "1ae4ead5f29612cbc938d743079842d4"
            self.graph_ids = []
            self.file_element = "PG"
            self.file_scope = "POINT1"
            self.pred_column = "power"
            self.batch_str = "_point1_pg"
        elif report_order == "point2_power":
            ##### 比赛光伏功率
            self.biz_id = "4bf37a3c739f4656b4ed07f7b33bef3d"
            self.biz_type_code = "1ae4ead5f29612cbc938d743079842d4"
            self.graph_ids = []
            self.file_element = "PG"
            self.file_scope = "POINT2"
            self.pred_column = "power"
            self.batch_str = "_point2_pg"
        elif report_order == "point1_ws":
            ##### 比赛风订正
            self.biz_id = "d21849c986a14bbbab8f0c9d54cd988d"
            self.biz_type_code = "e3e5fbf156fa57766e76002395489236"
            self.graph_ids = []
            self.file_element = "WS"
            self.file_scope = "POINT1"
            self.pred_column = "ws"
            self.batch_str = "_point1_ws"
        elif report_order == "point2_ns":
            ##### 比赛光伏订正
            self.biz_id = "4bf37a3c739f4656b4ed07f7b33bef3d"
            self.biz_type_code = "e3e5fbf156fa57766e76002395489236"
            self.graph_ids = []
            self.file_element = "NS"
            self.file_scope = "POINT2"
            self.pred_column = "swDown"
            self.batch_str = "_point2_ns"
        elif report_order == "point3_power":
            ##### 比赛贵州风功率
            self.biz_id = "3f66219068414c6ab06cdd538a3e456c"
            self.biz_type_code = "1ae4ead5f29612cbc938d743079842d4"
            self.graph_ids = []
            self.file_element = "PG"
            self.file_scope = "POINT3"
            self.pred_column = "power"
            self.batch_str = "_point3_pg"
        elif report_order == "point4_power":
            ##### 比赛贵州光伏功率
            self.biz_id = "d0f98cfd863a4d398bc77d671e7d01a7"
            self.biz_type_code = "1ae4ead5f29612cbc938d743079842d4"
            self.graph_ids = []
            self.file_element = "PG"
            self.file_scope = "POINT4"
            self.pred_column = "power"
            self.batch_str = "_point4_pg"
        elif report_order == "point3_ws":
            ##### 比赛贵州风订正
            self.biz_id = "3f66219068414c6ab06cdd538a3e456c"
            self.biz_type_code = "e3e5fbf156fa57766e76002395489236"
            self.graph_ids = []
            self.file_element = "WS"
            self.file_scope = "POINT3"
            self.pred_column = "ws"
            self.batch_str = "_point3_ws"
        elif report_order == "point4_ns":
            ##### 比赛贵州光伏订正
            self.biz_id = "d0f98cfd863a4d398bc77d671e7d01a7"
            self.biz_type_code = "e3e5fbf156fa57766e76002395489236"
            self.graph_ids = []
            self.file_element = "NS"
            self.file_scope = "POINT4"
            self.pred_column = "swDown"
            self.batch_str = "_point4_ns"
        self.log_code = "JTAU7E1W"
        self.file_code = "JTYVI51P"
        self.appcode = "f57f96b4-20c6-4584-a9f2-cb301bca43ed"
        self.file_company_code = "HFJT-QX"
        self.file_time_len = "072"
        self.use_online = 0

    def write_log(self, files):
        """向天工写日志"""
        now = datetime.utcnow() + timedelta(hours=8)
        date_str = now.strftime("%Y%m%d")
        logpath = "/jtdata/products/data/%s/%s@%s.log" % (self.log_code, self.appcode, date_str)
        log_str = json.dumps({
            "appcode": "f57f96b4-20c6-4584-a9f2-cb301bca43ed",
            "status": 0,
            "time": now.strftime("%Y%m%d%H%M%S%f"),
            "output": {
                "msg": "success",
                "files_list": files,
                "batch_time": now.strftime("%Y%m%d0800") + self.batch_str,
                "end_time ": now.strftime("%Y-%m-%d %H:%M:%S"),
                "data": ""
            }
        })
        with open(logpath, "a+") as f:
            f.writelines(log_str+"\n")
        self.print("写日志成功: %s" % logpath)

    def gen_target_filepath(self):
        """生成目标文件目录"""
        now = datetime.utcnow() + timedelta(hours=8)
        date_str = now.strftime("%Y%m%d")
        report_start_time = (now+timedelta(days=1)).strftime("%Y%m%d000000")
        filename = "MSP3_%s_WSDP1_%s_LNO_%s_%s_00000-%s15.csv" % (
                self.file_company_code,
                self.file_element,
                self.file_scope,
                report_start_time,
                self.file_time_len
                )
        folder_path = "/jtdata/products/data/%s/%s" % (self.file_code, date_str)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return os.path.join(folder_path, filename)

    def gen_predict_filepath(self, graph_id, day_num):
        """生成预测文件目录"""
        now = datetime.utcnow() + timedelta(hours=8)
        start_time = (now-timedelta(days=day_num)).strftime("%Y-%m-%d")
        end_time = (now-timedelta(days=day_num)+timedelta(days=1)).strftime("%Y-%m-%d")
        file_folder = os.path.join(settings.PREDICT_RESULT_SAVE_PATH, str(graph_id))
        # 取今天最新的预测成功的记录
        if self.use_online:
            tb = OnlineGraphsPredictRecordTB
        else:
            tb = PredictRecordTB
        predict_records = tb.select().where(
            graph_id=graph_id,
            status=STATUS.SUCCESS,
            ctime=("between", (start_time, end_time))
        ).order_by("ctime desc").all()
        if not predict_records:
            self.print("模型：%s (%s, %s)没有预测记录" % (graph_id, start_time, end_time))
            return None
        if not os.path.exists(file_folder):
            self.print("模型：%s 模型预测目录不存在" % graph_id)
            return None
        for record in predict_records:
            record_id = record["id"]
            file_name_prefix = "online_predict_%s_" % record_id if self.use_online else "predict_%s_" % record_id
            file_list = []
            for _file in os.listdir(file_folder):
                if _file.find(file_name_prefix) != -1:
                    file_list.append(os.path.join(file_folder, _file))
            if not file_list:
                continue
            if len(file_list)>1:
                continue
            filepath = file_list[0]
            return filepath
        else:
            self.print("模型：%s (%s, %s)未找到预测文件" % (graph_id, start_time, end_time))
            return None

    def cut_data(self, datas):
        """数据截取"""
        now = datetime.utcnow() + timedelta(hours=8)
        start_time = pd.to_datetime((now+timedelta(days=1)).strftime("%Y-%m-%d"))
        end_time = pd.to_datetime((now+timedelta(days=4)).strftime("%Y-%m-%d"))
        cut_datas = datas[(datas["time"]>=start_time)&(datas["time"]<=end_time)].sort_values("time")
        return cut_datas

    def check_data(self, datas):
        """检查数据是否合理"""
        # 检查长度
        if len(datas) != 289:
            raise Exception("数据长度不是%s, 预测文件数据长度为: %s)"  % (289, len(datas)))

        # 检查预测结果是否存在负值
        if sum(datas.iloc[:,1]<0) > 0:
            raise Exception("预测结果存在负值")

    def run(self):
        # 模型按评分排序
        filepath = self.gen_target_filepath()
        if os.path.isfile(filepath):
            if self.replace == "1":
                self.print("文件已经存在:%s, 执行替换" % filepath)
                os.remove(filepath)
            else:
                self.print("文件已经存在:%s" % filepath)
                return
        if self.graph_ids:
            graph_info = GraphsTB.find(id=("in", self.graph_ids))
        else:
            graph_info = GraphsTB.find(
                    biz_id=self.biz_id,
                    biz_type_code=self.biz_type_code,
                    status=STATUS.SUCCESS,
                    category=GRAPHTYPE.TRAIN)
        graph_sort = sorted(graph_info, key=lambda x: x["score"], reverse=True)
        # 上报使用最近两天的
        for day_num in range(2):
            for g in graph_sort:
                try:
                    # 获取预测文件路径
                    predict_file = self.gen_predict_filepath(g["id"], day_num)
                    if not predict_file:
                        self.print("模型：%s 未获取预测文件" % g["id"])
                        continue
                    # 读取预测数据
                    predict_datas = pd.read_csv(predict_file, parse_dates=["time"])
                    predict_datas.columns = ["time", self.pred_column]
                    # 数据剪切
                    cut_data = self.cut_data(predict_datas)
                    # 保存数据到目标目录
                    cut_data["time"] = cut_data["time"].dt.strftime("%Y%m%d%H%M%S")
                    # 检查数据合理性
                    self.check_data(cut_data)
                    # 保留3位小数
                    # cut_data.iloc[:,1] = cut_data.iloc[:,1].apply(lambda x: round(x, 3))
                    try:
                        cut_data.to_csv(filepath, encoding="utf_8", index=False)
                        # 判断目标文件夹是否已经有文件
                        if os.path.isfile(filepath):
                            self.print("模型：%s 生成预测文件成功 %s" % (g["id"], filepath))
                        else:
                            self.print("模型：%s 生成预测文件失败 %s" % g["id"])
                            continue
                        # 写天工日志：
                        self.write_log([filepath])
                    except:
                        if os.path.isfile(filepath):
                            self.print("模型：%s 文件生成成功 写日志失败" % g["id"])
                            os.remove(filepath)
                        else:
                            self.print("模型：%s 文件生成失败" % g["id"])
                        continue
                    return True
                except Exception as e:
                    self.print("模型: %s 报错\n %s" % (g["id"], traceback.format_exc()))
            else:
                now = datetime.utcnow() + timedelta(hours=8)
                if now.hour >= 7 and now.minute > 50 and day_num == 0:
                    self.print("尝试使用前一天的补报")
                else:
                    raise Exception("所有模型都上报失败")
