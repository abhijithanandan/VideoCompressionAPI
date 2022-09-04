from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    result = client.get("/")
    assert result.json().get('message') == 'Hello World'
    assert result.status_code == 200


