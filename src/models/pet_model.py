from sqlalchemy import Column, Integer, String, Boolean, DateTime

from . import Base


class PetTable(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, nullable=False)
    category = Column(String(20), nullable=False)
    name = Column(String(50))
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return f"Pet(id={self.id}, category={self.category}, name={self.name}, status={self.status})"
