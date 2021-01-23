from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.hashers import make_password, check_password

from backend.models.users import Players

from librarys.utils.strings import get_uuid
from librarys.common.tools import PaginatorResults
from librarys.common.tools import Refresh
from librarys.mixin.permission import LoginRequiredMixin


class RegisterView(View):
    template_name = "front/register.html"

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        address = request.POST.get("school", "")

        captcha = request.POST.get("captcha", "")

        if len(captcha) == 0 or captcha.upper() != request.session.get("valid_code", "").upper():
            data = {"status": 403, "msg": "验证码错误"}
            return JsonResponse(data, safe=False)

        # 无论数据提交是否成功，都要在服务器端刷新一遍验证码
        Refresh(request)

        if len(username) == 0 or len(password) == 0 or len(confirm_password) == 0 or len(address) == 0:
            data = {"status": 403, "msg": "数据不能为空"}
            return JsonResponse(data)

        if Players.objects.filter(username=username).count() > 0:
            data = {"status": 403, "msg": "用户已存在"}
            return JsonResponse(data, safe=False)

        if password != confirm_password:
            data = {"status": 403, "msg": "密码不一致"}
            return JsonResponse(data, safe=False)

        Players.objects.create(id=get_uuid(), username=username, address=address,
                               password=make_password(password=password))

        data = {"status": 200, "msg": "注册成功"}
        return JsonResponse(data, safe=False)


class LoginView(View):
    template_name = "front/login.html"

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        captcha = request.POST.get("captcha", "")  # 获取用户填写的验证码
        username = request.POST.get("username", "")
        passwd = request.POST.get("password", "")

        if len(captcha) == 0 or captcha.upper() != request.session.get("valid_code", "").upper():
            data = {"status": 403, "msg": "验证码错误"}
            return JsonResponse(data, safe=False)

        if len(username) == 0 or len(passwd) == 0:
            data = {"status": 403, "msg": "数据不能为空"}
            return JsonResponse(data)

        if Players.objects.filter(username=username).count() == 0:
            data = {"status": 403, "msg": "用户名或密码错误"}
            return JsonResponse(data, safe=False)

        db_user = Players.objects.filter(username=username).first()
        if check_password(passwd, db_user.password):
            request.session['is_login'] = True
            request.session['user_id'] = db_user.id
            request.session['user_name'] = db_user.username

            data = {"status": 200, "msg": "用户登录成功"}
            return JsonResponse(data, safe=False)

        else:

            data = {"status": 403, "msg": "用户名或密码错误"}
            return JsonResponse(data, safe=False)


class LogoutView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        request.session.flush()  # 清空session
        return redirect(reverse("front_index"))


# ShowPlayersView 是在前台展示所有的玩家，默认按照时间逆序排列
class ShowPlayersView(LoginRequiredMixin, View):
    template_name = "front/players.html"

    def get(self, request):
        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)
        currentPage = int(page)

        user_list, paginator = PaginatorResults(Players, page)

        return render(request, self.template_name, locals())
