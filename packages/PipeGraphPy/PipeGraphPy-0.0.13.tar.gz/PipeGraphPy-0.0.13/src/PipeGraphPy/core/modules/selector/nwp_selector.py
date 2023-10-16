
from itertools import combinations
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectorMixin
import numpy as np
from sklearn.utils.validation import check_array
from sklearn.utils import as_float_array
from PipeGraphPy.utils.examine import matrix_rmse
import pandas as pd


class CFS(TransformerMixin, BaseEstimator):
    def __init__(self):
        """
        This is a simple implementation of CFS(correlation-based feature
        selection) algorithm which used for feature selections, it can
        only handle numeric variables and numeric labels, it will be
        improved later.

        read more about CFS, please visit :
        ref:`https://blog.csdn.net/littlely_ll/article/details/71545929`.
        """
        self._relavent_cols = []
        self._merits = None

    def fit(self, X, y):
        """
        fit an array data

        :param X: a numpy array

        :param y: the label, a list or one dimension array

        :return:
        """
        self.columns = X.columns
        X = check_array(np.array(X))
        y = check_array(np.array(y))
        assert len(X) == len(y), "X and y should have same length!"

        m, n = X.shape

        for i in range(n):
            if np.var(X[:, i]) == 0.0:
                raise ValueError("Column feature should not be zero variance!")
            if isinstance(X[:, i][0], str):
                raise ValueError("It does not support string values yet!")

        correlations = np.corrcoef(X, y, rowvar=False)
        correlations = correlations[:-1, :]

        _max_index = np.argmax(correlations[:, -1])
        self._relavent_cols.append(_max_index)
        self._merits = correlations[_max_index, -1]

        while True:
            _tmp_relavent = []
            tmp_relavent_col = None
            max_merits = float("-inf")

            for i in range(n):
                if i not in self._relavent_cols:
                    _tmp_relavent.extend(self._relavent_cols)
                    _tmp_relavent.append(i)
                    row_ind, col_ind = zip(*combinations(_tmp_relavent, 2))

                    ff_mean = correlations[row_ind, col_ind].mean()
                    fc_mean = correlations[_tmp_relavent, -1].mean()

                    k = len(_tmp_relavent)
                    merits = (k * fc_mean) / np.sqrt(k + k*(k-1)*ff_mean)
                    if merits >= max_merits:
                        max_merits = merits
                        tmp_relavent_col = i

            if max_merits > self._merits:
                self._relavent_cols.append(tmp_relavent_col)
                self._merits = max_merits
            else:
                break
        return self

    def transform(self, X):
        X = check_array(np.array(X))
        X = X[:, self._relavent_cols]
        return X

    @property
    def merits(self):
        return self._merits

    @property
    def important_features(self):
        return self._relavent_cols


class Corr(SelectorMixin, BaseEstimator):
    def __init__(self, corr_thr=None):
        self.corr_thr = corr_thr
        self.select_index = []

    def fit(self, X, y):

        X = check_array(np.array(X))
        y = check_array(np.array(y).reshape(-1, 1))

        m, n = X.shape

        for i in range(n):
            if np.var(X[:, i]) == 0.0:
                raise ValueError("Column feature should not be zero variance!")
            if isinstance(X[:, i][0], str):
                raise ValueError("It does not support string values yet!")

        # correlations = np.corrcoef(X, y, rowvar=False)

        init_col = 0
        self.select_index.append(init_col)
        for i in range(n):
            if i != init_col:
                _corr = np.corrcoef(X[init_col], X[i])
                if _corr < self.corr_thr:
                    self.select_index.append(i)
    # TODO:


class ChooseNwp(SelectorMixin, BaseEstimator):

    def __init__(self, k, stable_weight=0.5) -> None:
        self.k = k
        self.target = 'r_wspd'
        self.stable_weight = stable_weight

    def fit(self, X, y):
        if max(y) > 100:
            raise ValueError("y must be r_wspd !")

        if not isinstance(X, pd.DataFrame):
            raise ValueError(
                "X must be pandas.DataFrame with `dtime` as index !")

        data = pd.concat([X, pd.DataFrame(np.array(y), columns=[
                         self.target], index=X.index)], axis=1)
        day_rmse = []
        for day, day_df in data.groupby(by=lambda x: x.strftime('%Y-%m-%d')):
            day_rmse.append(matrix_rmse(day_df.drop(
                self.target, axis=1).values, day_df[self.target].values))

        # 每天rmse
        day_rmse = pd.DataFrame(day_rmse, columns=X.columns)

        # 每天rmse平均的排名
        day_rmse_avg_rank = day_rmse.mean().rank(ascending=1, method='first')

        # 每天rmse排名的平均
        day_rmse_rank_avg = day_rmse.T.rank(
            ascending=1, method='first').mean(axis=1)

        # 每天rmse排名的平均的排名
        day_rmse_rank_avg_rank = day_rmse_rank_avg.rank(
            ascending=1, method='first')

        df = pd.concat([day_rmse_avg_rank, day_rmse_rank_avg_rank],
                       axis=1).dropna(how='any')

        self.scores_ = (
            (1 / df.iloc[:, 1]).fillna(0) * (
                1 - self.stable_weight) + (
                    1 / df.iloc[:, 0]).fillna(0) * self.stable_weight).values

        return self

    @staticmethod
    def _clean_nans(scores):
        """
        Fixes Issue #1240: NaNs can't be properly compared, so change them to
        the smallest value of scores's dtype. -inf seems to be unreliable.
        """
        # XXX where should this function be called? fit? scoring functions
        # themselves?
        scores = as_float_array(scores, copy=True)
        scores[np.isnan(scores)] = np.finfo(scores.dtype).min
        return scores

    def _get_support_mask(self):
        scores = self._clean_nans(self.scores_)
        mask = np.zeros(scores.shape, dtype=bool)

        # Request a stable sort. Mergesort takes more memory (~40MB per
        # megafeature on x86-64).
        mask[np.argsort(scores, kind="mergesort")[-self.k:]] = 1
        return mask
