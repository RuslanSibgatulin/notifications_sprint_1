from typing import Generator, Iterable, Protocol

import grpc

from deps.auth.proto.auth_pb2 import ListUsersRequest, User
from deps.auth.proto.auth_pb2_grpc import AuthStub
from models import UserInfo


class BaseAuthService(Protocol):
    def get_user_info(self, user_ids: list[str]) -> Iterable[UserInfo]:
        pass


class AuthService(BaseAuthService):
    def __init__(self, host: str, port: int):
        self._target = f"{host}:{port}"

    def get_user_info(self, user_ids: list[str]) -> Generator[UserInfo, None, None]:
        with grpc.insecure_channel(self._target) as channel:
            stub = AuthStub(channel)
            request = ListUsersRequest(user_ids=user_ids)
            stream: Iterable[User] = stub.ListUsers(request)

            for user in stream:
                yield UserInfo(
                    user_id=user.user_id, username=user.username, email=user.email
                )
