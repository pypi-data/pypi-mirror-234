# -*- coding: utf-8 -*-

from typing import List
from ..model.enums import CommonStatus
from ..model.entity import StreamSpiderModel
from ..dao import stream_spider_group


def get_spider_group_list(group_code: str, plat_codes: List[str], status: str = CommonStatus.ON) -> List[StreamSpiderModel]:
    rows = stream_spider_group.get_spider_group_list(group_code=group_code, plat_codes=plat_codes, status=status)
    rows = [StreamSpiderModel(**x) for x in rows]
    return rows


