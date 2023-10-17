# -*- coding: utf-8 -*-
from typing import List
from ..model.base import Platforms
from ..util import logger
from ..dao import batch_spider_group as batch_spider_group_dao
from ..model.entity import BatchSpiderGroup

LOGGER = logger.get('批次爬虫组')


def get_spider_group_list(group_code: str = None, plat_codes: List[str] = None, enable: int = None):
    rows = batch_spider_group_dao.get_spider_group_list(group_code=group_code, plat_codes=plat_codes, enable=enable)
    rows = [BatchSpiderGroup(**x) for x in rows]
    return rows


def get_spider_group(group_code: str = None, plat_code: str = None, enable: int = None):
    row = batch_spider_group_dao.get_spider_group(group_code=group_code, plat_code=plat_code, enable=enable)
    row = BatchSpiderGroup(**row)
    return row


def get_platforms_by_group(group_code: str, enable: int = None):
    rows = batch_spider_group_dao.get_platforms_by_group_code(group_code=group_code, enable=enable)
    rows = [Platforms(**x) for x in rows]
    return rows
