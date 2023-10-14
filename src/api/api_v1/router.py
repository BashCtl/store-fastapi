from fastapi import APIRouter
from src.api.api_v1.handlers.users import users_router


router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["user"])