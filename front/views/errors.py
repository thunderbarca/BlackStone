from django.shortcuts import render
from django.views.generic import View


class PageNotFound(View):
    """
    404页面
    """
    template_name = "front/404.html"

    def get(self, request, exception):
        return render(request, self.template_name)
