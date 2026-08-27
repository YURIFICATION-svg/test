from abc import ABCMeta, abstractmethod #추상 클래스를 만드는 기능
from user.domain.user import User

class IUserRepositary(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
