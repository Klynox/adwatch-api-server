# Generated by Django 3.1.6 on 2021-03-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20210313_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='has_plan',
        ),
        migrations.AddField(
            model_name='user',
            name='plantype',
            field=models.IntegerField(default=0),
        ),
    ]
