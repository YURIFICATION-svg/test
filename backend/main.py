from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from database import SessionLocal, engine, Base

class User(Base):
  __tablename__ = "users"

  id            = Column(Integer, primary_key=True, index=True)
  username      = Column(String(50), unique=True, nullable=False, index=True)
  password_hash = Column(String(200), nullable=False)

class RegisterReq(BaseModel):
  username: str
  password: str

pwd_ctx  = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = 'mika0508'
ALGORITHM = "HS256"
TOKEN_EXPIRE_H = 24

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TeaPartyRoom", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_pw(pw: str)   -> str:  return pwd_ctx.hash(pw)
def verify_pw(pw, h)   -> bool: return pwd_ctx.verify(pw, h)

def create_token(user_id: int) -> str:
  exp = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_H)
  return jwt.encode({"sub": str(user_id), "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
  db = SessionLocal()
  try:    yield db
  finally: db.close()

@app.post("/auth/login", summary="로그인")
def login(req: RegisterReq, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == req.username).first()
  if not user or not verify_pw(user.password, user.password_hash):
    raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다")
  
  token = create_token(user.id)
  return {"token": token, "token_type": "bearer", "username": user.username}


@app.post("/auth/register", summary="회원가입")
def register(req: RegisterReq, db: Session = Depends(get_db)):
  if db.query(User).filter(User.username == req.username).first():
      raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다")
  user = User(username=req.username, password_hash=hash_pw(req.password))
  db.add(user)
  db.commit()
  db.refresh(user)
  token = create_token(user.id)
  return {"token": token, "username": user.username}
  
