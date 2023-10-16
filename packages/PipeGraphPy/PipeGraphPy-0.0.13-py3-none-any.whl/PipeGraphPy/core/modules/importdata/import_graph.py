# coding: utf8

import traceback
import pickle
from PipeGraphPy.logger import log
from . import InputDataBase


class ImportGraph(InputDataBase):

    def __init__(self, **kw):
        InputDataBase.__init__(self, **kw)

    def run(self):
        try:
            with open(self.params['path'], 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception:
            log.error(traceback.format_exc())
            raise Exception('载入模型失败')

    def predict(self):
        return None
