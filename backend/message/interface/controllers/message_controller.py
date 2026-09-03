from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from dependency_injector.wiring import inject, Provide

from message.application.message_service import MService
from user.application.user_service import UserService
from containers import Container
from common.auth import get_current_user


router = APIRouter(prefix="/messages")


class MessageCreate(BaseModel):
    receiver_id: str
    title: str
    content: str


class MessageResponse(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    title: str
    content: str


def to_response(message) -> MessageResponse:
    return MessageResponse(
        id=message.id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        title=message.title,
        content=message.content,
    )


@router.post("", response_model=MessageResponse)
@inject
def send_message(
    message_body: MessageCreate,
    user_id: Annotated[str, Depends(get_current_user)],
    message_service: MService = Depends(Provide[Container.message_service]),
):
    message = message_service.send_message(
        sender_id=user_id,
        receiver_name=message_body.receiver_id,
        title=message_body.title,
        content=message_body.content,
    )
    return to_response(message)


@router.get("/received")
@inject
def read_received_message(
    user_id: Annotated[str, Depends(get_current_user)],
    message_service: MService = Depends(Provide[Container.message_service]),
):
    messages = message_service.read_received_message(user_id)
    return {"messages": [to_response(message) for message in messages]}


@router.get("/sent")
@inject
def read_sended_message(
    user_id: Annotated[str, Depends(get_current_user)],
    message_service: MService = Depends(Provide[Container.message_service]),
):
    messages = message_service.read_sended_message(user_id)
    return {"messages": [to_response(message) for message in messages]}


@router.get("/{message_id}", response_model=MessageResponse)
@inject
def find_by_id(
    message_id: str,
    user_id: Annotated[str, Depends(get_current_user)],
    message_service: MService = Depends(Provide[Container.message_service]),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    message = message_service.find_by_id(message_id)

    if message.sender_id != user_id and message.receiver_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="접근 권한이 없습니다.")

    return {
        **to_response(message),
        "receiver_name": user_service.find_by_id(message.receiver_id).name,
        "sender_name": user_service.find_by_id(message.sender_id).name
    }
        
