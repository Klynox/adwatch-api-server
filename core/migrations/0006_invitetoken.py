# Generated by Django 3.1.6 on 2021-03-13 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_plan_expire_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('biz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bizaccount')),
            ],
        ),
    ]
