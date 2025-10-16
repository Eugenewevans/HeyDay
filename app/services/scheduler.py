from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start()

    def schedule(self, func, run_date: datetime, *args, **kwargs):
        self.scheduler.add_job(func, trigger="date", run_date=run_date, args=args, kwargs=kwargs)

    def schedule_every_cron(self, cron: str, func, *args, **kwargs) -> None:
        # cron like "*/5 * * * *" (every 5 min)
        minute, hour, day, month, dow = cron.split()
        trigger = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=dow)
        self.scheduler.add_job(func, trigger=trigger, args=args, kwargs=kwargs, replace_existing=True, id=f"{func.__name__}")

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

