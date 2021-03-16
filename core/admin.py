from django.contrib import admin
from .models import *

class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', '_type', 'duration', 'created_at', 'duration']
    list_filter = ('_type', 'created_at')


class InviteAdmin(admin.ModelAdmin):
    list_display = ['token', "plan", "used", "created_at"]

admin.site.register(InviteToken, InviteAdmin)
admin.site.register(Plan, PlanAdmin)
