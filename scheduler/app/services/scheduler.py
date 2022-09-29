from typing import Callable, Protocol
from apscheduler.executors.base import BaseExecutor
from apscheduler.jobstores.base import BaseJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from models.scheduler import CronSchedule, DatetimeSchedule, IntervalSchedule, Job


class Scheduler(Protocol):
    def add_job(
        self,
        func: Callable,
        trigger: CronSchedule | DatetimeSchedule | IntervalSchedule,
        id: str,
        name: str,
        replace_existing: bool = True,
        *args,
        **kwargs
    ) -> Job:
        pass

    def get_job(self, job_id: str) -> Job:
        pass

    def get_jobs(self) -> list[Job]:
        pass

    def reschedule_job(
        self, job_id: str, trigger: CronSchedule | DatetimeSchedule | IntervalSchedule
    ) -> Job:
        pass

    def pause_job(self, job_id: str) -> Job:
        pass

    def resume_job(self, job_id: str) -> Job:
        pass

    def remove_job(self, job_id: str) -> None:
        pass


def init_scheduler(
    executors: dict[str, BaseExecutor], jobstores: dict[str, BaseJobStore]
):
    scheduler = BackgroundScheduler(executors=executors, jobstores=jobstores)
    scheduler.start()
    yield scheduler
    scheduler.shutdown()
