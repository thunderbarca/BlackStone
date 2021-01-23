import threading
from settings.config import DOCKER_CLIENT
from settings.config import logger

from backend.models.dockers import TopicName


# 使用线程实现docker镜像部署
class DockerDeploy(threading.Thread):

    def __init__(self, name):
        super(DockerDeploy, self).__init__()
        # threading.Thread.__init__(self)
        self.image_name = name

    def run(self):

        if TopicName.objects.filter(image_tag=self.image_name).count() == 0:
            return

        obj = TopicName.objects.get(image_tag=self.image_name)

        images_local_list = []

        # 获取本地已存在的镜像
        images_list = DOCKER_CLIENT.images.list()

        for i in images_list:
            if len(i.tags) > 0:
                images_local_list.append(i.tags[0])

        # if self.full_address in images_local_list:
        if self.image_name in images_local_list:
            obj.pull_status = "Complete"
            obj.save()

            return

        try:

            DOCKER_CLIENT.images.pull(self.image_name)
            obj.pull_status = "Complete"
            obj.save()

        except Exception as e:
            logger.warning(str(e))
            obj.pull_status = "Failed"
            obj.save()


# 使用线程实现docker镜像删除
class DockerDelete(threading.Thread):

    def __init__(self, name):
        super(DockerDelete, self).__init__()
        # threading.Thread.__init__(self)
        self.image_name = name

    def run(self):

        try:
            images_local_list = []

            # 获取本地已存在的镜像
            images_list = DOCKER_CLIENT.images.list()

            for i in images_list:
                if len(i.tags) > 0:
                    images_local_list.append(i.tags[0])

            if self.image_name in images_local_list:
                docker = DOCKER_CLIENT.images.remove(self.image_name)
                return
        except Exception as e:
            logger.warning(str(e))
            return


# 使用线程实现docker镜像停止
class ImageStop(threading.Thread):

    def __init__(self, name):
        super(ImageStop, self).__init__()
        self.container_id = name

    def run(self):

        try:
            container = DOCKER_CLIENT.containers.get(self.container_id)
            container.stop()

            return True

        except Exception as e:
            logger.warning(str(e))
            return False
