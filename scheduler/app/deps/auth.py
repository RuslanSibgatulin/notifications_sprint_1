from typing import Protocol

from faker import Faker

from models import UserInfo

faker = Faker()


class BaseAuthService(Protocol):
    def get_user_info(self, user_ids: list[str]) -> list[UserInfo]:
        pass


class FakeAuthService(BaseAuthService):
    def get_user_info(self, user_ids: list[str]) -> list[UserInfo]:
        return [
            UserInfo(
                user_id=user_id, username=faker.user_name(), email=faker.free_email()
            )
            for user_id in user_ids
        ]
