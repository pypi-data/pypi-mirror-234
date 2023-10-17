from typing import List, Union, Dict
from pydantic import BaseModel, Field
from .batch import BaseData
from .enums import TaskType


class StreamTaskItem(BaseData):
    """
    任务物料模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = Field(description="对象唯一序列号", default=None)
    # 【输入】商品链接
    url: str = Field(description="商品链接", default=None)
    # 【输入】来源APP（流采模式）
    appCode: str = Field(description="应用编码", default=None)
    # 电商链接唯一码（platCode:ecSkuId）
    linkId: str = Field(description="电商链接唯一码", default=None)
    # 电商商品编码
    ecSkuId: str = Field(description="电商商品编码", default=None)
    # 电商平台编码（识别链接获得）
    platCode: str = Field(description="电商平台编码", default=None)
    # 电商平台名称（识别链接获得）
    platName: str = Field(description="电商平台名称", default=None)
    # 批次编号
    batchId: str = Field(description="批次编号", default=None)
    # 【输入】用户指定编号（可选，不填使用默认值，等于sn）
    rowId: str = Field(description="用户指定编号（可选，不填使用默认值，等于sn）", default=None)
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = Field(description="扩展字段", default=None)

    def to_classify_result(self):
        rs = {
            'sn': self.sn,
            'linkId': self.linkId,
            'ecSkuId': self.ecSkuId,
            'platCode': self.platCode,
            'platName': self.platName,
            'appCode': self.appCode,
        }
        # 可有可无
        if self.rowId is not None:
            rs['rowId'] = self.rowId
        if self.callback is not None:
            rs['callback'] = self.callback
        return rs


class StreamApiData(BaseModel):
    """
    流式通用数据接收模型
    """
    # 【输入】应用编码
    appCode: str = Field(description="应用编码", default=None)
    # 【输入】任务类型
    spiderIds: Union[List[str], str] = Field(description="爬虫主键", default=[])
    # 【输入】任务明细清单
    taskItems: List[StreamTaskItem] = Field(description="任务明细清单", default=[])
    # 【输入】任务队列后缀（用于拆分某些应用专用任务队列）
    taskQueueSuffix: str = Field(description="任务队列后缀", default=None)
    # 【输入】文件名称配置键
    fileNameConfig: str = Field(description="任务明细清单", default='default')
