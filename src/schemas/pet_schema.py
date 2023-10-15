from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class NewPet(BaseModel):
    category: str = Field(..., max_length=20, description="pet category")
    name: str = Field(..., max_length=50, description="pet name")
    status: str = Field(...,  max_length=20, description="pet status")
