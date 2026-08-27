from fastapi import HTTPException

from database import SessionLocal
from message.domain.repositary.message_repo import IMRepositary
from message.domain.message import Message
from message.infra.db_models.message import Message as Message_table

class MRepositary(IMRepositary):
    def send(self, message: Message):
        message_table = Message_table(
            id = message.id,
            sender_id = message.sender_id,
            receiver_id = message.receiver_id,
            title = message.title,
            content = message.content
        )
        try:
            db = SessionLocal()
            db.add(message_table)
            db.commit()
        finally:
            db.close()
        
    def read_received(self, user_id: str):
        with SessionLocal() as db:
            messages = db.query(Message_table).filter(Message_table.receiver_id == user_id).all()

        return [Message(
            id = m.id,
            sender_id = m.sender_id,
            receiver_id = m.receiver_id,
            title = m.title,
            content = m.content
        ) for m in messages]

    def read_sended(self, user_id: str):
        with SessionLocal() as db:
            messages = db.query(Message_table).filter(Message_table.sender_id == user_id).all()

        return [Message(
            id = m.id,
            sender_id = m.sender_id,
            receiver_id = m.receiver_id,
            title = m.title,
            content = m.content
        ) for m in messages]

    def find(self, email_id: str):
        with SessionLocal() as db:
            message = db.query(Message_table).filter(Message_table.id == email_id).first()
        
        if not message:
            raise HTTPException(status_code = 422)

        return Message(
            id = message.id,
            sender_id = message.sender_id,
            receiver_id = message.receiver_id,
            title = message.title,
            content = message.content
        )
