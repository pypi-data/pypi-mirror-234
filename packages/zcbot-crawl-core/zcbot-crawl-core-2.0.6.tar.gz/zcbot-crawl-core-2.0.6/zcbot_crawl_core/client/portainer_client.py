# -*- coding: utf-8 -*-
import json
import requests
from ..util import logger
from ..util.decator import singleton
from ..model.entity import PortainerNode, BatchSpider

LOGGER = logger.get('容器')


@singleton
class PortainerClient(object):
    """
    Portainer客户端简易封装
    """

    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400'
        # 客户端
        self.create_api = '{}/api/endpoints/{}/docker/containers/create?name={}'
        self.start_api = '{}/api/endpoints/{}/docker/containers/{}/start'
        self.stop_api = '{}/api/endpoints/{}/docker/containers/{}/kill'

    def create_container(self, node: PortainerNode, spider: BatchSpider, container_name: str, param_data):
        container_conf = {
            "Cmd": [
                "/bin/sh",
                "-c",
                spider.param % param_data
            ],
            "Env": spider.env,
            "Image": spider.dockerImage
        }

        rs = requests.post(
            url=self.create_api.format(node.apiBaseUrl, node.endpointId, container_name),
            headers={
                'X-API-Key': node.apiToken,
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json;charset=UTF-8',
            },
            data=json.dumps(container_conf)
        )
        if rs:
            data = json.loads(rs.text) or {}
            if data.get('Id', None):
                id = data.get('Id', '')
                LOGGER.info(f'创建成功: id={id}, endpoint={node.endpointId} name={container_name}')
                return id

        LOGGER.error(f'创建失败: result={rs.text}, endpoint={node.endpointId} name={container_name}')

    def start(self, node: PortainerNode, container_id: str):
        rs = requests.post(
            url=self.start_api.format(node.apiBaseUrl, node.endpointId, container_id),
            headers={
                'X-API-Key': node.apiToken,
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json;charset=UTF-8',
            }
        )
        if rs and rs.status_code in [204, 200]:
            LOGGER.info(f'启动成功: id={container_id}')
            return container_id

        LOGGER.error(f'启动失败: id={container_id}')

    def stop(self, node: PortainerNode, container_id: str):
        rs = requests.post(
            url=self.stop_api.format(node.apiBaseUrl, node.endpointId, container_id),
            headers={
                'X-API-Key': node.apiToken,
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json;charset=UTF-8',
            }
        )
        if rs and rs.status_code in [204, 200]:
            LOGGER.info(f'停止成功: id={container_id}')
            return container_id

        LOGGER.error(f'停止失败: id={container_id}')
