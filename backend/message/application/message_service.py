from ulid import ULID
from dependency_injector.wiring import Provide
from fastapi import Depends, HTTPException

from message.domain.message import Message
from message.domain.repositary.message_repo import IMRepositary
from user.domain.repositary.user_repo import IUserRepositary
from containers import Container


class MService:
    def __init__(
        self,
        message_repo: IMRepositary = Depends(Provide[Container.message_repo]),
        user_repo: IUserRepositary = Depends(Provide[Container.user_repo]),
    ):
        self.ulid = ULID()
        self.message_repo = message_repo
        self.user_repo = user_repo

    def send_message(
        self,
        sender_id: str,
        receiver_name: str,
        title: str,
        content: str,
    ):
        receiver = self.user_repo.find_by_name(receiver_name)

        message = Message(
            id=self.ulid.generate(),
            sender_id=sender_id,
            receiver_id=receiver.id,
            title=title,
            content=content,
        )

        self.message_repo.send(message)
        return message

    def read_received_message(self, user_id: str):
        return self.message_repo.read_received(user_id)

    def read_sended_message(self, user_id: str):
        return self.message_repo.read_sended(user_id)

    def find_by_id(self, message_id: str):
        return self.message_repo.find(message_id)