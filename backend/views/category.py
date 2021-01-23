from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import get_uuid
from backend.models.category import Category


class CategoryView(AdminRequiredMixin, View):
    template_name = "backend/page/category/table.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        uid = request.POST.get("id", "")
        action = request.POST.get("action", "")

        if action == "each":
            Category.objects.filter(id=uid).delete()

        elif action == "batch":
            category_id = uid.split(",")
            Category.objects.filter(id__in=category_id).delete()

        else:
            data = {"status": 403, "msg": "方式错误"}
            return JsonResponse(data, safe=False)

        data = {"status": 200, "msg": "标签删除成功"}
        return JsonResponse(data, safe=False)


# ImageAddView 管理后端添加镜像
class CategoryAddView(AdminRequiredMixin, View):
    template_name = "backend/page/category/add.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(xframe_options_exempt)
    def post(self, request):
        category = request.POST.get("category", "")

        if len(category) == 0:
            data = {"status": 403, "msg": "请提供标签名"}
            return JsonResponse(data, safe=False)

        if Category.objects.filter(category_name=category).count() != 0:
            data = {"status": 403, "msg": "标签已存在"}
            return JsonResponse(data, safe=False)

        Category.objects.create(id=get_uuid(), category_name=category)

        data = {"status": 200, "msg": "标签创建成功"}
        return JsonResponse(data, safe=False)


# CategoryEditView 管理后端更新标签
class CategoryEditView(AdminRequiredMixin, View):
    template_name = "backend/page/category/edit.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        id_str = request.GET.get("category_id", "")

        if Category.objects.filter(id=id_str).count() == 0:
            data = {"status": 403, "msg": "标签不存在"}
            return JsonResponse(data, safe=False)

        category = Category.objects.get(id=id_str)

        return render(request, self.template_name, {"category": category})

    @staticmethod
    def post(request):
        id_str = request.POST.get("category_id", "")
        name = request.POST.get("name", "")

        if Category.objects.filter(id=id_str).count() == 0:
            data = {"status": 403, "msg": "标签不存在"}
            return JsonResponse(data, safe=False)

        category = Category.objects.get(id=id_str)
        category.category_name = name
        category.save()

        data = {"status": 200, "msg": "修改完成"}
        return JsonResponse(data, safe=False)
