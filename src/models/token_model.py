from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from . import Base


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"TokenTable(user_id={self.user_id}, access_token={self.access_token},status={self.status})"
