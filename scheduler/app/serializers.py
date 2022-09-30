from datetime import datetime, timezone

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

import models
from proto import scheduler_pb2


def serialize_schedule(
    schedule: models.CronSchedule | models.DatetimeSchedule | models.IntervalSchedule,
) -> tuple[
    str,
    (
        scheduler_pb2.CronSchedule
        | scheduler_pb2.DatetimeSchedule
        | scheduler_pb2.IntervalSchedule
    ),
]:
    if isinstance(schedule, models.CronSchedule):
        fields_map = {field.name: str(field) for field in schedule.fields}
        return "cron", scheduler_pb2.CronSchedule(**fields_map)
    if isinstance(schedule, models.DatetimeSchedule):
        return "at", scheduler_pb2.DatetimeSchedule(
            timestamp=schedule.run_date.timestamp()
        )
    if isinstance(schedule, models.IntervalSchedule):
        interval = schedule.interval
        days = interval.days
        hours, remainder = divmod(interval.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "interval", scheduler_pb2.IntervalSchedule(
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
    else:
        raise TypeError(
            f"Got a schedule object of an unexpected type: {type(schedule)}"
        )


def deserialize_schedule(
    name: str,
    schedule: scheduler_pb2.CronSchedule | scheduler_pb2.DatetimeSchedule | scheduler_pb2.IntervalSchedule,
) -> (models.CronSchedule | models.DatetimeSchedule | models.IntervalSchedule):
    match name:
        case "cron":
            return CronTrigger(
                year=schedule.year,
                month=schedule.month,
                day=schedule.day,
                week=schedule.week,
                day_of_week=schedule.day_of_week,
                hour=schedule.hour,
                minute=schedule.minute,
                second=schedule.second,
            )
        case "at":
            return DateTrigger(
                run_date=datetime.fromtimestamp(schedule.timestamp, tz=timezone.utc)
            )
        case "interval":
            return IntervalTrigger(
                days=schedule.days,
                hours=schedule.hours,
                minutes=schedule.minutes,
                seconds=schedule.seconds,
            )
        case _:
            raise ValueError(f"Got a schedule of an unexpected name: {name}")
