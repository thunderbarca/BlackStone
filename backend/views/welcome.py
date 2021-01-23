from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from backend.models.users import Users
from backend.models.users import Players
from backend.models.dockers import TopicName
from backend.models.category import Category

from librarys.mixin.permission import AdminRequiredMixin


class WelcomeView(AdminRequiredMixin, View):
    template_name = "backend/page/welcome.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        users_nums = Users.objects.count()
        players_nums = Players.objects.count()
        topic_nums = TopicName.objects.count()
        category_nums = Category.objects.count()

        return render(request, self.template_name, locals())
