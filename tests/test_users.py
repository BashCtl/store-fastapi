from src.schemas import user_schema
from src.schemas.token_schema import Token
from jose import jwt
from src.core.configs import settings


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
