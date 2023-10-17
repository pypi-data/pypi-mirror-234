# -*- coding: UTF-8 -*-


# rabbitmq结果集交换机名称
def get_rabbit_result_exchange_key():
    return f'ex.zcbot_result'


# rabbitmq路由名称
def get_rabbit_result_routing_key(batch_id):
    return f'rt.result_{batch_id}'


# rabbitmq结果集队列名称
def get_rabbit_result_queue_key(batch_id):
    return f'qu.result_{batch_id}'


# 测试
if __name__ == '__main__':
    # print(get_rabbit_result_queue_key(210100110011))
    pass
