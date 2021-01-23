from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views.generic import View

from backend.models.dockers import Resolver
from backend.models.dockers import TopicName

from librarys.mixin.permission import LoginRequiredMixin


class TopicsView(LoginRequiredMixin, View):
    template_name = "front/topics.html"

    def get(self, request):

        search_dict = dict()
        user_resolver = []

        search_dict['username'] = request.user.username

        result = Resolver.objects.filter(**search_dict).all()

        for j in result:
            user_resolver.append(j.topic_name)

        docker_list = TopicName.objects.filter(pull_status="Complete").all().order_by("create_date")

        docker_images = []

        for n in docker_list:
            docker_images.append(n.image_tag)

        category_info = []
        for i in docker_list:
            category_info.append(i.category)

        category_info = sorted(set(category_info), key=category_info.index)

        return render(request, self.template_name,
                      {"category": category_info, "user_resolver": user_resolver, "docker_images": docker_images})


class TopicSingleView(LoginRequiredMixin, View):
    template_name = "front/topic.html"

    def get(self, request, topic_id):
        topic = TopicName.objects.filter(id=topic_id)

        if topic.count() == 0:
            return redirect(reverse("front_topics"))

        quest = topic.first()

        result = Resolver.objects.filter(topic_name=quest.topic_name).order_by("create_date").all()[0:10]

        return render(request, self.template_name, {"info": quest, "result": result})
