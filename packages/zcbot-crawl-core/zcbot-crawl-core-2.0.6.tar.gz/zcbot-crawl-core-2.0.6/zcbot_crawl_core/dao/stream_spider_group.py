# encoding: utf-8

from typing import List
from ..client.mongo_client import Mongo
from ..model.enums import CommonStatus


def get_spider_group_list(group_code: str, plat_codes: List[str], status: str = CommonStatus.ON):
    _query = {}
    if group_code:
        _query['taskType'] = group_code
    if plat_codes:
        _query['platCode'] = {"$in": plat_codes}

    _query['status'] = status

    return Mongo().list(collection="zcbot_stream_spider_group", query=_query)
