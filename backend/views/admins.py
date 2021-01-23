from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import get_uuid

from backend.models.users import Users


class UserView(AdminRequiredMixin, ListView):
    template_name = "backend/page/admins/user.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        uid = request.POST.get("id", "")
        action = request.POST.get("action", "")

        if len(uid) == 0:
            data = {"status": 403, "msg": "请提供ID"}
            return JsonResponse(data, safe=False)

        if action == "each":
            Users.objects.filter(id=uid).delete()

        elif action == "batch":
            user_id = uid.split(",")
            Users.objects.filter(id__in=user_id).delete()

        else:
            data = {"status": 403, "msg": "方式错误"}
            return JsonResponse(data, safe=False)

        data = {"status": 200, "msg": "用户删除成功"}
        return JsonResponse(data, safe=False)


class AddUserView(AdminRequiredMixin, ListView):
    template_name = "backend/page/admins/add.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(xframe_options_exempt)
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        sex = request.POST.get("sex")
        rept_password = request.POST.get("rept_password")
        remark = request.POST.get("remark")

        if password != rept_password:
            data = {"status": 403, "msg": "两个密码不一致"}
            return JsonResponse(data, safe=False)

        if Users.objects.filter(username=username).count() != 0:
            data = {"status": 403, "msg": "用户已存在"}
            return JsonResponse(data, safe=False)

        if sex == "1":
            sex = "男"
        elif sex == "0":
            sex = "女"

        Users.objects.create_user(id=get_uuid(), username=username, password=password, is_superuser=True, sex=sex,
                                  remark=remark)

        data = {"status": 200, "msg": "用户创建成功"}
        return JsonResponse(data, safe=False)
