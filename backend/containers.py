from dependency_injector import containers, providers

#내부 모듈
from user.infra.repositary.user_repo import UserRepositary
from user.application.user_service import UserService
from message.infra.repositary.message_repo import MRepositary
from message.application.message_service import MService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user", "message"]
    )

    user_repo = providers.Factory(UserRepositary)
    user_service = providers.Factory(UserService, user_repo=user_repo)
    message_repo = providers.Factory(MRepositary)
    message_service = providers.Factory(MService, message_repo=message_repo)
