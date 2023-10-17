from src.schemas.order_schema import OrderOut
from src.models.order_model import Order


def test_place_valid_order(authorized_client, order_data):
    response = authorized_client.post("/store/orders", json=order_data)
    order_res = OrderOut(**response.json())
    assert response.status_code == 201
    assert order_res.user_id == order_data["user_id"]


def test_get_order_by_valid_id(authorized_client, placed_order):
    response = authorized_client.get(f"/store/orders/{placed_order.id}")
    order_res = OrderOut(**response.json())
    assert response.status_code == 200
    assert order_res.id == placed_order.id


def test_delete_placed_order(authorized_client, placed_order, session):
    response = authorized_client.delete(f"/store/orders/{placed_order.id}")
    assert response.status_code == 204
    assert session.query(Order).count() == 0
