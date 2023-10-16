import os
import json
import traceback
import shutil
from datetime import datetime, timedelta
from PipeGraphPy.config import settings
from PipeGraphPy.constants import STATUS, GRAPHTYPE
from PipeGraphPy.db.models import OnlineGraphsPredictRecordTB, PredictRecordTB, GraphsTB

class ReportMengDongEnergyTest():
    __version__ = 'v1.0.1'
    def __init__(self, **kw):
        self.params = kw
        self.instance_id = self.params.get("instance_id")        # 产品实例id
        self.product_id = self.params.get("product_id")          # 产品id
        self.model_ids = self.params.get("model_ids")              # 要上报的模型id
        self.filename = self.params.get("filename")              # 文件名称
        self.replace = self.params.get("replace")                # 是否替换
        self.file_path_code = self.params.get("file_path_code")  # 文件保存路径
        self.log_path_code = "JTAU7E1W"
        self.appcode = self.params.get("appcode")
        self.use_online = 0

    def get_batch_time(self):
        now = datetime.utcnow() + timedelta(hours=8)
        return now.strftime("%Y%m%d0000")

    def write_log(self, files):
        """向天工写日志"""
        now = datetime.utcnow() + timedelta(hours=8)
        date_str = now.strftime("%Y%m%d")
        logpath = "/jtdata/products/data/%s/%s@%s.log" % (self.log_path_code, self.appcode, date_str)
        log_str = json.dumps({
            "appcode": self.appcode,
            "status": 0,
            "time": now.strftime("%Y%m%d%H%M%S%f"),
            "output": {
                "msg": "success",
                "files_list": files,
                "batch_time": now.strftime("%Y%m%d0000"),
                "end_time ": now.strftime("%Y-%m-%d %H:%M:%S"),
                "data": ""
            }
        })
        # with open(logpath, "a+") as f:
        #     f.writelines(log_str+"\n")
        self.print(log_str)
        self.print("写日志成功: %s" % logpath)

    def get_filename(self):
        """文件名称"""
        filepath = self.filename
        filepath = str(filepath).strip()
        now = datetime.utcnow() + timedelta(hours=+8)
        date_year_str = str(now.year + 1) if now.month == 12 else str(now.year)
        date_month_str = "01" if now.month == 12 else str(now.month+1).rjust(2,"0")
        file_date_str = f"{date_year_str}{date_month_str}010000"
        filename = "NPS_%s_%s" % (self.filename, file_date_str)
        return filename

    def gen_target_filepath(self):
        """生成目标文件目录"""
        now = datetime.utcnow() + timedelta(hours=8)
        date_str = now.strftime("%Y%m%d")
        filename = self.get_filename()
        folder_path = "/jtdata/products/data/%s/%s" % (self.file_path_code, date_str)
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
        return datas

    def check_data(self, datas):
        """检查数据是否合理"""
        return datas

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
        assert self.instance_id
        assert self.product_id
        if self.model_ids:
            model_ids = list(map(int, str(self.model_ids).split(",")))
            graph_info = GraphsTB.find(id=("in", model_ids))
        else:
            graph_info = GraphsTB.find(
                    biz_id=self.instance_id,
                    biz_type_code=self.product_id,
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
                    try:
                        # cut_data.to_csv(filepath, encoding="utf_8", index=False)
                        shutil.copy(predict_file, filepath)
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
                # now = datetime.utcnow() + timedelta(hours=8)
                # if now.hour >= 7 and now.minute > 50 and day_num == 0:
                #     self.print("尝试使用前一天的补报")
                # else:
                raise Exception("所有模型都上报失败")

