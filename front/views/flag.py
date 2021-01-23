from django.views.generic import View
from django.http import JsonResponse

from backend.models.dockers import TopicName
from backend.models.dockers import Resolver

from librarys.mixin.permission import LoginRequiredMixin


class CheckFlagView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        image_id = request.POST.get("image_id")
        flag = request.POST.get("flag", "")

        if len(flag) == 0:
            data = {"status": 403, "msg": "必须提供flag"}
            return JsonResponse(data, safe=False)

        if request.user.is_superuser:
            data = {"status": 403, "msg": "管理员用户不能提交"}
            return JsonResponse(data, safe=False)

        player_name = request.session.get("user_name", "")

        flag_sql = TopicName.objects.filter(id=image_id).first().flag_strings

        if flag == flag_sql:
            docker_obj = TopicName.objects.filter(id=image_id).first().topic_name

            search_dict3 = dict()
            search_dict3['username'] = player_name
            search_dict3['topic_name'] = docker_obj

            search_result_con = Resolver.objects.filter(**search_dict3).all()

            if len(search_result_con) > 0:

                data = {"status": 403, "msg": "此题已经回答正确"}
                return JsonResponse(data, safe=False)

            else:

                topic = TopicName.objects.filter(id=image_id).first()

                score = topic.score
                category = topic.category.category_name

                Resolver.objects.create(username=player_name, topic_name=docker_obj,
                                        image_tag=topic.image_tag,
                                        score=score,
                                        category=category,
                                        answer=True)

                data = {"status": 200, "msg": "回答正确"}
                return JsonResponse(data, safe=False)

        else:
            data = {"status": 403, "msg": "回答错误"}
            return JsonResponse(data, safe=False)
