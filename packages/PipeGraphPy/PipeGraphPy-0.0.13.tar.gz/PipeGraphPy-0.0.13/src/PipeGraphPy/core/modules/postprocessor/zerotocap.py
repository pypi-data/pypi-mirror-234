# coding:utf-8

class ZeroToCap():
    def __init__(self, **kw):
        self.params = kw
        self.farm_info = kw.get('biz_info')

    def transform(self, df):
        assert self.farm_info['powercap'], '场站没有配置装机容量powercap'
        # 取装机容量
        powercap = self.farm_info['powercap']
        # 对预测值处理
        if 'r_apower_predict' in df.columns:
            df.loc[:, 'r_apower_predict'] = df['r_apower_predict'].apply(
                lambda x: 0 if x < 0 else int(
                    powercap) if x > int(powercap) else x
            )
        return df
