from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.schemas.user_schema import NewUser, UserResp, UpdateUser
from src.core.database import get_db
from src.services.user_service import UserService
from src.models.user_model import User
from src.services.auth_service import AuthService

users_router = APIRouter()


@users_router.post("/", response_model=UserResp, status_code=status.HTTP_201_CREATED)
def create_user(body: NewUser, db: Session = Depends(get_db)):
    return UserService.create_user(body, db)


@users_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserService.login(request, db)


@users_router.get("/logout")
def user_logout(current_user: User = Depends(AuthService.get_current_user),
                token: str = Depends(AuthService.oauth2_schema), db: Session = Depends(get_db)):
    return UserService.user_logout(current_user, token, db)


@users_router.get("/{id}", response_model=UserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(id, db)


@users_router.put("/{id}", response_model=UserResp)
def update_user(id: int, body: UpdateUser,
                current_user: User = Depends(AuthService.get_current_user),
                db: Session = Depends(get_db)):
    return UserService.update_user_by_id(id, body, current_user, db)


@users_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int,
                current_user: User = Depends(AuthService.get_current_user),
                db: Session = Depends(get_db)):
    return UserService.delete_user_by_id(id, current_user, db)
