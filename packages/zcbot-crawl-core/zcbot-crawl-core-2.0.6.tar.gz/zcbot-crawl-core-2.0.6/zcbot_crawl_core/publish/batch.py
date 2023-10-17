# -*- coding: utf-8 -*-
import json
import random
import uuid
from typing import List
from ..util import logger, cfg
from ..util import time as time_lib
from ..util import sequence as sequence_util
from ..util import redis_key as redis_key_util
from ..util.exceptions import BizException
from ..model.batch import BatchTaskItem
from ..client.redis_client import Redis
from ..client.portainer_client import PortainerClient
from ..model.entity import PortainerNode
from ..model.batch import BatchApiData, BatchJobInst
from ..model.enums import CommonStatus, CrawlJobStatus
from ..dao import batch_spider as spider_dao
from ..dao import node as node_dao

LOGGER = logger.get("任务")
client = PortainerClient()


def publish(api_data: BatchApiData):
    """
    发起批次采集
    """
    # 如果上游传递则直接使用，否则本系统生成批次编号
    batch_id = api_data.batchId or sequence_util.gen_batch_id()
    app_code = api_data.appCode
    LOGGER.info(f"[启动]开始启动 app_code={app_code}, batch_id={batch_id}")

    rs_list = list()

    # 任务数据与爬虫配置校验
    for task in api_data.taskList:
        task_items = task.taskItems
        spider_id = task.spiderId
        file_name_config = task.fileNameConfig
        if not spider_id or not task_items:
            LOGGER.error(f"[启动]存在异常任务 batch_id={batch_id}, spider_id={spider_id}, task_items={len(task_items)}, app_code={app_code}")
            continue
        spider = spider_dao.get_batch_spider(spider_id)
        if not spider or spider.status != CommonStatus.ON.name:
            LOGGER.error(f"[启动]爬虫不存在或已停用 spider_id={spider_id}, app_code={app_code}, batch_id={batch_id}, task_items={len(task_items)}")
            continue

        # 创建容器 + 初始化队列
        plat_code = spider.platCode
        task_mode = spider.taskMode
        batch_size = spider.batchSize
        inst_sn = sequence_util.short_uuid()
        # 初始化容器
        init_task_queue(task_items, batch_id, spider_id, batch_size, plat_code, task_mode)

        # 选择一个节点
        node = node_balance_choice(spider.nodes)
        if not node:
            LOGGER.error(f"[启动]爬虫暂无可用运行节点 spider_id={spider_id}, nodes={spider.nodes}, app_code={app_code}, batch_id={batch_id}, task_items={len(task_items)}")
            continue

        # 创建容器
        container_name = f'{spider.taskType}-{spider.platCode}-{batch_id}-{inst_sn}'
        container_id = client.create_container(
            spider=spider,
            node=node,
            container_name=container_name,
            param_data={"batch_id": batch_id, "inst_sn": inst_sn, "app_code": app_code, "file_name_config": file_name_config}
        )
        # 附带信息
        item_count = len(task_items)
        if container_id:
            job_inst = BatchJobInst(
                jobId=f'{node.endpointId}:{container_id}',
                batchId=batch_id,
                containerId=container_id,
                instSn=inst_sn,
                itemCount=item_count,
                node=node,
                spiderId=spider_id,
                platCode=plat_code,
                status=CrawlJobStatus.ERROR.name,
                statusText=CrawlJobStatus.ERROR.value,
            )
            # 启动容器
            rs = client.start(node, container_id)
            if rs:
                # 启动成功
                job_inst.status = CrawlJobStatus.RUNNING.name
                job_inst.statusText = CrawlJobStatus.RUNNING.value
            rs_list.append(job_inst)

    return rs_list


def cancel_job(node_id: str, container_id: str):
    """
    取消采集任务
    """
    node = node_dao.get_node(node_id)
    if not node:
        raise BizException(f"[任务]节点不存在或已停用 node_id={node_id}, container_id={container_id}")

    rs = client.stop(node, container_id)
    LOGGER.info(f"[任务]取消完成 endpoint_id={node.endpointId}, container_id={container_id}, rs={rs}")
    return rs


def init_task_queue(task_items, batch_id, spider_id, batch_size, plat_code, task_mode) -> int:
    """
    初始化任务队列
    :param task_items:
    :param batch_id:
    :param batch_size:
    :param spider_id:
    :param app_code:
    :param task_mode:
    :param expire_seconds:
    :return:
    """

    # 初始化队列
    LOGGER.info(f"[队列]任务队列初始化开始 task_mode={task_mode}")
    tmp_queue_expire = cfg.get_int("ZCBOT_CORE_REDIS_TMP_QUEUE_EXPIRE") or 3600
    if task_mode and task_mode == "multi":
        # 批量模式（如：京东价格）
        return _init_redis_batch(
            batch_id=batch_id,
            batch_size=batch_size,
            spider_id=spider_id,
            plat_code=plat_code,
            rows=task_items,
            expire_seconds=tmp_queue_expire
        )
    else:
        # 单条采集模式
        return _init_redis(batch_id=batch_id, spider_id=spider_id, plat_code=plat_code, rows=task_items, expire_seconds=tmp_queue_expire)


def _init_redis(batch_id: str, spider_id: str, plat_code: str, rows: List[BatchTaskItem], expire_seconds: int):
    redis_key = redis_key_util.get_task_queue_key(batch_id, spider_id)
    Redis().client.delete(redis_key)
    for row in rows:
        request_id = str(uuid.uuid4())
        task = row.dict()
        task['requestId'] = request_id
        if plat_code:
            task["platCode"] = plat_code
        # 任务入队
        Redis().client.lpush(redis_key, json.dumps(task))
        # 加入重试源数据集合
        add_to_retry_source_mapper(request_id, task, redis_key)

    # 设置任务队列过期时间：默认12小时自动清理
    set_expire(batch_id=batch_id, spider_id=spider_id, expire_seconds=expire_seconds)
    count = Redis().client.llen(redis_key)
    LOGGER.info(f"[队列]任务队列初始化完成 -> 单条模式 key={redis_key}, row={count}, count={len(rows)}")

    return count


def _init_redis_batch(batch_id: str, batch_size: int, spider_id: str, plat_code: str, rows: List[BatchTaskItem], expire_seconds: int):
    redis_key = redis_key_util.get_task_queue_key(batch_id, spider_id)
    Redis().client.delete(redis_key)

    batch_list = []
    random.shuffle(rows)
    for row in rows:
        task = row.dict()
        if plat_code:
            task["platCode"] = plat_code
        batch_list.append(task)
        if len(batch_list) >= batch_size:
            request_id = str(uuid.uuid4())
            batch_row_data = {
                "requestId": request_id,
                "data": batch_list
            }
            # 任务入队
            Redis().client.lpush(redis_key, json.dumps(batch_row_data))
            # 加入重试源数据集合
            add_to_retry_source_mapper(request_id, batch_row_data, redis_key)
            batch_list = []
    if batch_list:
        request_id = str(uuid.uuid4())
        batch_row_data = {
            "requestId": request_id,
            "data": batch_list
        }
        # 任务入队
        Redis().client.lpush(redis_key, json.dumps(batch_row_data))
        # 加入重试源数据集合
        add_to_retry_source_mapper(request_id, batch_row_data, redis_key)

    # 设置任务队列过期时间：默认12小时自动清理
    set_expire(batch_id, spider_id, expire_seconds)
    count = Redis().client.llen(redis_key)
    LOGGER.info(f"[队列]任务队列初始化完成 -> 批量模式 key={redis_key}, row={count}, count={len(rows)}")

    return len(rows)


def set_expire(batch_id: str, spider_id: str, expire_seconds=None):
    """
    设置任务队列过期时间
    1、分拣后入库：默认1小时（job未启动则清理）
    2、job启动：重置过期时间（限制采集时效）
    :param batch_id:
    :param spider_id:
    :param expire_seconds:
    :return:
    """
    _expire_seconds = expire_seconds or cfg.get_int("ZCBOT_CORE_REDIS_QUEUE_EXPIRE") or 12 * 3600
    redis_key = redis_key_util.get_task_queue_key(batch_id, spider_id)
    Redis().client.expire(redis_key, _expire_seconds)


def add_to_retry_source_mapper(request_id, task_data, task_queue_key):
    """
    加入任务映射队列，用于重试任务源数据
    """
    _data = {
        "queue": task_queue_key,
        "source": task_data,
        "genTime": time_lib.current_timestamp10()
    }
    _expire_seconds = cfg.get_int("ZCBOT_CORE_REDIS_QUEUE_EXPIRE") or 12 * 3600
    Redis().client.set(redis_key_util.get_retry_request_source_key(request_id), json.dumps(_data), ex=_expire_seconds)


# 节点选择，这里未来可做节点负载均衡
def node_balance_choice(nodes: List[str]) -> PortainerNode:
    node_list = node_dao.get_node_list({'portainerId': {'$in': nodes}})
    if node_list:
        node = random.choice(node_list)
    else:
        node = ""
    return node
