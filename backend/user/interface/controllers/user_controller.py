from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm

# 내부 모듈
from user.application.user_service import UserService
from containers import Container
from common.auth import get_current_user, oauth2_scheme

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str
    password: str

class UpdateUser(BaseModel):
    name: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: str
    name: str

@router.post("", response_model=UserResponse) #Post /users 요청이 오면 create_user() 실행
@inject
def create_user(user: CreateUserBody, user_service: UserService = Depends(Provide[Container.user_service])):
    created_user = user_service.create_user(name=user.name, password=user.password)
    return created_user

@router.put("", response_model=UserResponse)
@inject
def update_user(user_id: Annotated[str, Depends(get_current_user)], user: UpdateUser, user_service: UserService = Depends(Provide[Container.user_service])):
    user = user_service.update_user(id = user_id, name = user.name, password = user.password)
    return user

@router.get("")
@inject
def get_user(user_service: UserService = Depends(Provide[Container.user_service])):
    users = user_service.get_user()
    return user

@router.delete("", status_code = 204)
@inject
def delete_user(user_id: Annotated[str, Depends(get_current_user)], user_service: UserService = Depends(Provide[Container.user_service])):
    user_service.delete_user(user_id)

@router.post("/login")
@inject
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserService = Depends(Provide[Container.user_service])):
    access_token = user_service.login(form_data.username, form_data.password)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
@inject
def logout(token: Annotated[str, Depends(oauth2_scheme)], user_service: UserService = Depends(Provide[Container.user_service])):
    user_service.logout(token)
