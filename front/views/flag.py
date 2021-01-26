from django.views.generic import View
from django.http import JsonResponse

from backend.models.dockers import TopicName
from backend.models.dockers import Resolver
from backend.models.dockers import Containers
from backend.models.users import Players

from librarys.mixin.permission import LoginRequiredMixin
from librarys.utils.calculation import DynamicValueChallenge


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

        player_name = request.session.get("user_name", False) if request.session.get("user_name", False) \
            else str(request.user.username)

        if player_name is None:
            data = {"status": 403, "msg": "用户未登录"}
            return JsonResponse(data, safe=False)

        _topic = TopicName.objects.filter(id=image_id)

        if _topic.count() == 0:
            data = {"status": 403, "msg": "题目不存在"}
            return JsonResponse(data, safe=False)

        docker_obj = TopicName.objects.filter(id=image_id).first().topic_name

        search_dict3 = dict()
        search_dict3['username'] = player_name
        search_dict3['topic_name'] = docker_obj

        search_result_con = Resolver.objects.filter(**search_dict3).all()

        if len(search_result_con) > 0:
            data = {"status": 403, "msg": "此题已经回答正确"}
            return JsonResponse(data, safe=False)

        first_topic = _topic.first()
        if first_topic.score_type:
            score = _topic.first().score
        else:
            score = DynamicValueChallenge(first_topic.score, Resolver.objects.filter(topic_name=docker_obj).count() + 1)

        if first_topic.flag_type == "static":
            flag_sql = first_topic.flag_string

        else:
            search_dict3["image_tag"] = first_topic.image_tag
            search_dict3["status"] = "Running"
            contain = Containers.objects.filter(**search_dict3).first()

            if contain is None:
                data = {"status": 403, "msg": "回答错误"}
                return JsonResponse(data, safe=False)

            flag_sql = contain.flag_string

        if flag == flag_sql:

            category = first_topic.category.category_name
            play = Players.objects.get(username=player_name)

            Resolver.objects.create(username=player_name, topic_name=docker_obj,
                                    image_tag=first_topic.image_tag,
                                    score=score,
                                    category=category,
                                    address=play.address if play else "",
                                    answer=True)

            data = {"status": 200, "msg": "回答正确"}
            return JsonResponse(data, safe=False)

        else:
            data = {"status": 403, "msg": "回答错误"}
            return JsonResponse(data, safe=False)
