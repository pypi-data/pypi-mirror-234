# -*- coding: utf-8 -*-
from typing import List
from ..client.mongo_client import Mongo
from ..model.base import Rule


# 获取链接分拣规则配置
def get_url_parse_rule(host: str = None):
    if host:
        return Rule(**Mongo().get(collection='zcbot_url_parse_rule', query={'_id': host}))

    return [Rule(**x) for x in Mongo().list(collection='zcbot_url_parse_rule')]


# 获取支持网站平台
def get_platforms():
    return Mongo().list(collection='zcbot_platforms', sort=[('sort', 1)])


# 获取文件命名规则配置
def get_file_name_config(config_id):
    return Mongo().get(collection='zcbot_file_name_config', query={'_id': config_id})
