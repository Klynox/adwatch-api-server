# Generated by Django 3.1.6 on 2021-03-13 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_bizaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='expire_at',
            field=models.DateTimeField(null=True),
        ),
    ]
