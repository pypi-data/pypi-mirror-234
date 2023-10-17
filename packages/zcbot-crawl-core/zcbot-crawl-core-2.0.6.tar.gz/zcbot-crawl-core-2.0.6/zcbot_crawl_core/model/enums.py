# encoding:utf-8
from enum import Enum


class TaskType(str, Enum):
    """
    任务类型枚举
    """
    # 商品基础信息
    SKU_INFO = 'sku_info'
    # 商品价格
    SKU_PRICE = 'sku_price'
    # 商品基础信息及价格等详细信息
    SKU_FULL = 'sku_full'
    # 商品主详图
    SKU_IMAGE = 'sku_image'
    # 流式采集商品编码（如编码）
    STREAM_SKU_ID = 'stream_sku_id'
    # 流式采集商品价格信息
    STREAM_SKU_PRICE = 'stream_sku_price'
    # 流式采集商品基础信息及价格等详细信息
    STREAM_SKU_FULL = 'stream_sku_full'
    # 流式采集商品主详图
    STREAM_SKU_IMAGE = 'stream_sku_image'
    # 流式搜索同款商品
    STREAM_SKU_SAME = 'stream_sku_same'
    # 评论数量
    STREAM_SKU_COMMENT = 'stream_sku_comment'

    @staticmethod
    def to_list():
        enum_list = list()
        for tuple_item in TaskType.__members__.items():
            enum_list.append({'id': tuple_item[0], 'name': tuple_item[1].value})
        return enum_list


class CrawlJobStatus(str, Enum):
    """
    采集任务状态枚举
    """

    CREATED = "已创建"
    RUNNING = "采集中"
    CANCELED = "已取消"
    ERROR = "启动失败"
    CRAWLING = "采集中"
    CRAWLED = "采集完成"


class CommonStatus(str, Enum):
    """
    通用状态枚举
    """
    # 启用
    ON = '已启用'
    # 停用
    OFF = '已停用'


class StreamSpiderGroup(str, Enum):
    """
    爬虫组枚举
    """
    # 流采图片
    streamImage = "stream_image"
    # 流采价格
    streamPrice = "stream_price"
    # 流采商品
    streamSku = "stream_sku"
