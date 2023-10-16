"""
Global PipeGraphPy exception and warning classes.
"""
class LockAcquireTimeout(Exception):
    """锁获取超时"""

    pass


class CycleException(Exception):
    """有环"""

    pass


class MissInputError(Exception):
    """缺少输入"""

    pass


class ParamsError(Exception):
    """传参错误"""

    pass


class ModuleError(Exception):
    """模块错误"""

    pass


class RedisOperateError(Exception):
    """Redis操作出错"""

    pass


class MultiGraphException(Exception):
    """多个图异常，运行时只能运行一个图"""

    pass


class ImproperlyConfigured(Exception):
    """不当配置"""

    pass


def judge_err_type(ex):
    ex = str(ex)
    # try:
    #     error_type_infos = db.ErrorTypeTB.find()
    #     for i in error_type_infos:
    #         if ex.find(i["contained_string"]) != -1:
    #             return type(i["cls_name"], (Exception,), dict(msg=i["msg"])), i
    #     return None, None
    # except:
    #     return None, None
