# -*- coding: utf-8 -*-
from typing import Optional, List
from ..client.mongo_client import Mongo
from ..model.entity import PortainerNode
from ..model.enums import CommonStatus


# 获取节点信息
def get_node(node_id) -> Optional[PortainerNode]:
    rs = Mongo().get(collection='zcbot_portainer_node', query={'_id': node_id})
    if not rs:
        return None

    return PortainerNode(**rs)


# 获取节点信息列表
def get_node_list(query: dict = None, fields: dict = None, include_disable: bool = False) -> List[PortainerNode]:
    _query = query or {}
    _fields = fields or {}
    if not include_disable:
        _query['status'] = CommonStatus.ON.name
    rows = Mongo().list(collection='zcbot_portainer_node', query=_query, fields=_fields)
    if rows:
        return [PortainerNode(**row) for row in rows]

    return []
