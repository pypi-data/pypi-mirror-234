# coding:utf-8

class FilterColumns():
    def __init__(self, **kw):
        self.params = kw

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X

