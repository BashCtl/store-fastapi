from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models.user_model import User
from src.schemas.user_schema import NewUser, UserResp, UpdateUser
from src.schemas.order_schema import OrderItem, OrderIn, OrderOut
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.order_service import OrderService

store_route = APIRouter()


@store_route.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(body: OrderIn, current_user: User = Depends(AuthService.get_current_user),
                db: Session = Depends(get_db)):
    return OrderService.place_order(body, current_user, db)


@store_route.get("/orders/{id}", response_model=OrderOut)
def get_order(id: int, current_user: User = Depends(AuthService.get_current_user),
              db: Session = Depends(get_db)):
    return OrderService.get_order_by_id(id, current_user, db)


@store_route.delete("/orders/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, current_user: User = Depends(AuthService.get_current_user),
                 db: Session = Depends(get_db)):
    return OrderService.delete_order_by_id(id, current_user, db)
