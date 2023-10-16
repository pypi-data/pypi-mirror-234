import json
import traceback
from datetime import datetime, timedelta
from PipeGraphPy.db.models import GraphsTB, MLTConfigTB, NodesTB, WindFarmInfo179TB, ObjectsTB
from PipeGraphPy.db.models import WindFarmInfoTB
from dbpoolpy import connect_db
from PipeGraphPy.logger import rlog
from PipeGraphPy.constants import BIZ_TYPE, STATUS


def get_farm_info(wfid=None, graph_id=None):
    """返电场信息"""
    try:
        if wfid:
            try:
                farm_info = WindFarmInfoTB.find_one(wfid=wfid)
            except:
                farm_info = WindFarmInfo179TB.find_one(wfid=wfid)
            return farm_info
        elif not wfid and graph_id:
            graph_info = GraphsTB.find_one(id=graph_id)
            try:
                farm_info = WindFarmInfoTB.find_one(wfid=graph_info["biz_id"])
            except:
                farm_info = WindFarmInfo179TB.find_one(wfid=graph_info["biz_id"])
            return farm_info
        else:
            raise Exception("传参错误")
    except Exception:
        return None


def update_node_params(node_ids, key, value, value_key="value"):
    """更新节点的params字段信息
    parametes:
        node_ids: list or int 要更新节点的id
        key: str 要更新的键
        value: str 要更新的值
    """
    if isinstance(node_ids, int):
        node_ids = [node_ids]
    elif isinstance(node_ids, list):
        node_ids = node_ids
    else:
        raise Exception("update_node_params函数node_ids字段传值类型不合法")
    for node_id in node_ids:
        node_info = NodesTB.find_one(id=node_id)
        node_params = json.loads(node_info["params"])
        for i in node_params:
            if i["key"] == key:
                i[value_key] = value
                break
        NodesTB.set(params=json.dumps(node_params)).where(id=node_id)


def insert_batch(dbserver, table, datas, num=2000):
    try:
        cnt = 0
        with connect_db(dbserver) as db:
            while len(datas) > cnt:
                ceil_list = datas[cnt : cnt + num]
                db.insert(table).many(ceil_list).execute()
                cnt += num
    except Exception:
        rlog.error(traceback.format_exc())


def df_to_db(dbserver, table, df):
    if df.empty:
        return
    datas = df.to_dict(orient="records")
    insert_batch(dbserver, table, datas)


def get_biz_info(biz_type_code, biz_id):
    """获取业务信息
    参数：
        biz_type_code: 业务类型
        biz_id：业务id
    """
    # biz_type_code_list = BIZ_TYPE.values()
    # if biz_type_code not in biz_type_code_list:
    #     raise Exception("业务类型错误(%s), 需在(%s)中选择" % (biz_type_code, biz_type_code_list))
    if biz_type_code == BIZ_TYPE.WFID:
        return get_farm_info(wfid=biz_id)
    elif biz_type_code == BIZ_TYPE.WEATHER:
        return get_farm_info(wfid=biz_id)
    elif biz_type_code == BIZ_TYPE.MLT_MONTH:
        return get_farm_info(wfid=biz_id)
    elif biz_type_code == BIZ_TYPE.MLT_HOUR:
        return get_farm_info(wfid=biz_id)
    elif biz_type_code == BIZ_TYPE.MONTH_CURVE:
        return get_farm_info(wfid=biz_id)
    elif biz_type_code == BIZ_TYPE.MLT:
        biz_info = MLTConfigTB.find_one(wfid=biz_id)
        return biz_info or {}
    elif biz_type_code == BIZ_TYPE.CUSTOM:
        return {"biz_type_code": biz_type_code, "biz_id": biz_id}
    else:
        biz_info = ObjectsTB.find_one(biz_type_code=biz_type_code, biz_id=biz_id)
        return biz_info if biz_info else {"biz_type_code": biz_type_code, "biz_id": biz_id}

def graphs_wait_to_run(graph_ids):
    """模型进入训练队列"""
    if graph_ids:
        running_ids = GraphsTB.map("id").where(
                status=("in", [STATUS.RUNNING, STATUS.WAITRUN]),
                id=("in",graph_ids))
        if running_ids:
            graph_ids = list(set(graph_ids) - set(running_ids))
        if graph_ids:
            now = (datetime.utcnow()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            GraphsTB.set(
                status=STATUS.WAITRUN,
                wait_run_time=now,
                task_id=''
            ).where(id=("in", graph_ids))

def graphs_wait_to_predict(graph_ids, clock="12", is_pub=False, **kwargs):
    """模型进入预测队列"""
    params = {"clock": clock, "is_pub": is_pub}
    if kwargs:
        params.update(kwargs)
    if graph_ids:
        predicting_ids = GraphsTB.map("id").where(
                p_status=("in", [STATUS.RUNNING, STATUS.WAITRUN]),
                id=("in",graph_ids))
        if predicting_ids:
            graph_ids = list(set(graph_ids) - set(predicting_ids))
        if graph_ids:
            now = (datetime.utcnow()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
            GraphsTB.set(
                p_status=STATUS.WAITRUN,
                predict_params=json.dumps(params),
                wait_predict_time=now,
            ).where(id=("in", graph_ids))
