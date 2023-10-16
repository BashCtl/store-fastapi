from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models.user_model import User
from src.schemas.pet_schema import NewPet, PetRes
from src.services.auth_service import AuthService
from src.services.pet_service import PetService

pets_router = APIRouter()


@pets_router.post("/", status_code=status.HTTP_201_CREATED)
def add_pet(body: NewPet, db: Session = Depends(get_db),
            current_user: User = Depends(AuthService.get_current_user)):
    return PetService.add_pet(body, db)


@pets_router.get("/{id}", response_model=PetRes)
def get_pet(id: int, db: Session = Depends(get_db),
            current_user: User = Depends(AuthService.get_current_user)):
    return PetService.get_pet_by_id(id, db)


@pets_router.put("/{id}", response_model=PetRes)
def update_pet(id: int, body: NewPet, current_user: User = Depends(AuthService.get_current_user),
               db: Session = Depends(get_db)):
    return PetService.update_pet_by_id(id, body, db)
