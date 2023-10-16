import os
import pandas as pd
# import algo_data as ad
from datetime import datetime, timedelta
ad = None
import json


def parse_json(one_json, time_delta):
    with open(one_json, 'r') as load_f:
        try:
            load_json = json.load(load_f)
        except:
            raise Exception("%s读取报错" % load_f.name)
        predict_power_data = load_json['TransData']['DataBody']['PredictPowerDatas']['PredictPowerData'][0]['DataRecord']

        df_power = pd.DataFrame(predict_power_data)
        ptime_power = pd.to_datetime(df_power['datetime']) + time_delta
        predict_power = df_power['PredictPower']
        predict_theory_power = df_power['PredictTheoryPower']
        wfid = one_json.split('/')[-2].split('_')[-1]
        gid = load_json['TransData']['DataBody']['GID']

        predict_weather_data = load_json['TransData']['DataBody']['PredictWeatherDatas']['PredictWeatherData'][0]['DataRecord']
        df_weather = pd.DataFrame(predict_weather_data)
        ptime_weather = pd.to_datetime(df_weather['datetime']) + time_delta
        wspd = df_weather['wspd_70']
        mark = one_json.split('_')[-1][8:10]
        rain_sfc = df_weather['rain_sfc']
        snow_sfc = df_weather['snow_sfc']
        tskin_sfc = df_weather['tskin_sfc']
        clflo_sfc = df_weather['clflo_sfc']
        ghi_sfc = df_weather['ghi_sfc']
        p_70 = df_weather['p_70']
        t_70 = df_weather['t_70']
        wdir_70 = df_weather['wdir_70']
        rh_70 = df_weather['rh_70']
        rhoair_70 = df_weather['rhoair_70']
        clfmi_sfc = df_weather['clfmi_sfc']
        clfhi_sfc = df_weather['clfhi_sfc']

        power_data = {'ptime': ptime_power, 'wfid': wfid, 'gid': gid, 'predict_power': predict_power,
                      'PredictTheoryPower': predict_theory_power}
        weather_data = {'ptime': ptime_weather, 'wspd': wspd, 'mark': mark,
                        'rain_sfc': rain_sfc, 'snow_sfc': snow_sfc, 'tskin_sfc': tskin_sfc, 'clflo_sfc': clflo_sfc,
                        'ghi_sfc': ghi_sfc, 'p_70': p_70, 't_70': t_70, 'wdir_70': wdir_70, 'rh_70': rh_70,
                        'rhoair_70': rhoair_70, 'clfmi_sfc': clfmi_sfc, 'clfhi_sfc': clfhi_sfc}
        power_dataframe = pd.DataFrame(power_data, columns=['ptime', 'wfid', 'gid', 'predict_power', 'PredictTheoryPower'])
        weather_dataframe = pd.DataFrame(weather_data, columns=['ptime', 'wspd', 'mark', 'rain_sfc', 'snow_sfc',\
                                       'tskin_sfc', 'clflo_sfc', 'ghi_sfc', 'p_70', 't_70', 'wdir_70', 'rh_70', 'rhoair_70',\
                                       'clfmi_sfc', 'clfhi_sfc'])

        file_dt = one_json.split('_')[-1].split('.')[0][:-2]
#         timeStart = (datetime.strptime(file_dt, '%Y%m%d')+ timedelta(days=2)).strftime('%Y-%m-%d') + ' ' + '00:00:00'
#         timeEnd = (datetime.strptime(file_dt, '%Y%m%d')+ timedelta(days=2)).strftime('%Y-%m-%d') + ' ' + '23:45:00'

#         power_dataframe = power_dataframe[(power_dataframe['ptime'] >= timeStart) & (power_dataframe['ptime'] <= timeEnd)]
        # weather_dataframe = weather_dataframe[(weather_dataframe['ptime'] >= timeStart) & (weather_dataframe['ptime'] <= timeEnd)]
        dataframe = pd.merge(power_dataframe,  weather_dataframe, on='ptime', how='inner')
        return dataframe

def select_today_json(cids, last_day, clock, publish_path):
    """
    选择json文件,这里的逻辑比较绕，举例说明:
    1) 2019/09/19 08:00这个时刻的预测功率,记录在20190917.json这个文件里
    并且是文件里2019/09/19 00:00这个时刻对应的数据
    2) 每天需要入库的是明天的数据,即2018/09/19这天要入库的是2018/09/20的
    数据,因此应该选择的文件是20180918.json
    """
    task_list = []
    cid_dict = os.listdir(publish_path)

    for filesInCid in cid_dict:
        if filesInCid in cids:
            root_path = os.path.join(publish_path, filesInCid)
            file_names = os.listdir(root_path)
            for jsonFileName in file_names:
                if jsonFileName.split('.')[-1] == 'json':
                    if last_day and (jsonFileName.split('_')[-1].split('.')[0][:-2]==last_day) and (jsonFileName.split('_')[-1].split('.')[0][-2:]==str(clock)):
                        jsonsize = os.path.getsize(root_path+'/'+jsonFileName)
                        if (os.path.exists(root_path+'/'+jsonFileName)) & (jsonsize>10000):
                            task_list.append((filesInCid, root_path+'/'+jsonFileName))
    return task_list

def get_jsondata(dispatch_name, f_type, clock, publish_path):
    info_w = ad.farm_info(dispatch_name=dispatch_name, dtype='df', f_type=f_type)
    cids = info_w['cid'].values

    last_day= ((datetime.utcnow()+timedelta(hours=8)) + timedelta(days=-1)).strftime('%Y%m%d')
    file_path = select_today_json(cids, last_day, clock, publish_path)
    time_delta = timedelta(hours=8)  # 加8小时否？

    # 整合功率值
    allpower = []
    for cid_file in file_path:
        df = parse_json(cid_file[1], time_delta)
        df_power = df[['ptime', 'predict_power']]
        df_power['predict_power'] = df_power['predict_power'].astype('float')
        df_power = (df_power.rename(
                columns={
                    'ptime':'dtime',
                    'predict_power': "p_apower_"+str(cid_file[0]).split('_')[-1]}
                )
                .set_index('dtime'))
        allpower.append(df_power)
    allpower = pd.concat(allpower, axis=1).fillna(0)
    return allpower
