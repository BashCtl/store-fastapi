from fastapi import HTTPException, status, Response

from sqlalchemy.orm import Session
from src.models.pet_model import PetTable
from src.schemas.pet_schema import NewPet

from src.services.auth_service import AuthService


class PetService:

    @classmethod
    def add_pet(cls, body: NewPet, db: Session):
        pet = PetTable(**body.model_dump())
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet

    @classmethod
    def get_pet_by_id(cls, id: int, db: Session):
        pet = db.query(PetTable).filter(PetTable.id == id).first()
        if pet is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Pet not found.")
        return pet
