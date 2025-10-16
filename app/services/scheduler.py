from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start()

    def schedule(self, func, run_date: datetime, *args, **kwargs):
        self.scheduler.add_job(func, trigger="date", run_date=run_date, args=args, kwargs=kwargs)

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

