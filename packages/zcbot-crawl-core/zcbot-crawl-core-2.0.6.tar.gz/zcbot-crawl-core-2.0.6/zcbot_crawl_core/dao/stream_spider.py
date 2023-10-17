# -*- coding: utf-8 -*-
from typing import Optional, List
from ..client.mongo_client import Mongo
from ..model.entity import StreamSpider, StreamSpiderModel
from ..model.enums import CommonStatus


# 获取portainer爬虫配置
def get_stream_spiders(spider_ids: List[str], status: CommonStatus) -> List[StreamSpider]:
    rows = Mongo().list("zcbot_stream_spider", {'spiderId': {'$in': spider_ids}, 'status': status.name})
    if not rows:
        return []
    return [StreamSpider(**x) for x in rows]


def get_stream_spider(spider_id: str, status: CommonStatus) -> Optional[StreamSpiderModel]:
    row = Mongo().get('zcbot_stream_spider', {'spiderId': spider_id, 'status': status.name})
    if not row:
        return None
    return StreamSpiderModel(**row)


# 获取支持网站平台
def get_platforms_by_spider_id(spider_ids: List[str], status: CommonStatus):
    return Mongo().aggregate('zcbot_platforms', [
        {
            '$lookup': {
                'from': 'zcbot_stream_spider',
                'localField': '_id',
                'foreignField': 'plat_code',
                'as': 'spider'
            }
        },
        {
            '$match': {'spider._id': {'$in': spider_ids}, 'status': status.name}
        },
        {
            '$project': {'spider': 0}
        },
        {'$sort': {'sort': 1}}
    ])
