from concurrent import futures

import grpc

from api import AuthService
from core.config import settings
from proto.auth_pb2_grpc import add_AuthServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.max_workers))
    add_AuthServicer_to_server(AuthService(), server)

    server.add_insecure_port(f"[::]:{settings.port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
