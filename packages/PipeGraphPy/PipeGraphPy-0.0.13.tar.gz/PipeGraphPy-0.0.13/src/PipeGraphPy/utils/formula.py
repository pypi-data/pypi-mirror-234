import numpy as np


def rmse(obs, pre):
    return np.sqrt(np.mean((obs - pre)**2))
