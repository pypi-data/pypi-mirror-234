# -*- coding: utf-8 -*-
class BizException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.code = -1


class NoConfigException(Exception):
    def __init__(self, message: str = '系统参数配置异常'):
        self.message = message
        self.code = -1
