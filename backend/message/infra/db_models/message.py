from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

# 내부 모듈
from database import Base

class Message(Base):
    __tablename__ = "Message"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    sender_id: Mapped[str] = mapped_column(String(64), nullable=False)
    receiver_id: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(36), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)