from django.db import models
from backend.models.users import Users
from backend.models.category import Category


class TopicName(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    topic_name = models.CharField(max_length=30, unique=True)  # 题目名
    topic_description = models.CharField(max_length=1024)  # 题目描述
    image_img = models.CharField(max_length=45, default='registry.png')  # 镜像图片地址
    image_status = models.CharField(max_length=45)
    image_tag = models.CharField(max_length=45, null=True)
    flag_strings = models.CharField(max_length=125, unique=True, default='flag{}')
    pull_status = models.CharField(max_length=45)  # Running,Failed,Complete
    inside_port = models.CharField(default="80", max_length=126)
    score = models.IntegerField(default=0)
    display = models.BooleanField(default=True)

    upload_file = models.CharField(default="s1riu5", max_length=125)

    # 一对多外键设置，'多'的模型类设置外键，注意需要带参数on_delete
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="镜像分类", related_name='category')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="所属用户")

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return f"<{self.topic_name} Images Model>"


class Containers(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    username = models.CharField(max_length=30)
    image_id = models.CharField(max_length=512)
    image_tag = models.CharField(max_length=216)
    topic_name = models.CharField(max_length=216, default="1")
    inside_port = models.CharField(max_length=128)
    outside_port = models.CharField(max_length=128)
    contain = models.CharField(max_length=512)
    status = models.CharField(max_length=512, default="1")  # Running Stop

    def __str__(self):
        return f"<{self.image_tag} Container Model>"


class Resolver(models.Model):
    image_tag = models.CharField(max_length=30, blank=True, null=True, verbose_name='地址')
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户')
    score = models.IntegerField(default=0)
    topic_name = models.CharField(max_length=30, default="default")
    category = models.CharField(max_length=1024)
    type = models.CharField(max_length=32, default="docker")
    answer = models.BooleanField(default=False)

    def __str__(self):
        return f"<{self.username} Resolver Model>"
