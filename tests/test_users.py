from src.schemas import user_schema
from src.schemas.token_schema import Token
from jose import jwt
from src.core.configs import settings
from typing import List


def test_valid_registration(client, user):
    response = client.post("/users", json=user)
    new_user = user_schema.UserResp(**response.json())
    assert response.status_code == 201
    assert new_user.email == user['email']


def test_valid_login(client, registered_user):
    response = client.post("/users/login", data={"username": registered_user["email"],
                                                 "password": registered_user["password"]})
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    id = payload.get("id")
    assert id == registered_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


def test_get_single_user(client, registered_user):
    response = client.get(f"/users/{1}")
    user_res = user_schema.UserResp(**response.json())
    assert response.status_code == 200
    assert user_res.email == registered_user["email"]


def test_get_all_users(client, list_users):
    response = client.get("/users/list")
    users = list(map(lambda user: user_schema.UserResp(**user), response.json()))
    assert response.status_code == 200
    assert len(users) == len(list_users)


def test_update_user(authorized_client, registered_user):
    registered_user["phone"] = "111-555-7"
    response = authorized_client.put(f"/users/{registered_user['id']}", json=registered_user)
    assert response.status_code == 200


def test_delete_user(authorized_client, registered_user):
    response = authorized_client.delete(f"/users/{registered_user['id']}")
    assert response.status_code == 204


def test_logout_user(authorized_client, registered_user):
    response = authorized_client.get("/users/logout")
    assert response.status_code == 200
    response = authorized_client.delete(f"/users/{registered_user['id']}")
    assert response.status_code == 401
