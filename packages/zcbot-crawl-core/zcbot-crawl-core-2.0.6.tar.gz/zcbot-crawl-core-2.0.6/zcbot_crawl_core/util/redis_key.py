# -*- coding: UTF-8 -*-


# 采集任务队列
def get_task_queue_key(batch_id: str, spider_id: str):
    return f'zcbot:{batch_id}:{spider_id}'


# 采集任务队列
def get_task_queue_key_for_remove(batch_id: str):
    return f'zcbot:{batch_id}:*'


# 采集重试任务源数据映射
def get_retry_request_source_key(request_id: str):
    return f'zcbot:request-source:{request_id}'


# 测试
if __name__ == '__main__':
    pass
