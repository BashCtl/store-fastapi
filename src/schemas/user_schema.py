from pydantic import BaseModel, EmailStr, Field


class NewUser(BaseModel):
    username: str = Field(..., min_length=2, max_length=30, description="username")
    first_name: str = Field(..., min_length=1, max_length=30, description="user firstname")
    last_name: str = Field(..., min_length=1, max_length=30, description="user lastname")
    email: EmailStr = Field(..., description="user email")
    phone: str = Field(..., description="user phone number")
    password: str = Field(..., min_length=5, max_length=25, description="user password")


class UserResp(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
