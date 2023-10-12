from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.schemas.user_schema import NewUser, UserResp
from src.core.database import get_db
from src.services.user_service import UserService

users_router = APIRouter()


@users_router.post("/", response_model=UserResp, status_code=status.HTTP_201_CREATED)
def create_user(body: NewUser, db: Session = Depends(get_db)):
    return UserService.create_user(body, db)
