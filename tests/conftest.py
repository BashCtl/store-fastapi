import json
import pathlib
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.core.database import get_db
from src.run import app

SQACHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(SQACHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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