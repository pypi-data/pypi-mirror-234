# -*- coding: utf-8 -*-
# @Time    : 2022/4/24 16:53:34
# @Author  : Pane Li
# @File    : exception.py
"""
定义各种异常类型

"""


class UsernameOrPasswordError(Exception):
    pass


class ParameterValueError(Exception):
    pass


class ParameterTypeError(Exception):
    pass


class AddResourceError(Exception):
    pass


class ResourceNotFoundError(Exception):
    pass


class ResourceAlreadyExist(Exception):
    pass


class TimeOutError(Exception):
    pass


class UpgradeFailedError(Exception):
    pass


class ModelError(Exception):
    pass
