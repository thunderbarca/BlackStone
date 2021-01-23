from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin
from librarys.common.dockers import ImageStop

from backend.models.dockers import Containers


class ContainerView(AdminRequiredMixin, View):
    template_name = "backend/page/container/table.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        uid = request.POST.get("id", "")
        action = request.POST.get("action", "")
        operate = request.POST.get("operate", "")

        if operate == "delete":

            if action == "each":
                Containers.objects.filter(id=uid).delete()

            elif action == "batch":
                container_id = uid.split(",")
                Containers.objects.filter(id__in=container_id).delete()

            elif action == "all":
                containers = Containers.objects.all()
                for i in containers:
                    if i.status == "Running":
                        #  启用分线程关闭容器
                        obj = ImageStop(i.contain)
                        obj.start()

                containers.delete()

            else:
                data = {"status": 403, "msg": "方式错误"}
                return JsonResponse(data, safe=False)

            data = {"status": 200, "msg": "容器删除成功"}
            return JsonResponse(data, safe=False)

        elif operate == "stop":
            nums = Containers.objects.filter(id=uid).count()
            if nums > 0:
                container = Containers.objects.get(id=uid)
                container.status = "Stop"
                container.save()

                #  启用分线程关闭容器
                obj = ImageStop(container.contain)
                obj.start()

                data = {"status": 200, "msg": "容器终止"}
                return JsonResponse(data, safe=False)
