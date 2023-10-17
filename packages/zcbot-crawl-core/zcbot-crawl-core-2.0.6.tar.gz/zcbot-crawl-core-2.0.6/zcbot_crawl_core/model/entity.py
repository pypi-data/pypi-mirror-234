from typing import List
from pydantic import BaseModel


class BatchSpider(BaseModel):
    """
    Portainer爬虫
    """
    # 爬虫id(主键)
    spiderId: str = None
    # 容器镜像标签
    dockerImage: str = None
    # 运行启动参数模板
    param: str = None
    # 任务模式（批量multi、单个single）
    taskMode: str = None
    # 批次请求大小（批量模式有效）
    batchSize: int = 1
    # 可运行节点编号列表
    nodes: List[str] = None
    # 电商平台编码
    platCode: str = None
    # 电商平台名称
    platName: str = None
    # 任务类型
    taskType: str = None
    # 任务类型描述
    taskTypeText: str = None
    # 备注
    remark: str = None
    # 支持链接规则编码集合
    patterns: List[str] = None
    # 运行环境变量集合
    env: List[str] = None
    # 状态
    status: str = None
    statusText: str = None


class SupportPlatform(BaseModel):
    """
    支持平台
    """
    # 【输入】平台编码
    platCodes: List[str] = None
    # 【输入】
    groupCode: str = None


class Spider(BaseModel):
    spiderId: str = None
    # 平台名称
    platCode: str = None
    # 任务类型
    taskType: str = None
    # 任务类型(显示用)
    taskTypeText: str = None
    # 是否默认可点击
    defaultChecked: int = None
    # 备份
    remark: str = None
    # 状态
    status: str = None
    statusText: str = None


class BatchSpiderGroup(BaseModel):
    # 爬虫组(主键)
    groupId: str = None
    # 爬虫信息
    spiders: List[Spider] = []
    # 平台编码
    platCode: str = None
    # 平台名称
    platName: str = None
    # 组编码
    groupCode: str = None
    # 组名称
    groupName: str = None
    # 标题
    title: str = None
    # 状态
    status: str = None
    statusText: str = None
    # 商品状态选择
    skuStatusElect: str = None


class PortainerNode(BaseModel):
    """
    Portainer平台节点
    """
    # 端点序列号 全局唯一（自定义，不可直接使用节点Id字段）
    nodeId: str = None
    # 端点名称
    nodeName: str = None
    # 备注
    remark: str = None

    # api base url
    apiBaseUrl: str = None
    # api token
    apiToken: str = None
    # /api/endpoints中的Id字段
    endpointId: str = None

    # 状态
    status: str = None
    statusText: str = None


class StreamSpider(BaseModel):
    """
    流程爬虫
    """
    # 爬虫项目名称
    botName: str = None
    # redis队列
    redisKey: str = None
    # 爬虫id(主键)
    spiderId: str = None
    # 爬虫名称
    spiderName: str = None
    # 爬虫信号
    signals: List[str] = []
    # 任务模式（批量batch、单个single）
    taskMode: str = None
    # 批次请求大小（批量模式有效）
    batchSize: int = 1
    # 电商平台编码
    platCode: str = None
    # 电商平台名称
    platName: str = None
    # 任务类型
    taskType: str = None
    # 任务类型描述
    taskTypeText: str = None
    # 备注
    remark: str = None
    # 支持链接规则编码集合
    patterns: List[str] = None
    # 状态
    status: str = None
    statusText: str = None


class StreamSpiderModel(BaseModel):
    """
    流采爬虫配置表
    """
    # sn,id,爬虫id
    # _id命名规则：groupCode:spiderProjectName:spiderName
    # eg: sku_full:stream_sku_jd:sku_info_pc_v1
    _id: str = None
    # 爬虫组编码
    groupCode: str = None
    # 爬虫组名称
    groupName: str = None
    # 平台编码
    platCode: str = None
    # 平台名称
    platName: str = None
    # 爬虫项目名称
    botName: str = None
    # 爬虫id
    spiderId: str = None
    # 爬虫名称
    spiderName: str = None
    # 爬虫状态
    status: str = None
    # 爬虫状态中文
    statusText: str = None
    # redis队列
    redisKey: str = None
    # 任务模式 单条/批量 single/batch
    taskMode: str = None
    # 批次大小 1/60
    batchSize: int = None
    # 备注
    remark: str = None
