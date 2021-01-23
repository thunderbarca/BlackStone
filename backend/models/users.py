from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    id = models.CharField(max_length=64, primary_key=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    nickname = models.CharField(max_length=32, blank=True, null=True, verbose_name='昵称')
    sex = models.CharField(max_length=8, default='男')
    is_superuser = models.BooleanField()
    remark = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
    last_ip = models.CharField(max_length=64, default="", verbose_name='最后登录的IP')
    last_time = models.CharField(max_length=32, default="", verbose_name='最后的登录时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return f"<{self.username}> Model"


class Players(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户名')
    address = models.CharField(max_length=64, blank=True, null=True, verbose_name='地址')
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name='密码哈希')

    class Meta:
        verbose_name = '参赛者'
        ordering = ['-create_date']

    def __str__(self):
        return f"<{self.username}> Model"
