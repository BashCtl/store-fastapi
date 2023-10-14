from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.configs import settings
from src.core.database import get_db
from src.models.token_model import TokenTable
from src.models.user_model import User
from src.schemas.token_schema import TokenData


class AuthService:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = eval(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    JWT_REFRESH_SECRET = settings.JWT_REFRESH_SECRET

    oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")

    @classmethod
    def create_access_token(cls, data: dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.SECRET_KEY, algorithm=AuthService.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict, expire_delta: int = None):
        to_encode = data.copy()
        if expire_delta:
            expire_delta = datetime.utcnow() + timedelta(minutes=expire_delta)
        else:
            expire_delta = datetime.utcnow() + timedelta(minutes=AuthService.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire_delta})
        encoded_jwt = jwt.encode(to_encode, AuthService.JWT_REFRESH_SECRET, algorithm=AuthService.ALGORITHM)
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
        token_data = AuthService.verify_access_token(token, credential_exception)
        user = db.query(User).filter(User.id == token_data.id).first()

        token_db = db.query(TokenTable).filter(TokenTable.access_token == token).first()
        if token_db.status:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token blocked.")
