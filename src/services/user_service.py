from fastapi import HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.schemas.user_schema import NewUser, UpdateUser
from src.core.security import hashing_password, verify_password
from src.models.user_model import User
from src.services.auth_service import AuthService


class UserService:

    @classmethod
    def create_user(cls, body: NewUser, db: Session):
        body.password = hashing_password(body.password)
        new_user = User(**body.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @classmethod
    def get_user_by_id(cls, id: int, db: Session):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{id}' not found.")
        return user

    @classmethod
    def login(cls, request: OAuth2PasswordRequestForm, db: Session):
        user = db.query(User).filter(User.email == request.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
        access_token = AuthService.create_access_token({"id": user.id})
        return {"token_type": "bearer", "access_token": access_token}

    @classmethod
    def update_user_by_id(cls, id: int, body: UpdateUser, current_user: User, db: Session):
        user_to_update = db.query(User).filter(User.id == id)
        if not user_to_update.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        if id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation forbidden. You don't have permissions.")
        user_to_update.update(body.model_dump(), synchronize_session=False)
        db.commit()
        return user_to_update.first()

    @classmethod
    def delete_user_by_id(cls,id:int, current_user: User, db: Session):
        user_to_delete = db.query(User).filter(User.id==id)
        if not user_to_delete.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        if id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation forbidden. You don't have permissions.")
        user_to_delete.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)