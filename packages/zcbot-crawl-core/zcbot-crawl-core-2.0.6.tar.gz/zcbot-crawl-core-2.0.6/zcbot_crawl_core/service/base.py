# -*- coding: utf-8 -*-
from ..util import logger
from ..model.base import Platforms, Rule
from ..dao import meta as meta_dao

LOGGER = logger.get('基础')


# 获取支持网站平台
def get_platforms():
    rows = meta_dao.get_platforms()
    return [Platforms(**x) for x in rows]


# 获取链接分拣规则配置
def get_url_parse_rule(host: str = None):
    rows = meta_dao.get_url_parse_rule(host)
    return rows


def get_file_name_config(config_id: str = None):
    row = meta_dao.get_file_name_config(config_id)
    return row
