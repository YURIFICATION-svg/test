from ulid import ULID
from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

#내부 모듈
from user.domain.user import User
from user.domain.repositary.user_repo import IUserRepositary
from utils.crypto import Crypto
from containers import Container
from common.auth import create_access_token, logout as logout_user

class UserService:
    def __init__(self, user_repo: IUserRepositary = Depends(Provide[Container.user_repo])):
        self.ulid = ULID()
        self.crypto = Crypto()
        self.user_repo = user_repo

    def create_user (self, name: str, password: str):
        _user = None
        try:
            _user = self.user_repo.find_by_name(name)
        except HTTPException as e:
            if e.status_code != 422:
                raise e
        if _user:
            raise HTTPException(status_code = 422)
            
        user: User = User(
            id = self.ulid.generate(),
            name = name,
            password = self.crypto.encrypt(password),
        )
        self.user_repo.save(user)

        return user

    def update_user(self, id: str, name: str | None = None, password: str | None = None):
        user = self.user_repo.find_by_id(id)
        if name:
            user.name = name
        if password:
            user.password = self.crypto.encrypt(password)

        self.user_repo.update(user)

        return user

    def get_users(self):
        return self.user_repo.get_users()

    def delete_user(self, id: str):
        self.user_repo.delete(id)

    def login(self, name: str, password: str):
        user = self.user_repo.find_by_name(name)
        if not self.crypto.verify(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token = create_access_token(payload = {"user_id": user.id})
        return access_token

    def logout(self, token: str):
        logout_user(token)
        