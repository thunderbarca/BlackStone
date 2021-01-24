import re

from django.views.generic import View
from django.http import JsonResponse

from backend.models.dockers import TopicName
from backend.models.dockers import Containers

from settings.config import PORT_QUEUE
from settings.config import DOCKER_CLIENT

from librarys.mixin.permission import LoginRequiredMixin
from librarys.utils.strings import get_uuid
from librarys.common.dockers import ImageStop
from librarys.utils.strings import str2int


class DockerOperationView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        action = request.POST.get("action")
        images_id = request.POST.get("images_id")

        search_dict = dict()

        if action == "start":
            obj = TopicName.objects.filter(id=images_id).first()

            if "," in obj.inside_port:
                port_list = []
                port_pattern = re.compile("([0-9]+)")
                ports = port_pattern.findall(obj.inside_port)
                for i in ports:
                    port = str(str2int(i)) if str2int(i) != 0 else "80"
                    port_list.append(port)

                port_list = port_list
            else:
                port = str(str2int(obj.inside_port)) if str2int(obj.inside_port) != 0 else "80"
                port_list = [port]

            port_dict = {}

            out_list = []

            for i in port_list:
                port_get = PORT_QUEUE.get()
                port_dict[i] = port_get
                out_list.append(str(port_get))

            outside = ",".join(out_list)

            info = TopicName.objects.filter(image_tag=obj.image_tag).first()

            if info is None:
                data = {"status": 403, "msg": "无此镜像"}
                return JsonResponse(data, safe=False)

            search_dict['username'] = request.user.username
            search_dict['status'] = "Running"

            # 状态检查
            result = Containers.objects.filter(**search_dict).count()

            if result > 0:
                run_list = []
                result = Containers.objects.filter(**search_dict).all()

                for i in result:
                    run_list.append(i.topic_name)

                result1 = ",".join(run_list)

                data = {"status": 300, "msg": "题目:{}已启动，请先关闭再启动此镜像".format(result1)}
                return JsonResponse(data, safe=False)

            try:

                con = DOCKER_CLIENT.containers.run(image=obj.image_tag, ports=port_dict, detach=True)
                user = str(request.user.username) if str(request.user.username) \
                    else request.session.get("user_name", "")

                Containers.objects.create(id=get_uuid(), username=user, contain=con.id,
                                          inside_port=obj.inside_port, outside_port=outside, topic_name=obj.topic_name,
                                          image_tag=obj.image_tag, status="Running")

                data = {"status": 200, "msg": str(port_dict)}

                return JsonResponse(data, safe=False)

            except Exception as e:

                data = {"status": 403, "msg": f"镜像启动失败，请稍后再试,{str(e)}"}

                return JsonResponse(data, safe=False)

        elif action == "destroy":

            search_dict = dict()

            search_dict['username'] = request.session.get("user_name", "") if request.session.get("user_name",
                                                                                                  "") else request.user.username
            search_dict['status'] = "Running"

            obj = TopicName.objects.filter(id=images_id).first().image_tag
            search_dict["image_tag"] = obj

            search_result = Containers.objects.filter(**search_dict).all()
            if len(search_result) > 0:
                two_result = Containers.objects.filter(**search_dict).first()
                two_result.status = "Stop"
                two_result.save()

                if "," in two_result.outside_port:
                    outside = two_result.outside_port.split(",")
                else:
                    outside = [two_result.outside_port]

                for i in outside:
                    PORT_QUEUE.put_nowait(int(i))

                #  启用子线程关闭容器
                obj = ImageStop(two_result.contain)
                obj.start()

                data = {"status": 200, "msg": "容器已销毁"}
                return JsonResponse(data, safe=False)

            else:
                data = {"status": 403, "msg": "无启动容器"}
                return JsonResponse(data, safe=False)
