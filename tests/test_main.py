from fastapi.testclient import TestClient
from webapp.main import app

client = TestClient(app)


def test_generate_default_length():
    response = client.post("/generate", json={})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert len(data["token"]) == 20


def test_generate_custom_length():
    response = client.post("/generate", json={"length": 10})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert len(data["token"]) == 10


def test_generate_invalid_length():
    response = client.post("/generate", json={"length": -5})
    assert response.status_code == 422  # FastAPI should return validation
    # error for negative length