import grpc
from dependency_injector.wiring import Provide, inject
from grpc_interceptor.exceptions import InvalidArgument, NotFound

import models
from containers import Container
from proto import scheduler_pb2, scheduler_pb2_grpc
from serializers import deserialize_schedule, serialize_schedule
from services.notifications.base import BaseNotificationTask, NotificationTasksRegistry
from services.scheduler import Scheduler


class NotificationsSchedulerService(scheduler_pb2_grpc.NotificationsSchedulerServicer):
    @inject
    def __init__(
        self,
        scheduler: Scheduler = Provide[Container.scheduler],
        registry: NotificationTasksRegistry = Provide[Container.registry],
    ):
        self._scheduler = scheduler
        self._registry = registry

    def ListNotifications(
        self, request: scheduler_pb2.Empty, context: grpc.ServicerContext
    ) -> scheduler_pb2.NotificationsList:
        tasks: list[BaseNotificationTask] = self._registry.get_tasks()
        return scheduler_pb2.NotificationsList(
            notifications=[task.name for task in tasks]
        )

    def AddJob(
        self, request: scheduler_pb2.AddJobRequest, context: grpc.ServicerContext
    ) -> scheduler_pb2.Job:
        task: BaseNotificationTask | None = self._registry.get_task(
            request.notification
        )
        if not task:
            raise NotFound("Notification not found")

        schedule_name = request.WhichOneof("schedule")

        if not schedule_name:
            raise InvalidArgument("You should specify schedule")

        schedule = getattr(request, schedule_name)
        trigger = deserialize_schedule(schedule_name, schedule)

        job: models.Job = self._scheduler.add_job(
            func=task,
            trigger=trigger,
            id=task.name,
            name=request.description,
            replace_existing=True,
        )
        job_response = scheduler_pb2.Job(
            notification=job.id,
            description=job.name,
            **{schedule_name: schedule},
            next_run_time=int(job.next_run_time.timestamp()),
        )
        return job_response

    def GetJob(
        self, request: scheduler_pb2.GetJobRequest, context: grpc.ServicerContext
    ) -> scheduler_pb2.Job:
        job: models.Job | None = self._scheduler.get_job(request.notification)
        if not job:
            raise NotFound("Job not found")

        schedule_name, schedule = serialize_schedule(job.trigger)
        job_response = scheduler_pb2.Job(
            notification=job.id,
            description=job.name,
            **{schedule_name: schedule},
            next_run_time=int(job.next_run_time.timestamp()),
        )
        return job_response

    def ListJobs(
        self, request: scheduler_pb2.Empty, context: grpc.ServicerContext
    ) -> scheduler_pb2.JobList:
        jobs: list[models.Job] = self._scheduler.get_jobs()
        jobs_response = []

        for job in jobs:
            schedule_name, schedule = serialize_schedule(job.trigger)
            job_response = scheduler_pb2.Job(
                notification=job.id,
                description=job.name,
                **{schedule_name: schedule},
                next_run_time=int(job.next_run_time.timestamp()),
            )
            jobs_response.append(job_response)

        return scheduler_pb2.JobList(jobs=jobs_response)

    def RescheduleJob(
        self, request: scheduler_pb2.RescheduleJobRequest, context: grpc.ServicerContext
    ) -> scheduler_pb2.Job:
        task: BaseNotificationTask | None = self._registry.get_task()
        if not task:
            raise NotFound("Job not found")

        schedule_name = request.WhichOneOf("schedule")
        if not schedule_name:
            raise InvalidArgument("You should specify schedule")

        schedule = getattr(request, schedule_name)
        trigger = deserialize_schedule(schedule_name, schedule)

        job: models.Job = self._scheduler.reschedule_job(
            job_id=task.name, trigger=trigger
        )

        job_response = scheduler_pb2.Job(
            notification=job.id,
            description=job.name,
            **{schedule_name: schedule},
            next_run_time=int(job.next_run_time.timestamp()),
        )
        return job_response

    def PauseJob(
        self, request: scheduler_pb2.PauseJobRequest, context: grpc.ServicerContext
    ) -> scheduler_pb2.Empty:
        self._scheduler.pause_job(request.notification)
        return scheduler_pb2.Empty()

    def ResumeJob(
        self, request: scheduler_pb2.ResumeJobRequest, context: grpc.ServicerContext
    ) -> scheduler_pb2.Empty:
        self._scheduler.resume_job(request.notification)
        return scheduler_pb2.Empty()
