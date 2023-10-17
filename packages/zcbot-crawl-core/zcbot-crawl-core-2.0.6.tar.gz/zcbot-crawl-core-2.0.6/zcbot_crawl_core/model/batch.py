from typing import List, Union, Dict
from pydantic import BaseModel, Field
from .base import BaseData
from .enums import CrawlJobStatus
from ..util import time as time_lib


class BatchTaskItem(BaseData):
    """
    【输入】任务明细模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 【输入】用户指定编号
    rowId: str = None
    # 【输入】商品链接
    url: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class BatchTask(BaseModel):
    """
    【输入】批次采集数据接收模型
    """
    # 【输入】任务爬虫编码清单
    spiderId: Union[List[str], str] = None
    # 【输入】任务链接明细清单
    taskItems: List[BatchTaskItem] = None
    # 【输入】启动容器数量
    containerCount: int = 1
    # 【输入】文件名称配置键（主详图采集命名使用，非必要）
    fileNameConfig: str = 'default'


class BatchApiData(BaseModel):
    """
    【输入】批次采集接口接收模型
    """
    # 【输入】批次编号
    batchId: str
    # 【输入】应用编码
    appCode: str
    # 【输入】任务明细清单
    taskList: List[BatchTask]
    # 【输入】是否为补采任务
    supplyTask: bool = False


class BatchJobInst(BaseData):
    """
    【输出】任务明细模型
    """
    # 【输出】对象唯一序列号（全局唯一，可用于主键，等于_id）
    jobId: str = None
    # 【输出】批次编号
    batchId: str = None
    # 【输出】爬虫容器ID
    containerId: str = None
    # 【输出】爬虫实例指纹，用于爬虫内部标记结果出处
    instSn: str = None
    # 【输出】任务数
    itemCount: int = None
    # 【输出】job运行节点
    node: Dict = None
    # 【输出】平台编码
    platCode: str = None
    # 【输出】 爬虫Id
    spiderId: str = None
    # 【输出】job状态
    status: str = None
    # 【输出】job状态描述
    statusText: str = None
    # 创建时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )
    # 更新时间
    updateTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )

    def set_status(self, status: CrawlJobStatus):
        self.status = status.name
        self.statusText = status.value


class BatchTaskResp(BaseModel):
    """
    【输出】批次采集数据接收模型
    """
    # 【输出】爬虫编码
    spiderId: str
    # 【输出】批次编号
    batchId: str
    # 【输出】任务链接明细清单
    nodes: List[BatchJobInst] = []


class BatchSpiderGroupQuery(BaseModel):
    """
    【输出】支持平台
    """
    # 【输入】平台编码
    platCodes: List[str] = None
    # 【输入】组编码
    groupCode: str = None
    # 【输入】是否可用
    # enable: int = 1
    status: str = None
    statusText: str = None
