import json

from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import reverse
from django.db.models import Count
from django.db.models import Sum

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import str2int

from backend.models.users import Users
from backend.models.users import Players
from backend.models.dockers import TopicName
from backend.models.category import Category
from backend.models.dockers import Containers
from backend.models.dockers import Resolver


class IndexAPIView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        result = {'homeInfo': {'title': '首页', 'href': reverse("back_welcome")},
                  'logoInfo': {'title': '后台管理', 'image': '/static/backend/images/logo.png', 'href': ''},
                  'menuInfo': [
                      {'title': '常规管理', 'icon': 'fa fa-address-book', 'href': '', 'target': '_self', 'child': [
                          {'title': '主页设置', 'href': '', 'icon': 'fa fa-home', 'target': '_self', 'child': [
                              {'title': '欢迎界面', 'href': reverse("back_welcome"), 'icon': 'fa fa-tachometer',
                               'target': '_self'},
                              {'title': '管理用户', 'href': reverse('back_user'), 'icon': 'fa fa-tachometer',
                               'target': '_self'}]},
                          {'title': '标签管理', 'href': reverse("back_category_show"), 'icon': 'fa fa-window-maximize',
                           'target': '_self'},
                          {'title': '题目部署', 'href': reverse("back_images_show"), 'icon': 'fa fa-flag-o',
                           'target': '_self'},
                          {'title': '比赛用户', 'href': reverse("back_players"), 'icon': 'fa fa-snowflake-o',
                           'target': '_self'},
                          {'title': '容器管理', 'href': reverse("back_container_show"), 'icon': 'fa fa-file-text',
                           'target': '_self'},
                          {'title': '答题记录', 'href': reverse("back_resolver_show"), 'icon': 'fa fa-lemon-o',
                           'target': '_self'},
                          {'title': '成绩管理', 'href': '', 'icon': 'fa fa-anchor', 'target': '_self', 'child': [
                              {'title': '个人成绩', 'href': reverse("back_person_score_show"), 'icon': 'fa fa-bell-o',
                               'target': '_self'},
                              # {'title': '团队成绩', 'href': reverse('back_user'), 'icon': 'fa fa-bell',
                              #  'target': '_self'}
                          ]},
                          {'title': '系统设置', 'href': reverse("back_setting"), 'icon': 'fa fa-gears', 'target': '_self'},

                      ]},

                  ]
                  }

        return JsonResponse(result)


class UserApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1
        currentPage = str2int(request.GET.get('page', 1))
        countList = str2int(request.GET.get('limit', 15))

        user_list = Users.objects.all().order_by('create_date')
        paginator_user = user_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = list()

        for i, v in enumerate(paginator_user):
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList), 'username': v.username, 'sex': v.sex,
                        'super': v.is_superuser,
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'experience': 255,
                        'last_ip': v.last_ip, 'last_time': v.last_time, 'classify': '作家', 'score': 57, "uid": v.id}
            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(user_list), 'data': new_list}

        return JsonResponse(user)


class PlayersApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1
        currentPage = str2int(request.GET.get('page', 1))
        countList = str2int(request.GET.get('limit', 10))

        player_dict = {}
        search_params = json.loads(request.GET.get('searchParams', "{}"))

        for index in search_params:
            if len(search_params[index]) > 0:
                player_dict[index] = search_params[index]

        if len(player_dict) == 0:
            user_list = Players.objects.all().order_by('create_date')
        else:
            user_list = Players.objects.filter(**player_dict).order_by('create_date')

        paginator_user = user_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = list()

        for i, v in enumerate(paginator_user):
            score = Resolver.objects.filter(username=v.username).aggregate(nums=Sum('score'))

            new_dict = {'id': i + 1 + ((currentPage - 1) * countList), 'username': v.username,
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'address': v.address, "score": score.get("nums"), "uid": v.id}
            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(user_list), 'data': new_list}

        return JsonResponse(user)


class ImagesApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1
        countList = str2int(request.GET.get('limit', 15))
        currentPage = str2int(request.GET.get('page', 1))

        search_dict = {}
        search_params = json.loads(request.GET.get('searchParams', "{}"))

        for index in search_params:
            if len(search_params[index]) > 0:
                search_dict[index] = search_params[index]

        if len(search_dict) == 0:
            dockers_list = TopicName.objects.all().order_by('create_date')
        else:
            dockers_list = TopicName.objects.filter(**search_dict).order_by('create_date')

        paginator_docker = dockers_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = list()

        for i, v in enumerate(paginator_docker):
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList), 'username': v.user.username,
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'topic_name': v.topic_name,
                        'image_tag': v.image_tag,
                        'pull_status': v.pull_status,
                        'flag_string': v.flag_string,
                        'inside_port': v.inside_port,
                        'score': v.score,
                        'display': v.display,
                        'type': v.score_type,
                        'uid': v.id}

            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(dockers_list), 'data': new_list}

        return JsonResponse(user)


class CategoryApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1
        currentPage = str2int(request.GET.get('page', 1))
        countList = str2int(request.GET.get('limit', 15))

        category_list = Category.objects.all().order_by('create_date')
        paginator_category = category_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = list()

        for i, v in enumerate(paginator_category):
            count = Category.objects.get(id=v.id).category.count()
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList),
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'category': v.category_name,
                        'nums': count,
                        'category_id': v.id}

            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(category_list), 'data': new_list}

        return JsonResponse(user)


class ContainerApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1

        countList = str2int(request.GET.get('limit', 15))
        currentPage = str2int(request.GET.get('page', 1))

        container_list = Containers.objects.all().order_by('create_date')
        paginator_container = container_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = []

        for i, v in enumerate(paginator_container):
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList),
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'username': v.username,
                        'image_tag': v.image_tag,
                        'topic_name': v.topic_name,
                        'status': v.status,
                        'uid': v.id}

            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(container_list), 'data': new_list}

        return JsonResponse(user)


class ResolverApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1

        countList = str2int(request.GET.get('limit', 15))
        currentPage = str2int(request.GET.get('page', 1))

        resolver_list = Resolver.objects.all().order_by('create_date')
        paginator_container = resolver_list[(currentPage - 1) * countList:currentPage * countList]

        new_list = []

        for i, v in enumerate(paginator_container):
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList),
                        'create': v.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'username': v.username,
                        'image_tag': v.image_tag,
                        'topic_name': v.topic_name,
                        'score': v.score,
                        'uid': v.id}

            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(resolver_list), 'data': new_list}

        return JsonResponse(user)


class PersonScoreApiView(AdminRequiredMixin, View):

    @staticmethod
    def get(request):
        # 从前端获取当前的页码数,默认为1

        countList = str2int(request.GET.get('limit', 15))
        currentPage = str2int(request.GET.get('page', 1))

        person_list = []
        user = Players.objects.all()

        for i in user:
            person_list.append(i.username)

        info = Resolver.objects.filter(username__in=person_list).values('username').annotate(
            Sum('score')).annotate(Count('username')).order_by("-score__sum")

        paginator_container = info[(currentPage - 1) * countList:currentPage * countList]

        new_list = []

        for i, v in enumerate(paginator_container):
            new_dict = {'id': i + 1 + ((currentPage - 1) * countList),
                        'username': v.get("username", ""),
                        'score': v.get("score__sum", ""),
                        'nums': v.get("username__count", ""),
                        'address': Players.objects.get(username=v.get("username", "")).address
                        }

            new_list.append(new_dict)

        user = {'code': 0, 'msg': '', 'count': len(info), 'data': new_list}

        return JsonResponse(user)
