import queue
import docker
import logging

"""
一些全局属性信息
"""
PORT_QUEUE = queue.Queue()

for i in range(10000, 20000):
    PORT_QUEUE.put(i)

# 初始化docker环境
DOCKER_CLIENT = docker.from_env()

logger = logging.getLogger('django')

WHITE_LIST = ["zip", "rar", "7z"]
