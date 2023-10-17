from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    status = Column(String(15), nullable=False, default="placed")
    complete = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    items = relationship("OrderItem")

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, status={self.status}, complete={self.complete})"


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("PetTable")

    def __repr__(self):
        return f"OrderItem(id={self.id}, order_id={self.order_id}, pet_id={self.pet_id})"
