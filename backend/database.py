from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://mika_user:PlGi9xYUxgFtmbzFp1CfYIoYCuexLKbW@dpg-da84q9rtqb8s73ds70hg-a.ohio-postgres.render.com/mika"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from user.infra.db_models.user import User
    from message.infra.db_models.message import Message
    Base.metadata.create_all(bind=engine)
