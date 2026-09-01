from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from dataclasses import dataclass
import uuid
import os
import redis

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")
REDIS_URL = os.getenv("REDIS_URL")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def create_access_token(
    payload: dict,
    expires_delta: timedelta = timedelta(hours=6)
):
    expire = datetime.utcnow() + expires_delta
    payload.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    except JWTError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if redis_client.exists(f"blacklist:{jti}"):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)

    return user_id

def logout(token: str):
    payload = decode_access_token(token)
    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    exp_dt = datetime.utcfromtimestamp(exp) if isinstance(exp, (int, float)) else exp
    expires_seconds = int((exp_dt - datetime.utcnow()).total_seconds())
    if expires_seconds > 0:
        redis_client.setex(f"blacklist:{jti}", expires_seconds, "1")


