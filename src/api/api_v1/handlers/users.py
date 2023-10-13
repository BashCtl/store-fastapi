from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.schemas.user_schema import NewUser, UserResp
from src.core.database import get_db
from src.services.user_service import UserService

users_router = APIRouter()


@users_router.post("/", response_model=UserResp, status_code=status.HTTP_201_CREATED)
def create_user(body: NewUser, db: Session = Depends(get_db)):
    return UserService.create_user(body, db)


@users_router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserService.login(request, db)


@users_router.get("/{id}", response_model=UserResp)
def get_user(id: int, db: Session = Depends(get_db)):
    return UserService.get_user_by_id(id, db)
