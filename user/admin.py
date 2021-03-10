from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'email', 'usertype', 'complete']
    list_filter = ['complete', 'usertype']

admin.site.register(User, UserAdmin)
