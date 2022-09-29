# flake8: noqa
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scheduler.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fscheduler.proto\x12\x16NotificationsScheduler"\x07\n\x05\x45mpty"*\n\x11NotificationsList\x12\x15\n\rnotifications\x18\x01 \x03(\t"\x84\x02\n\x0c\x43ronSchedule\x12\x11\n\x04year\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x12\n\x05month\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x10\n\x03\x64\x61y\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x11\n\x04week\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x18\n\x0b\x64\x61y_of_week\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x11\n\x04hour\x18\x06 \x01(\tH\x05\x88\x01\x01\x12\x13\n\x06minute\x18\x07 \x01(\tH\x06\x88\x01\x01\x12\x13\n\x06second\x18\x08 \x01(\tH\x07\x88\x01\x01\x42\x07\n\x05_yearB\x08\n\x06_monthB\x06\n\x04_dayB\x07\n\x05_weekB\x0e\n\x0c_day_of_weekB\x07\n\x05_hourB\t\n\x07_minuteB\t\n\x07_second"%\n\x10\x44\x61tetimeSchedule\x12\x11\n\ttimestamp\x18\x01 \x01(\x03"\x90\x01\n\x10IntervalSchedule\x12\x11\n\x04\x64\x61ys\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x12\n\x05hours\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x14\n\x07minutes\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x14\n\x07seconds\x18\x04 \x01(\x05H\x03\x88\x01\x01\x42\x07\n\x05_daysB\x08\n\x06_hoursB\n\n\x08_minutesB\n\n\x08_seconds"\xff\x01\n\x03Job\x12\x14\n\x0cnotification\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x34\n\x04\x63ron\x18\x03 \x01(\x0b\x32$.NotificationsScheduler.CronScheduleH\x00\x12\x36\n\x02\x61t\x18\x04 \x01(\x0b\x32(.NotificationsScheduler.DatetimeScheduleH\x00\x12<\n\x08interval\x18\x05 \x01(\x0b\x32(.NotificationsScheduler.IntervalScheduleH\x00\x12\x15\n\rnext_run_time\x18\x06 \x01(\x03\x42\n\n\x08schedule"4\n\x07JobList\x12)\n\x04jobs\x18\x01 \x03(\x0b\x32\x1b.NotificationsScheduler.Job"\xf2\x01\n\rAddJobRequest\x12\x14\n\x0cnotification\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x34\n\x04\x63ron\x18\x03 \x01(\x0b\x32$.NotificationsScheduler.CronScheduleH\x00\x12\x36\n\x02\x61t\x18\x04 \x01(\x0b\x32(.NotificationsScheduler.DatetimeScheduleH\x00\x12<\n\x08interval\x18\x05 \x01(\x0b\x32(.NotificationsScheduler.IntervalScheduleH\x00\x42\n\n\x08schedule"%\n\rGetJobRequest\x12\x14\n\x0cnotification\x18\x01 \x01(\t"\xe4\x01\n\x14RescheduleJobRequest\x12\x14\n\x0cnotification\x18\x01 \x01(\t\x12\x34\n\x04\x63ron\x18\x02 \x01(\x0b\x32$.NotificationsScheduler.CronScheduleH\x00\x12\x36\n\x02\x61t\x18\x03 \x01(\x0b\x32(.NotificationsScheduler.DatetimeScheduleH\x00\x12<\n\x08interval\x18\x04 \x01(\x0b\x32(.NotificationsScheduler.IntervalScheduleH\x00\x42\n\n\x08schedule"\'\n\x0fPauseJobRequest\x12\x14\n\x0cnotification\x18\x01 \x01(\t"(\n\x10ResumeJobRequest\x12\x14\n\x0cnotification\x18\x01 \x01(\t2\xe5\x04\n\x16NotificationsScheduler\x12]\n\x11ListNotifications\x12\x1d.NotificationsScheduler.Empty\x1a).NotificationsScheduler.NotificationsList\x12L\n\x06\x41\x64\x64Job\x12%.NotificationsScheduler.AddJobRequest\x1a\x1b.NotificationsScheduler.Job\x12L\n\x06GetJob\x12%.NotificationsScheduler.GetJobRequest\x1a\x1b.NotificationsScheduler.Job\x12J\n\x08ListJobs\x12\x1d.NotificationsScheduler.Empty\x1a\x1f.NotificationsScheduler.JobList\x12Z\n\rRescheduleJob\x12,.NotificationsScheduler.RescheduleJobRequest\x1a\x1b.NotificationsScheduler.Job\x12R\n\x08PauseJob\x12\'.NotificationsScheduler.PauseJobRequest\x1a\x1d.NotificationsScheduler.Empty\x12T\n\tResumeJob\x12(.NotificationsScheduler.ResumeJobRequest\x1a\x1d.NotificationsScheduler.Emptyb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "scheduler_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _EMPTY._serialized_start = 43
    _EMPTY._serialized_end = 50
    _NOTIFICATIONSLIST._serialized_start = 52
    _NOTIFICATIONSLIST._serialized_end = 94
    _CRONSCHEDULE._serialized_start = 97
    _CRONSCHEDULE._serialized_end = 357
    _DATETIMESCHEDULE._serialized_start = 359
    _DATETIMESCHEDULE._serialized_end = 396
    _INTERVALSCHEDULE._serialized_start = 399
    _INTERVALSCHEDULE._serialized_end = 543
    _JOB._serialized_start = 546
    _JOB._serialized_end = 801
    _JOBLIST._serialized_start = 803
    _JOBLIST._serialized_end = 855
    _ADDJOBREQUEST._serialized_start = 858
    _ADDJOBREQUEST._serialized_end = 1100
    _GETJOBREQUEST._serialized_start = 1102
    _GETJOBREQUEST._serialized_end = 1139
    _RESCHEDULEJOBREQUEST._serialized_start = 1142
    _RESCHEDULEJOBREQUEST._serialized_end = 1370
    _PAUSEJOBREQUEST._serialized_start = 1372
    _PAUSEJOBREQUEST._serialized_end = 1411
    _RESUMEJOBREQUEST._serialized_start = 1413
    _RESUMEJOBREQUEST._serialized_end = 1453
    _NOTIFICATIONSSCHEDULER._serialized_start = 1456
    _NOTIFICATIONSSCHEDULER._serialized_end = 2069
# @@protoc_insertion_point(module_scope)