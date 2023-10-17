from typing import List

from pydantic import BaseModel, Field

from ..util import time as time_lib


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # mongodb主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class Platforms(BaseModel):
    """
    支持平台模型
    """
    # 平台编码
    platCode: str = None
    # 平台名称
    platName: str = None
    # 排序
    sort: int = None
    # logo
    logo: str = None


class Rule(BaseModel):
    """
    解析规则
    """
    # host
    host: str = None
    # 平台编码
    platCode: str = None
    # 参数
    params: List = []
    # 解析规则
    regex: List = []
    # 排序
    sort: int = None
    # 生成时间
    genTime: int = None
