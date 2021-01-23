from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin

from backend.models.dockers import Resolver


class ResolverView(AdminRequiredMixin, View):
    template_name = "backend/page/resolver/table.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        # 数据只有清空操作，避免舞弊
        action = request.POST.get("action", "")

        if action == "delete":
            Resolver.objects.all().delete()

        else:
            data = {"status": 403, "msg": "方式错误"}
            return JsonResponse(data, safe=False)

        data = {"status": 200, "msg": "信息删除成功"}
        return JsonResponse(data, safe=False)
