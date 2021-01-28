from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.hashers import make_password

from backend.models.users import Players

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import get_uuid


class PlayersView(AdminRequiredMixin, View):
    template_name = "backend/page/players/table.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        # 从前端获取当前的页码数,默认为1
        # page = int(request.GET.get('page', 1))
        #
        # user_list, nums = BackPaginatorResults(Players, page)

        return render(request, self.template_name)

    @staticmethod
    def post(request):
        uid = request.POST.get("id", "")
        action = request.POST.get("action", "")

        if action == "each":
            Players.objects.filter(id=uid).delete()

        elif action == "batch":
            user_id = uid.split(",")
            Players.objects.filter(id__in=user_id).delete()

        else:
            data = {"status": 403, "msg": "删除用户失败"}
            return JsonResponse(data, safe=False)

        data = {"status": 200, "msg": "用户删除成功"}
        return JsonResponse(data, safe=False)


class PlayersAddView(AdminRequiredMixin, View):
    template_name = "backend/page/players/add.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(xframe_options_exempt)
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        rept_password = request.POST.get("rept_password")
        address = request.POST.get("school")

        if password != rept_password:
            data = {"status": 403, "msg": "两个密码不一致"}
            return JsonResponse(data, safe=False)

        if Players.objects.filter(username=username).count() > 0:
            data = {"status": 403, "msg": "用户已存在"}
            return JsonResponse(data, safe=False)

        Players.objects.create(id=get_uuid(), username=username, password=make_password(password), address=address)

        data = {"status": 200, "msg": "用户创建成功"}
        return JsonResponse(data, safe=False)


class PlayersEditView(AdminRequiredMixin, View):
    template_name = "backend/page/players/edit.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        player_id = request.GET.get("player_id", "")
        if len(player_id) == 0:
            data = {"status": 403, "msg": "请提供ID"}
            return JsonResponse(data, safe=False)

        player_filter = Players.objects.filter(id=player_id)
        if player_filter.count() == 0:
            data = {"status": 403, "msg": "找不到此用户"}
            return JsonResponse(data, safe=False)

        player = Players.objects.filter(id=player_id).first()

        return render(request, self.template_name, {"player": player})

    @method_decorator(xframe_options_exempt)
    def post(self, request):

        player_id = request.POST.get("id")
        password = request.POST.get("password")
        rept_password = request.POST.get("rept_password")
        address = request.POST.get("address", "")

        if password != rept_password:
            data = {"status": 403, "msg": "两个密码不一致"}
            return JsonResponse(data, safe=False)

        if Players.objects.filter(id=player_id).count() == 0:
            data = {"status": 403, "msg": "用户不存在"}
            return JsonResponse(data, safe=False)

        player = Players.objects.get(id=player_id)
        player.password = make_password(password)
        player.address = address
        player.save()

        data = {"status": 200, "msg": "用户创建成功"}
        return JsonResponse(data, safe=False)
