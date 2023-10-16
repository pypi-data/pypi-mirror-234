#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Default PGP settings.
"""
import os
import sys
# from pyecharts.globals import NotebookType

class PGP_ENV:
    DEV = "dev"   # 本地开发
    DEBUG = "debug" # 本地测试
    RPC = "rpc"   # rpc
    RUN_WORKER = "run_worker"  # 训练worker
    PREDICT_WORKER = "predict_worker"   # 预测worker
    SDK = "sdk"  # sdk
    NONE = "none"   # 非执行训练和预测环境


DEBUG = False if str(os.environ.get("PGP_NOT_DEBUG")) == "1" else True
ISDEV = False if str(os.environ.get("PGP_NOT_DEV")) == "1" else True
ISJUPYTER = True if str(os.environ.get("PGP_JUPYTER")) == "1" else False
RUN_PERMISSION = True if str(os.environ.get("PGP_RUN_PERMISSION")) == "1" else False
RUN_MODEL_SAVE_PATH = os.environ.get("PGP_RUN_MODEL_SAVE_PATH", "")
SDK_MODEL_SAVE_PATH = os.environ.get("PGP_SDK_MODEL_SAVE_PATH", "")
PREDICT_MODEL_SAVE_PATH = os.environ.get("PGP_PREDICT_MODEL_SAVE_PATH", '')
PREDICT_RESULT_SAVE_PATH = os.environ.get("PGP_PREDICT_RESULT_SAVE_PATH", '')
TEMP_SAVE_PATH = os.environ.get("PGP_TEMP_SAVE_PATH", "")
CUSTOM_CACHE_PATH = os.environ.get("PGP_CUSTOM_CACHE_PATH", '')
REDIS_HOST = os.environ.get("REDIS_HOST", '39.105.185.60')
REDIS_PORT = int(os.environ.get("REDIS_PORT", '6371'))
PGP_DB_HOST = os.environ.get("PGP_DB_HOST", '39.105.185.60')
PGP_DB_PORT = int(os.environ.get("PGP_DB_PORT", '33061'))
AMQP_URL = os.environ.get("AMQP_URL", '')
RUN_TIMEOUT = int(os.environ.get("RUN_TIMEOUT", 60 * 60 * 6))   # 训练超时2小时
PREDICT_TIMEOUT = int(os.environ.get("PREDICT_TIMEOUT", 60 * 10))   # 预测超时5分钟
RT_DB_CONNECTOR = os.environ.get("RT_DB_CONNECTOR", '')
ISONLINE = True if str(os.environ.get("PGP_IS_ONLINE")) == "1" else False
DEPLOYMENT_ENV = os.environ.get("PGP_DEPLOYMENT_ENV", "none")
RUN_ENV = os.environ.get("PGP_RUN_ENV", 'test')    # 运行环境, test, online, dev, sdk

# 模型保存配置
if DEPLOYMENT_ENV == PGP_ENV.SDK:
    HOME_CACHE_PATH = os.path.expanduser('~/.cache/PipeGraphPy/sdk/')
    if not SDK_MODEL_SAVE_PATH:
        SDK_MODEL_SAVE_PATH = os.path.join(HOME_CACHE_PATH, "sdk")
    if not os.path.exists(SDK_MODEL_SAVE_PATH):
        os.makedirs(SDK_MODEL_SAVE_PATH)
else:
    HOME_CACHE_PATH = os.path.expanduser('~/.cache/PipeGraphPy/')
if not RUN_MODEL_SAVE_PATH:
    RUN_MODEL_SAVE_PATH = os.path.join(HOME_CACHE_PATH, "models")
if not PREDICT_MODEL_SAVE_PATH:
    PREDICT_MODEL_SAVE_PATH = os.path.join(HOME_CACHE_PATH, "models")
if not PREDICT_RESULT_SAVE_PATH:
    PREDICT_RESULT_SAVE_PATH = os.path.join(HOME_CACHE_PATH, "predict_result")
if not TEMP_SAVE_PATH:
    TEMP_SAVE_PATH = os.path.join(HOME_CACHE_PATH, "temp")
if not CUSTOM_CACHE_PATH:
    CUSTOM_CACHE_PATH = os.path.join(HOME_CACHE_PATH, "custom")
if not os.path.exists(CUSTOM_CACHE_PATH):
    os.makedirs(CUSTOM_CACHE_PATH)
    _init_file = os.path.join(CUSTOM_CACHE_PATH, "__init__.py")
    with open(_init_file, "w") as f:
        f.write("#")
sys.path.append(os.path.dirname(CUSTOM_CACHE_PATH))
MODEL_SAVE_NAME = "graph_model_{graph_id}"
ALGO_MODEL_SAVE_NAME = "algo_model_{graph_id}_{node_id}_{algo_mod_type}_{idx}"

# 运行模式 1: 包引用 2：grpc
RUN_PATTERN = 1

# redis设置
REDIS_DB = 3 if str(os.environ.get("PGP_NOT_DEV")) == "1" else 4
REDIS_KEY_TTL = 7 * 24 * 60 * 60  # 过期时间,默认7天

# celery 存储设置
CELERY_REDIS_HOST = None
CELERY_REDIS_PORT = None
CELERY_REDIS_DB = None


# 时间格式
DATETIME_FORMAT = "%H:%M:%S"
DATETIME_TOTAL_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
]

# 计算存储引擎
STORAGE_ENGINE = "file"

# 结构数据库配置
DATABASES = {
    "ENGINE": "sqlite3",
    "NAME": "PipeGraphPy",
}

# 数据库配置
DATABASES_POOL = None
# 数据库名称
DATABASE_NAME = None
DATABASE_SERVER_NAME = None
DATABASE_DB_NAME = None


# jupyter_type
# JUPYTER_TYPE = NotebookType.JUPYTER_LAB


# SDK是否显示log日志
SDK_SHOW_LOG = False

