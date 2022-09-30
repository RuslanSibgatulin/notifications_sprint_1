from typing import Generator

import grpc
from faker import Faker

from proto.auth_pb2 import ListUsersRequest, User
from proto.auth_pb2_grpc import AuthServicer


faker = Faker()


class AuthService(AuthServicer):
    def ListUsers(
        self, request: ListUsersRequest, context: grpc.ServicerContext
    ) -> Generator[User, None, None]:
        for user_id in request.user_ids:
            yield User(
                user_id=user_id,
                username=faker.user_name(),
                email=faker.free_email(),
            )
