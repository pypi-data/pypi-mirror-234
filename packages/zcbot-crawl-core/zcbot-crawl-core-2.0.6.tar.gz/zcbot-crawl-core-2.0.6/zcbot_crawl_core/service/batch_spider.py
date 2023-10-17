# -*- coding: utf-8 -*-
from ..util import logger
from ..dao import batch_spider as batch_spider_dao

LOGGER = logger.get('批次爬虫')


def get_batch_spider(spider_id: str):
    row = batch_spider_dao.get_batch_spider(spider_id=spider_id)
    return row
