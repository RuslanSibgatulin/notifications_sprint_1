from datetime import datetime, timedelta
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class CronSchedule(Protocol):
    fields: list[Any]


@runtime_checkable
class DatetimeSchedule(Protocol):
    run_date: datetime


@runtime_checkable
class IntervalSchedule(Protocol):
    interval: timedelta


class Job(Protocol):
    id: str
    name: str
    trigger: CronSchedule | DatetimeSchedule | IntervalSchedule
    next_run: datetime
