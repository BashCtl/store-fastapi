from src.schemas import user_schema


def test_valid_registration(client, user):
    response = client.post("/user", json=user)
    new_user = user_schema.UserResp(**response.json())
    assert response.status_code == 201
    assert new_user.email == user['email']
