from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import Updater


def startScheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(Updater().updatePlan, 'interval', minutes=5)
    scheduler.start()
