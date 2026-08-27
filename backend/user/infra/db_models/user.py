from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

# 내부 모듈
from database import Base

class User(Base):
    __tablename__ = "User"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)