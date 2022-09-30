from __future__ import print_function

import logging

import grpc

import proto.scheduler_pb2 as scheduler_pb2
import proto.scheduler_pb2_grpc as scheduler_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = scheduler_pb2_grpc.NotificationsSchedulerStub(channel)
        response = stub.ListJobs(scheduler_pb2.Empty())
        print(response.jobs)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = scheduler_pb2_grpc.NotificationsSchedulerStub(channel)
        response = stub.ListNotifications(scheduler_pb2.Empty())
        print(response.notifications)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = scheduler_pb2_grpc.NotificationsSchedulerStub(channel)
        response = stub.AddJob(
            scheduler_pb2.AddJobRequest(
                notification="recommend_continue_watching",
                description="sdsd",
                interval=scheduler_pb2.IntervalSchedule(minutes=1),
            )
        )
        print(response)


if __name__ == "__main__":
    logging.basicConfig()
    run()
