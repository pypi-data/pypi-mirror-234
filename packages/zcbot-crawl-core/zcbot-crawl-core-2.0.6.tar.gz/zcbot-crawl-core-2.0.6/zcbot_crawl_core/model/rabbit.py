import time
from enum import Enum
from typing import Union, Dict, List
from pydantic import BaseModel


class MsgType(Enum):
    """
    消息类型枚举
    """
    # 爬虫控制指令
    ACT_OPENED = 'OPENED'
    ACT_CLOSED = 'CLOSED'
    # 数据消息
    DATA_SKU_TEXT = 'SKU_TEXT'
    DATA_SKU_IMAGES = 'SKU_IMAGES'
    # 压缩指令
    ZIP_DONE = 'ZIP_DONE'


class SignalType(Enum):
    """
    采云间爬虫状态信号枚举
    """
    OPENED = 'OPENED'
    CLOSED = 'CLOSED'


class BaseMsg(BaseModel):
    """
    标准消息数据模型
    """
    # 消息类型（控制消息：ACT；数据消息：DATA）
    msg_type: MsgType
    # 消息体
    msg_body: Union[str, Dict, List] = None
    # 产生时间戳
    gen_time: int = int(time.time())
