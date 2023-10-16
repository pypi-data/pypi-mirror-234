from dataclasses import dataclass

from ..value_objects import Email
from .entity import Entity


@dataclass(frozen=True)
class UserId:
    value: str


class User(Entity):
    """"""

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def name(self) -> str:
        return self._name

    def __init__(self, id: UserId, email: Email, name: str) -> None:
        self._id = id
        self._email = email
        self._name = name

    @staticmethod
    def create(id: UserId, email: Email, name: str) -> "User":
        return User(id, email, name)
