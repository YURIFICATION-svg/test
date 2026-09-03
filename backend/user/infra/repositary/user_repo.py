from fastapi import HTTPException

#내부 모듈
from database import SessionLocal
from user.domain.repositary.user_repo import IUserRepositary
from user.domain.user import User as UserV0
from user.infra.db_models.user import User

class UserRepositary(IUserRepositary): #구현체
    def save(self, user: UserV0):
        new_user = User(
            id = user.id,
            name = user.name,
            password = user.password
        )
        try:
            db = SessionLocal()
            db.add(new_user)
            db.commit()
        finally:
            db.close()

    def find_by_name(self, name: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.name == name).first()
        
        if not user:
            raise HTTPException(status_code = 422)

        return UserV0(
            id = user.id,
            name = user.name,
            password = user.password
        )
    
    def find_by_id(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()
        
        if not user:
            raise HTTPException(status_code = 422)

        return UserV0(
            id = user.id,
            name = user.name,
            password = user.password
        )

    def update(self, user_vo: UserV0):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code = 422)

            user.name = user_vo.name
            user.password = user_vo.password

            db.add(user)
            db.commit()
        
        return user

    def delete(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code = 422)
                
            db.delete(user)
            db.commit()
        
