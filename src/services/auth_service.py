from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.core.configs import settings
from src.schemas.token_schema import TokenData
from src.core.database import get_db
from src.models.user_model import User


class AuthService:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")

    @classmethod
    def create_access_token(cls, data: dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_access_token(cls, token: str, credential_exception):
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=[AuthService.ALGORITHM])
            id: int = payload.get("id")
            if id is None:
                raise credential_exception
            token_data = TokenData(id=id)
        except JWTError:
            raise credential_exception
        return token_data

    @classmethod
    def get_current_user(cls, token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials.",
                                             headers={"WWW-Authenticate": "Bearer"})
        token = AuthService.verify_access_token(token, credential_exception)
        user = db.query(User).filter(User.id == token.id).first()
        return user
