from django.shortcuts import render
from django.views.generic import View
from django.db.models import Sum, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from backend.models.users import Players
from backend.models.dockers import Resolver

from librarys.utils.strings import str2int


# 用来显示个人成绩
class PersonalView(View):
    template_name = "front/stat.html"

    def get(self, request, username):
        user_list = []
        score_list = {}
        sort_dict = {}

        user = Players.objects.all()

        for i in user:
            user_list.append(i.username)

        result = Resolver.objects.filter(answer=True).filter(username__in=user_list).values('username').annotate(
            Sum('score')).annotate(Count('username'))

        for i, line in enumerate(result):
            sort_dict[line["username"]] = i + 1
            score_list[line["username"]] = line["score__sum"]

        try:
            key1 = sort_dict[username]
            score = score_list[username]
        except KeyError:
            key = 0
            score = 0
            answer_list = []
            score_list = []
            return render(request, self.template_name, locals())

        answer_list = Resolver.objects.filter(answer=True).filter(username=username).all()

        # 从前端获取当前的页码数,默认为1
        page = request.GET.get('page', 1)

        # 把当前的页码数转换成整数类型
        currentPage = str2int(page) if str2int(page) == 0 else 1

        # 生成paginator对象,定义每页显示15条记录
        paginator = Paginator(answer_list, 15)

        try:
            score_list = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            score_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            score_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        return render(request, self.template_name, locals())
