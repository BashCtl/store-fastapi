import pytest
from src.schemas import pet_schema
from src.models.pet_model import PetTable


def test_add_pet(authorized_client, pet):
    response = authorized_client.post("/pets", json=pet)
    new_pet = pet_schema.PetRes(**response.json())
    assert response.status_code == 201
    assert new_pet.name == pet["name"]


def test_get_pet_by_id(authorized_client, db_pet):
    response = authorized_client.get(f"/pets/{db_pet.id}")
    pet = pet_schema.PetRes(**response.json())
    assert response.status_code == 200
    assert pet.name == db_pet.name


def test_get_all_pets(authorized_client, pet_list):
    response = authorized_client.get("/pets/list")
    pets = list(map(lambda pet: pet_schema.PetRes(**pet), response.json()))
    assert response.status_code == 200
    assert len(pets) == len(pet_list)


def test_update_pet(authorized_client, db_pet, pet):
    pet["name"] = "BlackDog"
    response = authorized_client.put(f"/pets/{db_pet.id}", json=pet)
    pet_res = pet_schema.PetRes(**response.json())
    assert response.status_code == 200
    assert pet_res.name == "BlackDog"


def test_delete_pet(authorized_client, db_pet, session):
    response = authorized_client.delete(f"/pets/{db_pet.id}")
    assert response.status_code == 204
    assert session.query(PetTable).count() == 0


def test_add_pet_unauthorized_client(client, pet):
    response = client.post("/pets", json=pet)
    assert response.status_code == 401


def test_get_unauthorized_client_pet_by_id(client, db_pet):
    response = client.get(f"/pets/{db_pet.id}")
    assert response.status_code == 401


def test_unauthorized_client_get_all_pets(client, pet_list):
    response = client.get("/pets/list")
    assert response.status_code == 401


def test_unauthorized_client_update_pet(client, db_pet, pet):
    pet["name"] = "BlackDog"
    response = client.put(f"/pets/{db_pet.id}", json=pet)
    assert response.status_code == 401


def test_unauthorized_client_delete_pet(client, db_pet):
    response = client.delete(f"/pets/{db_pet.id}")
    assert response.status_code == 401


def test_invalid_add_pet(authorized_client):
    response = authorized_client.post("/pets", json={})
    assert response.status_code == 422


@pytest.mark.parametrize("id, status_code", [
    (00, 404),
    (-1, 404),
    ("id", 422)
])
def test_get_pet_by_invalid_id(authorized_client, id, status_code):
    response = authorized_client.get(f"/pets/{id}")
    assert response.status_code == status_code
