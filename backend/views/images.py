from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import get_uuid
from librarys.utils.strings import str2int
from librarys.utils.files import file_delete
from librarys.common.dockers import DockerDeploy
from librarys.common.dockers import DockerDelete

from backend.models.category import Category
from backend.models.dockers import TopicName

from settings.base import BASE_DIR


def delete_topic(uid: str):
    if TopicName.objects.filter(id=uid).count() > 0:
        topic = TopicName.objects.get(id=uid)
        if topic.image_tag:
            topic_image = topic.image_tag
            docker = DockerDelete(name=topic_image)
            docker.start()

        file_path = BASE_DIR.joinpath("front", topic.upload_file[1:])
        if topic.upload_file != "s1riu5":
            file_delete(file_path)

        TopicName.objects.filter(id=uid).delete()


class ImagesView(AdminRequiredMixin, View):
    template_name = "backend/page/images/table.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        uid = request.POST.get("id", "")
        action = request.POST.get("action", "")

        if action == "each":
            delete_topic(uid)

        elif action == "batch":
            topic_id = uid.split(",")
            for i in topic_id:
                delete_topic(i)

        elif action == "clear":
            # 清空题目
            for i in TopicName.objects.all():
                delete_topic(i.id)

        else:
            data = {"status": 403, "msg": "方式错误"}
            return JsonResponse(data, safe=False)

        data = {"status": 200, "msg": "镜像删除成功"}
        return JsonResponse(data, safe=False)


# ImageAddView 管理后端添加镜像
class ImageAddView(AdminRequiredMixin, View):
    template_name = "backend/page/images/add.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        category = Category.objects.all().order_by("-create_date")

        return render(request, self.template_name, {"category": category})

    @staticmethod
    def post(request):
        topic_title = request.POST.get("title", "")
        topic_image = request.POST.get("tag", "")
        topic_desc = request.POST.get("remark", "")
        topic_display = request.POST.get("display", "1")
        topic_category = request.POST.get("category", "")
        topic_score = request.POST.get("score", "")
        topic_flag = request.POST.get("flag", "")
        topic_ports = request.POST.get("ports", "")
        filename = request.POST.get("name", "")

        if topic_display == "1":
            display = True
        else:
            display = False

        if Category.objects.filter(id=topic_category).count() == 0:
            data = {"status": 403, "msg": "标签不存在"}
            return JsonResponse(data, safe=False)

        if TopicName.objects.filter(topic_name=topic_title).count() != 0:
            data = {"status": 403, "msg": "题目已存在"}
            return JsonResponse(data, safe=False)

        if TopicName.objects.filter(flag_strings=topic_flag).count() != 0:
            data = {"status": 403, "msg": "flag已存在"}
            return JsonResponse(data, safe=False)

        category = Category.objects.filter(id=topic_category).first()

        if len(filename) == 0:
            file_path = "s1riu5"

        else:

            if filename[0:7] != "/static":
                data = {"status": 403, "msg": "文件路径错误"}
                return JsonResponse(data, safe=False)

            file_path = filename

        if len(topic_image) > 0:
            # 如果提供了镜像名称
            docker_name = TopicName.objects.create(id=get_uuid(), topic_name=topic_title,
                                                   topic_description=topic_desc,
                                                   image_tag=topic_image, display=display, score=topic_score,
                                                   flag_strings=topic_flag, inside_port=topic_ports,
                                                   category=category,
                                                   user=request.user, pull_status="Running", upload_file=file_path)

            docker = DockerDeploy(name=topic_image)
            docker.start()
        else:
            docker_name = TopicName.objects.create(id=get_uuid(), topic_name=topic_title,
                                                   topic_description=topic_desc,
                                                   display=display, score=topic_score,
                                                   flag_strings=topic_flag, inside_port=topic_ports,
                                                   category=category,
                                                   user=request.user, pull_status="Complete", upload_file=file_path)

        data = {"status": 200, "msg": "创建成功"}
        return JsonResponse(data, safe=False)


# ImagesEditView 管理后端更新标签
class ImagesEditView(AdminRequiredMixin, View):
    template_name = "backend/page/images/edit.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        id_str = request.GET.get("image_id", "")

        if TopicName.objects.filter(id=id_str).count() == 0:
            data = {"status": 403, "msg": "题目不存在"}
            return JsonResponse(data, safe=False)

        topic_name = TopicName.objects.get(id=id_str)

        return render(request, self.template_name, {"topic": topic_name})

    @staticmethod
    def post(request):
        id_str = request.POST.get("id", "")
        name = request.POST.get("topic_name", "")
        desc = request.POST.get("topic_desc", "")
        ports = request.POST.get("ports", "")
        display = request.POST.get("display", "1")
        score = request.POST.get("score", "")
        flag = request.POST.get("flag", "")

        if display == "1":
            topic_display = True
        else:
            topic_display = False

        topic = TopicName.objects.filter(id=id_str)
        if topic.count() == 0:
            data = {"status": 403, "msg": "数据不存在"}
            return JsonResponse(data, safe=False)

        _topic = TopicName.objects.get(id=id_str)
        if len(name) > 0:
            _topic.topic_name = name

        if len(desc) > 0:
            _topic.topic_description = desc

        if len(ports) > 0:
            _topic.inside_port = ports

        _topic.display = topic_display

        if len(score) > 0:
            _topic.score = str2int(score)

        if len(flag) > 0:
            _topic.flag_strings = flag

        _topic.save()

        data = {"status": 200, "msg": "修改完成"}
        return JsonResponse(data, safe=False)
