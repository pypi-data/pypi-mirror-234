from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class StructToRNNData(TransformerMixin, BaseEstimator):
    """将结构数据转为RNN时间步数据

    Args:
        TransformerMixin ([type]): [description]
        BaseEstimator ([type]): [description]

        steps: 时间窗口
        padding ([type]): 前后补充，使输出和输入数据条数相同
        sampling_rate ([type]): 是否跳步，例如2就是将时间块 [1,2,3,4,5,6] 变为 [1,3,5]
        stride ([type]): 滑动步长
        shuffle ([type]): 是否乱序
        reverse ([type]): 是否反转
        align ([type]): [description]
        future_steps ([type]): 未来时间步长，用X的T+n时刻信息预测预测T时刻
        LSTM2D_ksize ([type]): 转为5D格式，(
            batch, time, channels, LSTM2D_ksize, LSTM2D_ksize)
    """

    def __init__(self, window,
                 padding=True,
                 sampling_rate=1,
                 stride=1,
                 shuffle=False,
                 reverse=False,
                 align=True,
                 future_steps=0,
                 LSTM2D_ksize=0) -> None:

        self.window = window
        self.future_steps = future_steps
        self.padding = padding
        self.sampling_rate = sampling_rate
        self.stride = stride
        self.shuffle = shuffle
        self.reverse = reverse
        self.align = align
        self.y_bias = self.window - 1
        self.window = self.window + self.future_steps
        self.LSTM2D_ksize = LSTM2D_ksize

    def fit(self, X, y):

        self.dim = X.shape[1]
        self.y = y
        return self

    def transform(self, X, y=None):
        if y is None:
            y = np.zeros(len(X))

        if len(self.y) == len(y):
            y = self.y

        if self.padding and self.y_bias > 1:
            X_pad = np.array([np.array(X)[-1]] * self.y_bias)
            y_pad = np.array([y[-1]] * self.y_bias)
            X = np.vstack([X, X_pad])
            y = np.append(y, y_pad)

        self.data_gen = TimeseriesGenerator(X, y, self.window,
                                            sampling_rate=self.sampling_rate,
                                            stride=self.stride,
                                            shuffle=self.shuffle,
                                            reverse=self.reverse,
                                            batch_size=1)

        data, target = self._concat(self.data_gen)

        # target默认往后错开1个时间步长
        if self.align:
            data = np.vstack([data, [data[-1]]])
            target = np.append(y[self.window-1], target)

        if self.future_steps > 0:
            data = np.vstack([data, [data[-1]]*self.future_steps])
            target = np.append(y[self.y_bias:self.window], target)

        if self.LSTM2D_ksize > 0:
            data = data[:len(data)-len(data) % self.window]
            target = target[:len(target)-len(target) % self.window]

            fold = self.window / (self.LSTM2D_ksize ** 2)

            data = data.reshape(
                int(len(data) / fold),
                1,
                self.LSTM2D_ksize,
                self.LSTM2D_ksize,
                data.shape[2])

            # d = []
            # for i in target:
            #     d.append(
            # np.full((1, 1, self.LSTM2D_ksize, self.LSTM2D_ksize, 1), i))
            # target = np.vstack(d)
        return data, target

    def _concat(self, data_iter):
        data = []
        target = []
        for _x, _y in data_iter:
            data.append(_x)
            target.append(_y)
        return np.concatenate(data), np.concatenate(target)
