# Generated by Django 3.1.5 on 2021-01-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_auto_20210122_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicname',
            name='flag_type',
            field=models.CharField(default='static', max_length=32),
        ),
        migrations.AlterField(
            model_name='topicname',
            name='flag_strings',
            field=models.CharField(default='flag{}', max_length=125, null=True),
        ),
    ]
