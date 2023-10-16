from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
import numpy as np
import warnings
import random


class MRMR(BaseEstimator, TransformerMixin):
    def __init__(self, feature_num):
        """
        mRMR is a feature selection which maximises the 
        feature-label correlation and minimises the feature-feature 
        correlation. this implementation can only applied 
        for numeric values, read more about mRMR, please 
        refer :ref:
        `https://blog.csdn.net/littlely_ll/article/details/71749776`.

        :param feature_num: selected number of features
        """
        self.feature_num = feature_num
        self._selected_features = []

    def fit(self, X, y):
        """
        fit an array data

        :param X: a numpy array

        :param y: the label, a list or one dimension array

        :return:
        """
        X = check_array(X)
        y = check_array(y)
        assert X.shape[0] == len(y), "X and y not in the same length!"

        if self.feature_num > X.shape[1]:
            self.feature_num = X.shape[1]
            warnings.warn(
                "The feature_num has to be set less or equal to {}"
                .format(X.shape[1]), UserWarning)

        MIs = self.feature_label_MIs(X, y)
        max_MI_arg = np.argmax(MIs)

        selected_features = []

        MIs = list(zip(range(len(MIs)), MIs))
        selected_features.append(MIs.pop(int(max_MI_arg)))

        while True:
            max_theta = float("-inf")
            max_theta_index = None

            for mi_outset in MIs:
                ff_mis = []
                for mi_inset in selected_features:
                    ff_mi = self.feature_feature_MIs(
                        X[:, mi_outset[0]], X[:, mi_inset[0]])
                    ff_mis.append(ff_mi)
                theta = mi_outset[1] - 1 / len(selected_features) * sum(ff_mis)
                if theta >= max_theta:
                    max_theta = theta
                    max_theta_index = mi_outset
            selected_features.append(max_theta_index)
            MIs.remove(max_theta_index)

            if len(selected_features) >= self.feature_num:
                break

        self._selected_features = [ind for ind, mi in selected_features]

        return self

    def transform(self, X):
        return X[:, self._selected_features]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

    def entropy(self, c):
        """
        entropy calculation

        :param c:

        :return:
        """
        c_normalized = c / float(np.sum(c))
        c_normalized = c_normalized[np.nonzero(c_normalized)]
        H = -sum(c_normalized * np.log2(c_normalized))
        return H

    def feature_label_MIs(self, arr, y):
        """
        calculate feature-label mutual information

        :param arr:

        :param y:

        :return:
        """
        m, n = arr.shape
        MIs = []
        p_y = np.histogram(y)[0]
        h_y = self.entropy(p_y)

        for i in range(n):
            p_i = np.histogram(arr[:, i])[0]
            p_iy = np.histogram2d(arr[:, 0], y)[0]

            h_i = self.entropy(p_i)
            h_iy = self.entropy(p_iy)

            MI = h_i + h_y - h_iy
            MIs.append(MI)
        return MIs

    def feature_feature_MIs(self, x, y):
        """
        calculate feature-feature mutual information

        :param x:

        :param y:

        :return:
        """
        p_x = np.histogram(x)[0]
        p_y = np.histogram(y)[0]
        p_xy = np.histogram2d(x, y)[0]

        h_x = self.entropy(p_x)
        h_y = self.entropy(p_y)
        h_xy = self.entropy(p_xy)

        return h_x + h_y - h_xy

    @property
    def important_features(self):
        return self._selected_features


class Relif():
    def __init__(self, max_iter, tao):
        """
        This is a simple implementation of relif algorithm which used
        for feature selections, the relif is simple to understand and
        high performance, but it can only deal with binary classification.

        Pay attention: relif use random sample selection of same class
        rather than using nearest neighbor sample to calculate nearest
        hit and miss, and it use number or string to make difference
        between named variable and numeric variable.
        it cannot handle null data, it will be improved later.

        Read more in :
        ref:`https://blog.csdn.net/littlely_ll/article/details/71614826`.

        :param max_iter: max iterations of relif

        :param tao: the threshold of feature weight
        """
        self.max_iter = max_iter
        self.tao = tao
        self.chosen_features = dict()

    def fit(self, X, y):
        """
        fit an array data

        :param X: a numpy array

        :param y: the label, a list or one dimension array

        :return:
        """
        X = self._check_array(X)
        y = self._check_array(y)
        assert X.shape[0] == len(y), "X and y not in the same length!"

        m, n = X.shape

        weight = np.zeros(n)

        for _ in range(self.max_iter):
            sample_seed = random.randint(0, m-1)
            sample_y = y[sample_seed]
            sample_x = X[sample_seed]

            while True:
                seed = random.randint(0, m - 1)
                if y[seed] == sample_y and sample_seed != seed:
                    near_hit = X[seed]
                    break
            while True:
                seed = random.randint(0, m - 1)
                if y[seed] != sample_y:
                    near_miss = X[seed]
                    break

            for i in range(n):
                near_hit_sum = 0
                near_miss_sum = 0
                if isinstance(sample_x[i], str):
                    if sample_x[i] != near_hit[i]:
                        near_hit_sum += 1
                    if sample_x[i] != near_miss[i]:
                        near_miss_sum += 1
                elif isinstance(sample_x[i], float):
                    near_hit_sum += pow(sample_x - near_hit, 2)
                    near_miss_sum += pow(sample_x - near_miss, 2)

                weight[i] += near_miss_sum - near_hit_sum

        weight = weight / self.max_iter

        for i, w in enumerate(weight):
            if w >= self.tao:
                self.chosen_features.update({i: w})

        return self

    def transform(self, X):
        """
        transform the array data

        :param X: array of data

        :return: the selected features
        """
        chosen_features = list(self.chosen_features.keys())
        return X[:, chosen_features]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

    @property
    def important_features(self):
        return self.chosen_features


class RelifF():
    def __init__(self, max_iter, tao, neighbors):
        """
        This is a simple implementation of relifF algorithm which used
        for feature selections, the relifF is simple to understand and
        can process multi-classifications.

        Pay attention: relifF use random sample selection of same class
        rather than using nearest neighbor sample to calculate nearest
        hit and miss, and it cannot handle null data, it will be
        improved later.

        Read more in :
        ref:`https://blog.csdn.net/littlely_ll/article/details/71614826`.

        :param max_iter: max iterations of relifF

        :param tao: the threshold of feature weight

        :param neighbors: the neighbors of each class to calculate weight
        """
        self.max_iter = max_iter
        self.tao = tao
        self.neighbors = neighbors
        self._weight = None
        self._important_weight = dict()

    def fit(self, X, y):
        """
        fit an array data

        :param X: a numpy array

        :param y: the label, a list or one dimension array

        :return:
        """
        X = self._check_array(X)
        y = self._check_array(y)
        assert X.shape[0] == len(y), "X and y not in the same length!"

        m, n = X.shape

        self._weight = np.zeros(n)

        label_count = dict()
        label_index = dict()
        for label in np.unique(y):
            label_index[label] = np.where(y == label)[0]
            label_count[label] = len(np.where(y == label)[0])

        # label probability
        label_probability = dict((label, count/m)
                                 for label, count in label_count.items())

        col_type = []
        for i in range(n):
            if isinstance(X[:, i][0], str):
                col_type.append((1,))
            else:
                col_min = X[:, i].min()
                col_max = X[:, i].max()
                difference = col_max - col_min
                col_type.append((0, difference))

        for _ in range(self.max_iter):
            sample_seed = random.randint(0, m - 1)
            sample_y = y[sample_seed]
            sample_x = X[sample_seed]

            for j in range(n):
                near_hit_sum = 0
                near_miss_sum = 0
                for label in label_index.keys():
                    if label == sample_y:
                        near_hit_neighbors = np.random.choice(
                            label_index[label], self.neighbors, replace=False)
                        for i in near_hit_neighbors:
                            sample_i = X[i]
                            if col_type[j][0] == 1:
                                if sample_x[j] != sample_i[j]:
                                    near_hit_sum += 1
                            else:
                                near_hit_sum += np.abs(
                                    sample_x[j] - sample_i[j]) / col_type[j][1]
                    else:
                        pre_near_miss_sum = 0
                        near_miss_neighbors = np.random.choice(
                            label_index[label], self.neighbors, replace=False)
                        for i in near_miss_neighbors:
                            sample_i = X[i]
                            if col_type[j][0] == 1:
                                if sample_x[j] != sample_i[j]:
                                    pre_near_miss_sum += 1
                            else:
                                pre_near_miss_sum += np.abs(
                                    sample_x[j] - sample_i[j]
                                ) / col_type[j][1] + 0.001
                        near_miss_sum += pre_near_miss_sum * label_probability[
                            label] / (1 - label_probability[sample_y])

                self._weight[j] += (near_miss_sum -
                                    near_hit_sum) / self.neighbors

        for i, w in enumerate(self._weight):
            if w >= self.tao:
                self._important_weight[i] = w

        return self

    def transform(self, X):
        """
        transform the array data

        :param X:  array of data

        :return: the selected features
        """
        important_col = list(self._important_weight.keys())
        return X[:, important_col]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

    @property
    def important_features(self):
        return self._important_weight

    @property
    def weight(self):
        return self._weight
