from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    _type = models.IntegerField(default=0) #1 for half, 2 for full, 3 for biz
    duration = models.IntegerField(default=1) # 1 for monthly, 2for yearly
    created_at = models.DateTimeField(auto_now_add=False)
    expire_at = models.DateTimeField(auto_now_add=False, null=True)
    active = models.BooleanField(default=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)

    def __str__(self):
        return self.name



class InviteToken(models.Model):
    token = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.biz.name

