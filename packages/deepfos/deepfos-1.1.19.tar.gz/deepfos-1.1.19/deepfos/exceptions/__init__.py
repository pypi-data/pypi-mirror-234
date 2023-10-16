from .hook import eliminate_from_traceback


class DeepfosBaseException(Exception):
    """deepfos自定义异常基类"""


# -----------------------------------------------------------------------------
# Option Error
class BaseOptionError(DeepfosBaseException):
    """配置项异常基类"""


class OptionNotSetError(BaseOptionError):
    """配置项未设置"""


class OptionTypeError(BaseOptionError):
    """配置项类型错误"""


class OptionValueError(BaseOptionError):
    """配置项值错误"""


# -----------------------------------------------------------------------------
# API Error
class APIError(DeepfosBaseException, OSError):
    """API相关异常"""


class APIRequestError(APIError):
    """调用API时请求异常"""


class APIResponseError(APIError):
    """调用API返回异常"""
    def __init__(self, msg, code=None):
        super().__init__(msg)
        self.code = code


# -----------------------------------------------------------------------------
# Element Error

class ElementError(DeepfosBaseException):
    """元素相关异常"""


class ElementTypeMissingError(ElementError):
    """无法获取元素类型"""


class ElementNotFoundError(ElementError):
    """元素不存在"""


class ElementAmbiguousError(ElementError):
    """无法锁定唯一元素"""


class ElementVersionIncompatibleError(ElementError):
    """元素版本不兼容"""


class DimensionSaveError(ElementError):
    """无法保存维度"""


class MemberNotFoundError(ElementError):
    """维度成员不存在"""


class VariableUpdateError(ElementError):
    """无法更新变量"""


class VariableCreateError(ElementError):
    """无法新建变量"""


# -----------------------------------------------------------------------------
# RedisLock Error

class LockAcquireFailed(DeepfosBaseException):
    """无法获取Redis锁"""


class BadFutureError(DeepfosBaseException):
    """获取future property返回值过程出现错误"""
    def __init__(self, msg, obj):
        super().__init__(msg)
        self.obj = obj


# -----------------------------------------------------------------------------
# Pyscript Error
class PyTaskError(DeepfosBaseException):
    """执行脚本报错基类"""


class ResultTimeOutError(PyTaskError):
    """执行脚本超时"""


class PyTaskInvalidError(PyTaskError):
    """脚本任务ID无效"""


class PyTaskRevokedError(PyTaskError):
    """执行脚本被取消"""


class PyTaskRunTimeError(PyTaskError):
    """执行脚本出错"""


class PyTaskUnsetError(PyTaskError):
    """任务未设置"""


class PyTaskConcurrencyExceed(PyTaskError):
    """任务并发数过高"""


# -----------------------------------------------------------------------------
# FinancialCube Error
class MDXExecuteTimeout(DeepfosBaseException):
    """执行MDX任务超时"""


# -----------------------------------------------------------------------------
# DeepModel Error
class DeepModelError(DeepfosBaseException):
    """DeepModel相关报错基类"""


class ObjectNotExist(DeepModelError):
    """DeepModel对象不存在"""


class RequiredFieldUnfilled(DeepModelError):
    """缺少必填字段"""


class ExternalObjectReadOnly(DeepModelError):
    """外部对象只可读"""


class RelationRequired(DeepModelError):
    """multi link字段缺少relation信息"""


class SingleLinkInRelation(DeepModelError):
    """single link字段出现在relation中"""


class MultiLinkTargetNotUnique(DeepModelError):
    """relation信息source的target不唯一"""
