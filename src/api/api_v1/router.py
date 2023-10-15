from fastapi import APIRouter
from src.api.api_v1.handlers.users import users_router
from src.api.api_v1.handlers.pets import pets_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(pets_router, prefix="/pets", tags=["pets"])
