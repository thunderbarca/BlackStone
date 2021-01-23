from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from librarys.mixin.permission import AdminRequiredMixin


class SettingMenu(AdminRequiredMixin, View):
    template_name = "backend/page/setting.html"

    @method_decorator(xframe_options_exempt)
    def get(self, request):
        return render(request, self.template_name)
