# -*- coding: utf-8 -*-
from typing import List
from ..client.mongo_client import Mongo


# 获取支持网站平台
def get_platforms_by_group(group_code: str, enable: int = None):
    _query = {}
    if group_code:
        _query["groupCode"] = group_code
    if enable is not None:
        _query["enable"] = enable

    return Mongo().list('zcbot_batch_spider_group', query=_query)


def get_platforms_by_group_code(group_code: str, enable):
    _query = {
        "groupCode": group_code
    }
    _fields = {
        "spiders": 0,
        "_id": 0
    }
    return Mongo().aggregate('zcbot_platforms', [
        {
            '$lookup': {
                'from': 'zcbot_batch_spider_group',
                'localField': '_id',
                'foreignField': 'platCode',
                'as': 'spider'
            }
        },
        {
            '$match': {'spider.groupCode': group_code}
        },
        {
            '$project': {'spider': 0}
        },
        {'$sort': {'sort': 1}}
    ])


# 根据爬虫组编号，获取可选的爬虫清单
def get_spider_group(group_code: str = None, plat_code: str = None, enable: int = None):
    _query = {}
    if group_code:
        _query["groupCode"] = group_code
    if plat_code:
        _query["platCode"] = plat_code
    if enable is not None:
        _query["enable"] = enable

    return Mongo().get('zcbot_batch_spider_group', query=_query)


# 根据爬虫组编号，获取爬虫组清单
def get_spider_group_list(group_code: str = None, plat_codes: List[str] = None, enable: int = None):
    _query = {}
    if group_code:
        _query["groupCode"] = group_code
    if plat_codes and len(plat_codes):
        _query["platCode"] = {"$in": plat_codes}
    if enable is not None:
        _query["enable"] = enable

    return Mongo().list('zcbot_batch_spider_group', query=_query)
