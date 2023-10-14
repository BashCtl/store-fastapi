from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from . import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(15), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"
