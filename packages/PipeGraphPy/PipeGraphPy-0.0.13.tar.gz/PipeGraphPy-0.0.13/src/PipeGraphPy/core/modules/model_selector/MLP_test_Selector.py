import pandas as pd
import numpy as np


class MLPSelectModel(object):
    def __init__(self, **kw):
        self.select_params = kw

    def fit(self, model_list, X, y):
        try:
            model_rmse_list = []
            for i, model in enumerate(model_list):
                predict_power = model.predict(X)
                train_model_rmse = self.Rmse(y["r_apower"].values, predict_power)
                model_rmse_list.append([i, train_model_rmse])
            model_rmse_list = pd.DataFrame(model_rmse_list)
            print("rmse list>>>>>")
            print(model_rmse_list)
            model_rmse_list.columns = ["key", "rmse"]
            key = model_rmse_list.loc[
                model_rmse_list["rmse"] == model_rmse_list["rmse"].min(), "key"
            ].values
            return model_list[int(key)]
        except Exception:
            pass

    def Rmse(self, obs, pre):
        return np.sqrt(np.mean((obs - pre) ** 2))
