# coding: utf8

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PipeGraphPy.constants import FARMTYPE
from PipeGraphPy.constants import DATATYPE
from PipeGraphPy.config import settings
from . import AlgodataBase
from PipeGraphPy.logger import plog

nwp_order = ["EC", "CMA", "GFS", "MIX", "METE", "SUP", "OPT"]

class TheoryData(AlgodataBase):
    INPUT = []
    OUTPUT = [DATATYPE.DATAFRAME]
    TEMPLATE = [
        {
            "key": "nwp_config",
            "name": "预测数据气象源",
            "type": "string",
            "plugin": "input",
            "need": True,
            "value": "{'EC':['001'],'CMA':['001'],'GFS':['001'],'METE':['001'],'SUP':['001'],'MIX':['001'],'OPT':['001']}",
            "desc": "字段说明",
        },
    ]
    params_rules = {
        "nwp_config": {
            "name": "预测数据气象源",
            "type": dict,
            "need": True,
        },
    }

    def get_theorydata(self):
        if self.farm_info["f_type"] == FARMTYPE.WIND:
            def func(speed, cap):
                return cap / (1 + 164 * np.exp(-0.6 * speed))
            tx = np.random.uniform(0, 20, 1000)
            ty = func(tx, int(self.farm_info['powercap']))
            noise = np.random.rand(len(
                tx)) * int(self.farm_info['powercap']) / 20 - 0.5 * int(self.farm_info['powercap']) / 20
            ty = ty + noise
            tho = pd.DataFrame(tx, columns=['speed'])
            tho.insert(1, 'power', ty)
            return tho
        elif self.farm_info["f_type"] == FARMTYPE.PV:
            csv_path = os.path.join(
                settings.HOME_PATH, "PipeGraphPy/theory_curve/theory_curve_pv.csv"
            )
            if not os.path.isfile(csv_path):
                raise Exception(f"理论曲线文件不存在:{csv_path}")
            cur = pd.read_csv(csv_path)
            noise = np.random.rand(len(cur)) * 2000
            cur['power'] = cur['power'].values + noise
            cur['power'] = cur['power'].values * int(self.farm_info['powercap']) / 30000
            return cur
        else:
            raise Exception("电场类型错误")

    def run(self):
        theorydata = self.get_theorydata()
        if self.farm_info["f_type"] == FARMTYPE.WIND:
            theory_df = theorydata.rename(
                columns={
                    theorydata.columns[0]: "theory_wspd_70_001",
                    theorydata.columns[1]: "r_apower",
                }
            )
        elif self.farm_info["f_type"] == FARMTYPE.PV:
            theory_df = theorydata.rename(
                columns={
                    theorydata.columns[0]: "theory_ghi_sfc_001",
                    theorydata.columns[1]: "r_apower",
                }
            )
        else:
            theory_df = pd.DataFrame()
        return theory_df

    def evaluate(self):
        return self.run()

    def predict(self):
        aim_date = (datetime.utcnow()+timedelta(hours=8)).strftime("%Y%m%d")
        nwp_data = pd.DataFrame()
        for nwp in nwp_order:
            if self.params["nwp_config"].get(nwp):
                try:
                    nwp_data = self._gen_predict_data_opt(
                            nwp_config={nwp:self.params["nwp_config"].get(nwp)},
                            feature=self.feature,
                            clock=self.params.get("clock", "12"),
                            pub_date=aim_date
                            )
                    if nwp_data.empty:
                        continue
                    break
                except Exception as e:
                    plog.info(str(e))
        if nwp_data.empty:
            raise Exception("所有气象源均无数据%s失败" % self.params["nwp_config"])
        if self.farm_info["f_type"] == FARMTYPE.WIND:
            nwp_data = nwp_data.rename(
                columns={nwp_data.columns[0]: "theory_wspd_70_001"}
            )
        elif self.farm_info["f_type"] == FARMTYPE.PV:
            nwp_data = nwp_data.rename(
                columns={nwp_data.columns[0]: "theory_ghi_sfc_001"}
            )
        else:
            nwp_data = pd.DataFrame()
        return nwp_data
