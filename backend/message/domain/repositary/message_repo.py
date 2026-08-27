from abc import ABCMeta, abstractmethod
from message.domain.message import Message

class IMRepositary(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    def read_received(self, user_id: str):
        raise NotImplementedError

    @abstractmethod
    def read_sended(self, user_id: str):
        raise NotImplementedError

    @abstractmethod
    def find(self, message_id: str):
        raise NotImplementedError   