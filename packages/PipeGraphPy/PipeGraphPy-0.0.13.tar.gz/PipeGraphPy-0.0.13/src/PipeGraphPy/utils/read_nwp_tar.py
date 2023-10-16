
import os
import tarfile
import pandas as pd
import algo_data as ad
from datetime import date
from PipeGraphPy.config import settings

CORRECT_NWP_SOURCE = {"GRIDAI", "ECENSAI", "METE", "SUP", "PVS"}

if settings.IS_AWS_BAK:
    NWP_FILEPATH = "/mnt/correct/NWP_ZY_backup/{weather_source}/{wfid}/"
else:
    NWP_FILEPATH = "/mnt/sources/NWP_ZY/{weather_source}/{wfid}/"
TAR_FILENAME = "farm_{wfid}_{nwp_start_time}.tar.gz"
CORRECT_TAR_FILENAME = 'stn_{stn_id}_farm_{wfid}_{nwp_start_time}.tar.gz'
CSV_FILENAME = "stn_{stn_id}_farm_{wfid}_{nwp_start_time}.csv"

"""
文件格式
文件路径：/mnt/correct/NWP_ZY/{wfid}/
气象tar包文件的格式：farm_{wfid}_{nwp_start_time}.tar.gz；
csv的文件名格式：stn_{stn_id}_farm_{wfid}_{nwp_start_time}.csv
"""

drop_columns = ['datetime']


def pubdate2nwp_start_time(weather_source, pub_date, clock):
    time_mapper = ad.WeatherRT.gen_nwp_file_time(pub_date)
    if weather_source in ['CONWX', 'ML', 'MF', 'XZ']:
        nwp_start_time = time_mapper[weather_source][clock]
    else:
        nwp_start_time = time_mapper['ORI'][clock]
    return nwp_start_time


def read_nwp_tar(wfid, weather_source, stn_id, pub_date, clock):
    """
    读取气象tar文件中的气象数据
    params:
        wfid: str 场站id
        weather_source: str 气象源
        stn_id: 坐标id
        pub_date: 要发布的日期
        clock: 气象文件时刻标识: 00或12
    return:
        DataFrame 文件内的气象数据
    """
    nwp_start_time = pubdate2nwp_start_time(weather_source, pub_date, clock)
    if weather_source in CORRECT_NWP_SOURCE:
        tar_filename = CORRECT_TAR_FILENAME.format(
                stn_id=stn_id, wfid=wfid, nwp_start_time=nwp_start_time)
    else:
        tar_filename = TAR_FILENAME.format(wfid=wfid, nwp_start_time=nwp_start_time)
    csv_filename = CSV_FILENAME.format(stn_id=stn_id, wfid=wfid, nwp_start_time=nwp_start_time)
    tar_path = NWP_FILEPATH.format(weather_source=weather_source, wfid=wfid)
    tar_filepath = os.path.join(tar_path, tar_filename)
    if not os.path.exists(tar_filepath):
        raise FileExistsError('tar文件 %s 不存在' % tar_filepath)
    tar = tarfile.open(tar_filepath, "r:gz")
    tar_file_list = tar.getnames()
    if csv_filename not in tar_file_list:
        raise FileExistsError("csv 文件%s不在tar包文件%s里" % (csv_filename, tar_filepath))
    try:
        nwp_data = pd.read_csv(tar.extractfile(csv_filename))
        for i in drop_columns:
            if i in nwp_data.columns:
                nwp_data.drop(columns=i, inplace=True)
        return nwp_data
    except:
        raise IOError("%s,%s数据读取出错，检查csv格式" % (csv_filename, tar_filepath))


if __name__ == "__main__":
    nwp_df = read_nwp_tar(
        wfid="652243",
        weather_source="MIX",
        stn_id="001",
        # pub_date=date.today().strftime("%Y%m%d"),
        pub_date="20220417",
        clock="12"
    )
    print(nwp_df)
