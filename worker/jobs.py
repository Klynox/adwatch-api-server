from core.models import Plan
from django.utils import timezone
class Updater():
    def updatePlan(self):
        plans = Plan.objects.filter(active=True)
        for plan in plans:
            now = timezone.now()
            if plan.expire_at <= now:
                users = plan.user_set.all()
                for user in users:
                    user.usertype, user.plan, user.biz_acct = 0, None, None
                    user.save()
                plan.active = False
                plan.save()
