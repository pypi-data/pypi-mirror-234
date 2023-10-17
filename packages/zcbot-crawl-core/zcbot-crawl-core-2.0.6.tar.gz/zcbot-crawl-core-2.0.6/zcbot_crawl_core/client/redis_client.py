# -*- coding: utf-8 -*-
import redis
from ..util import cfg
from ..util.decator import singleton
from ..util.exceptions import NoConfigException


@singleton
class Redis(object):
    """
    Redis客户端简易封装（单例）
    """

    def __init__(self, redis_uri: str = None, redis_db: int = None, decode_responses=True):
        self.redis_uri = redis_uri or cfg.get('ZCBOT_CORE_REDIS_URL')
        self.redis_db = redis_db or cfg.get('ZCBOT_CORE_REDIS_DB')
        if not self.redis_uri:
            raise NoConfigException('redis uri not config!')
        if not self.redis_db:
            raise NoConfigException('redis database not config!')

        self.client = redis.Redis.from_url(url=self.redis_uri, db=self.redis_db, decode_responses=decode_responses)

    # 销毁关闭连接池
    def __del__(self):
        if self.client:
            self.client.close()
