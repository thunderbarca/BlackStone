import requests

from urllib.parse import urlsplit

from django.shortcuts import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# PaginatorResults 是前台用来将数据信息进行处理的分页函数
def PaginatorResults(models, page: int, offset: int = 10) -> (list, Paginator):
    user_mess = models.objects.all().order_by('create_date')

    # 生成paginator对象,定义每页显示多少条记录
    paginator = Paginator(user_mess, offset)

    # 把当前的页码数转换成整数类型
    currentPage = int(page)

    try:
        user_list = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        user_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        user_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return user_list, paginator


# 从request获取应用全地址
def GenerateHost(request) -> str:
    # request.is_secure()
    # 如果是https则为True，反之为False
    http = urlsplit(request.build_absolute_uri(None)).scheme
    # 获得当前的HTTP或HTTPS
    host = request.META['HTTP_HOST']
    # 获取当前域名
    short_url = http + '://' + host
    return short_url


# 用来刷新验证码的函数
def Refresh(request):
    try:
        captcha_address = f"{GenerateHost(request)}{reverse('captcha')}"
        requests.get(captcha_address)

    except requests.RequestException as e:
        print(e)
