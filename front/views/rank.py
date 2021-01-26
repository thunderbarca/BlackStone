from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models.users import Players
from backend.models.dockers import Resolver

from django.db.models import Sum
from django.db.models import Count
from django.db.models import Max


class RankView(View):
    template_name = "front/ranking.html"

    def get(self, request):
        user_list = []

        user = Players.objects.all()

        for i in user:
            user_list.append(i.username)

        info = Resolver.objects.filter(username__in=user_list).values('username').annotate(
            Sum('score')).annotate(Count('username')).annotate(Max('address')).order_by("-score__sum")

        # 生成paginator对象,定义每页显示15条记录
        paginator = Paginator(info, 15)

        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)

        # 把当前的页码数转换成整数类型
        currentPage = int(page)

        try:
            score_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            score_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            score_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        return render(request, self.template_name, locals())
