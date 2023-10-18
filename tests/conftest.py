import json
import os
import pathlib

import pytest
from faker import Faker
from faker.providers import person
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import get_db
from src.models import Base
from src.models.order_model import Order
from src.models.pet_model import PetTable
from src.models.token_model import TokenTable
from src.models.user_model import User
from src.run import app
from src.schemas import order_schema
from src.services.auth_service import AuthService
from src.services.order_service import OrderService
from src.core.configs import settings

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASS}"
                           f"@{settings.DB_URI}:{settings.DB_PORT}/{settings.TEST_DB_NAME}")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fake = Faker()
fake.add_provider(person)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


def load_data(file):
    file = pathlib.Path(f"{os.getcwd()}/tests/testdata/{file}")
    with open(file) as f:
        data = json.load(f)

    return data


@pytest.fixture
def user():
    return load_data("user.json")


@pytest.fixture
def registered_user(client, user):
    user["username"] = "registered"
    user["email"] = "register@test.com"
    response = client.post("/users", json=user)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user["password"]

    return new_user


@pytest.fixture
def list_users(client, user):
    users = []
    user["username"] = "registered_1"
    user["email"] = "register_1@test.com"
    users.append(user)
    response = client.post("/users", json=user)
    assert response.status_code == 201
    user["username"] = "registered_2"
    user["email"] = "register_2@test.com"
    users.append(user)
    response = client.post("/users", json=user)
    assert response.status_code == 201
    return users


@pytest.fixture
def token(registered_user, session):
    token = AuthService.create_access_token({"id": registered_user["id"]})
    refresh_token = AuthService.create_refresh_token({"id": registered_user["id"]})
    token_db = TokenTable(user_id=registered_user["id"], access_token=token, refresh_token=refresh_token, status=True)
    session.add(token_db)
    session.commit()
    session.refresh(token_db)
    return token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# Pets fixtures

@pytest.fixture
def pet():
    return load_data("pet.json")


@pytest.fixture
def db_pet(session, pet):
    pet_to_add = PetTable(**pet)
    session.add(pet_to_add)
    session.commit()
    assert session.query(PetTable).count() == 1
    return pet_to_add


@pytest.fixture
def pet_list(session, db_pet):
    pet_to_add = PetTable(**load_data("pet2.json"))
    session.add(pet_to_add)
    session.commit()
    assert session.query(PetTable).count() == 2
    return session.query(PetTable).all()


@pytest.fixture
def order_data(pet_list, registered_user):
    order = load_data("order.json")
    return order


@pytest.fixture
def placed_order(session, order_data, registered_user):
    body = order_schema.OrderIn(**order_data)
    current_user = User(**registered_user)
    order = OrderService.place_order(body, current_user, session)
    assert session.query(Order).count() == 1
    return order
