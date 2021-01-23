from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render
from django.shortcuts import reverse
from django.http import JsonResponse

from backend.models.users import Users

from librarys.utils.strings import get_now_time
from librarys.common.tools import Refresh


class LoginView(View):
    template_name = "backend/login.html"

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def post(request):
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        captcha = request.POST.get("captcha", None)

        if request.session["valid_code"].lower() != captcha.lower():
            data = {"status": 403, "msg": "验证码错误"}
            return JsonResponse(data, safe=False)

        user = authenticate(username=username, password=password)

        if user is not None:

            # login方法实现登录
            login(request, user)

            # 更新用户登录的时间和ip
            user = Users.objects.get(username=username)
            user.last_time = get_now_time()
            user.last_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            user.save()

            data = {"status": 200, "url_jump": reverse("back_index")}
            return JsonResponse(data, safe=False)

        else:
            # 无论数据提交是否成功，都要在服务器端刷新一遍验证码
            Refresh(request)

            # res = requests.get("http://127.0.0.1:8000/get_valid_img")
            data = {"status": 403, "msg": "用户名或者是密码错误"}
            return JsonResponse(data, safe=False)
