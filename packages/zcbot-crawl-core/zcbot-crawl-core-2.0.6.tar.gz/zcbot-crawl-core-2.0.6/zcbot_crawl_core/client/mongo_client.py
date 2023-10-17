# -*- coding: utf-8 -*-
import pytz
from pymongo import MongoClient

from ..util import cfg
from ..util.exceptions import NoConfigException
from ..util.decator import singleton


@singleton
class Mongo(object):
    """
    Mongo基础客户端简易封装
    """

    def __init__(self, mongo_uri: str = None, mongo_db: str = None, *args, **kwargs):
        self.mongo_uri = mongo_uri or cfg.get('ZCBOT_CORE_MONGO_URL')
        self.mongo_db = mongo_db or cfg.get('ZCBOT_CORE_MONGO_DB')
        if not self.mongo_uri:
            raise NoConfigException('mongodb uri not config!')
        if not self.mongo_db:
            raise NoConfigException('mongodb database not config!')

        self.client = MongoClient(self.mongo_uri, tz_aware=True, tzinfo=pytz.timezone('Asia/Shanghai'))
        self.db = self.client[self.mongo_db]

    # 获取集合
    def get_collection(self, coll):
        return self.db.get_collection(coll)

    # 查询对象
    def get(self, collection, query={}):
        result = self.db[collection].find_one(query)
        return result

    # 统计数量
    def count(self, collection, query={}):
        return self.db[collection].count(query)

    # 查询列表
    def list(self, collection, query={}, fields=None, sort=[]):
        if fields:
            cursor = self.db[collection].find(query, fields, sort=sort)
        else:
            cursor = self.db[collection].find(query, sort=sort)
        return list(cursor)

    # 查询去重列表
    def distinct(self, collection, dist_key, query={}, fields=None):
        return self.db[collection].find(query, fields).distinct(dist_key)

    # 聚合查询
    def aggregate(self, collection, pipeline=[]):
        cursor = self.db[collection].aggregate(pipeline, session=None, allowDiskUse=True)
        return list(cursor)

    # 查询分页列表
    def list_with_page(self, collection, query={}, page_size=10000, fields=None):
        rows = list()
        total = self.db[collection].count(query)
        if total > 0 and page_size > 0:
            total_page = round(len(total) / page_size)
            for page in range(0, total_page):
                if fields:
                    cursor = self.db[collection].find(query, fields).skip(page_size * page).limit(page)
                else:
                    cursor = self.db[collection].find(query).skip(page_size * page).limit(page)
                curr_batch = list(cursor)
                if curr_batch:
                    rows.append(curr_batch)
        return rows

    # 插入或更新
    def insert_or_update(self, collection, data, id_key='_id'):
        return self.db[collection].update({id_key: data[id_key]}, {'$set': data}, upsert=True)

    # 更新
    def update(self, collection, filter, data, multi=False):
        return self.db[collection].update(filter, {'$set': data}, multi=multi)

    # 以主键更新
    def update_by_pk(self, collection, pk_val, data):
        return self.db[collection].update({'_id': pk_val}, {'$set': data}, multi=False)

    # 批量更新
    def batch_update(self, collection, filter, datas, multi=False):
        return self.db[collection].update(filter, datas, multi=multi)

    # 更新
    def delete(self, collection, filter):
        return self.db[collection].delete_many(filter)

    # 插入或更新
    def bulk_write(self, collection, bulk_list):
        if bulk_list:
            return self.db[collection].bulk_write(bulk_list, ordered=False, bypass_document_validation=True)

    # 关闭链接
    def close(self):
        self.client.close()

    # 销毁关闭链接
    def __del__(self):
        if self.client:
            self.client.close()
