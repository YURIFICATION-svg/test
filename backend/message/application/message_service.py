from message.domain.message import Message
from message.domain.repositary.message_repo import IMRepositary
from user.domain.repositary.user_repo import IUserRepositary


class MService:
    def __init__(
        self,
        message_repo: IMRepositary,
        user_repo: IUserRepositary,
    ):
        self.message_repo = message_repo
        self.user_repo = user_repo

    def send_message(
        self,
        sender_name: str,
        receiver_name: str,
        title: str,
        content: str,
    ):
        receiver = self.user_repo.find_by_name(receiver_name)

        message = Message(
            id=self._generate_id(),
            sender_id=sender_name,
            receiver_id=receiver_name,
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

    @staticmethod
    def _generate_id() -> str:
        import ulid

        return str(ulid.new())
