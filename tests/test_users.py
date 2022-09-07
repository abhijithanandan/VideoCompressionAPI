from app import schemas
from .database import client, session


def test_root(client):
    result = client.get("/")
    assert result.json().get('message') == 'Hello World'
    assert result.status_code == 200


def test_create_user(client):
    result = client.post("/users/", json={
            "username": "abhijith",
            "first_name": "abhijith",
            "last_name": "ananadan",
            "password": "password123",
            "user_type": "administrator",
            "organization": "VCApi Org",
            "email": "abhi@vcapi.com"
    })

    new_user = schemas.UserResponse(**result.json())
    assert new_user.email == "abhi@vcapi.com"
    assert result.status_code == 201
