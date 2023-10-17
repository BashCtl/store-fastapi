import pytest
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


def test_update_unauthorized_user(client, registered_user):
    registered_user["phone"] = "111-555-7"
    response = client.put(f"/users/{registered_user['id']}", json=registered_user)
    assert response.status_code == 401


def test_unauthorized_user_deletion(client, registered_user):
    response = client.delete(f"/users/{registered_user['id']}")
    assert response.status_code == 401


def test_unauthorized_user_logout(client):
    response = client.get("/users/logout")
    assert response.status_code == 401


def test_invalid_registration(client, user):
    user['email'] = ""
    response = client.post("/users", json=user)
    assert response.status_code == 422


@pytest.mark.parametrize("email, password, status_code", [
    ("", "qwerty1234", 422),
    ("black@test.com", "", 422),
    ("black", "qwerty1234", 401),
    ("black@test.com", "pass", 401)
])
def test_invalid_user_login(client, registered_user, email, password, status_code):
    response = client.post("/users/login", data={"username": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize("id, status_code", [
    (00, 404),
    (-1, 404),
    ("id", 422)
])
def test_get_single_user_by_invalid_id(client, id, status_code):
    response = client.get(f"/users/{id}")
    assert response.status_code == status_code


@pytest.mark.parametrize("id, status_code", [
    (00, 404),
    (-1, 404),
    ("id", 422)
])
def test_delete_user_by_invalid_id(authorized_client, id, status_code):
    response = authorized_client.delete(f"/users/{id}")
    assert response.status_code == status_code


@pytest.mark.parametrize("id, status_code", [
    (00, 404),
    (-1, 404),
    ("id", 422)
])
def test_update_user_by_invalid_id(authorized_client, id, status_code, registered_user):
    response = authorized_client.put(f"/users/{id}", json=registered_user)
    assert response.status_code == status_code
