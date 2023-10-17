from fastapi import HTTPException, status, Response

from sqlalchemy.orm import Session
from src.schemas.order_schema import OrderIn, OrderItem
from src.models.user_model import User
from src.models.order_model import Order, OrderItem
from src.models.pet_model import PetTable


class OrderService:

    @classmethod
    def place_order(cls, body: OrderIn, current_user: User, db: Session):
        order = Order(user_id=current_user.id, status=body.status, complete=body.complete)
        db.add(order)
        db.commit()
        db.refresh(order)
        for item in body.items:
            pet = db.query(PetTable).filter(PetTable.id == item.pet_id).first()
            if pet and pet.status == "available":
                order_item = OrderItem(order_id=order.id, pet_id=item.pet_id)
                pet.status = "sold"
                db.add(order_item)
                db.commit()
            else:
                db.delete(order)
                db.commit()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Item with '{item.pet_id}' id not available")
        return order

    @classmethod
    def get_order_by_id(cls, id: int, current_user: User, db: Session):
        order = db.query(Order).filter(Order.id == id).first()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
        elif order.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Forbidden.")
        return order

    @classmethod
    def delete_order_by_id(cls, id: int, current_user: User, db: Session):
        order_query = db.query(Order).filter(Order.id == id)
        if order_query.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")
        if order_query.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Forbidden.")
        order_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
