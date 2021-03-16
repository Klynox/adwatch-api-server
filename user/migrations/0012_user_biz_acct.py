# Generated by Django 3.1.6 on 2021-03-13 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_bizaccount'),
        ('user', '0011_user_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='biz_acct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bizaccount'),
        ),
    ]
