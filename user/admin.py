from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'email', 'usertype', 'complete']
    list_filter = ['complete', 'usertype']

class PasswordRecoveryAdmin(admin.ModelAdmin):
    list_display = ['token', 'user', 'used']

admin.site.register(User, UserAdmin)
admin.site.register(Default)
admin.site.register(PasswordRecovery, PasswordRecoveryAdmin)
