#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from PipeGraphPy.asyn.celery import app
from celery.app.control import Control
from PipeGraphPy.logger import log


def terminate(task_id):
    """停止任务
    parameters:
        task_id (Union(str, list)): 要停止的单个task_id或列表task_id
            (or list of ids).
    """
    try:
        celery_control = Control(app=app)
        celery_control.revoke(task_id, terminate=True)
    except Exception:
        log.error(traceback.format_exc())
