from django.db import models


class Category(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    category_name = models.CharField(max_length=30, unique=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True, null=True)

    class Meta:
        ordering = ['create_date']

    def __str__(self):
        return f"<{self.category_name} Category Model>"
