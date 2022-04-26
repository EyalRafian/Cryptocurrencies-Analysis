import pytest
from main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_coins_table(client):
    response = client.get("/")
    assert response.status_code == 200

def test_create_coin(client):
    response = client.post(
        "/add",
        json={
            "ticker": "BTC-USD",
        },
    )
    assert response.status_code == 200
    assert response.json()
    print(response.json())

def test_delete_coin(client):
    response = client.post(
        "/delete",
        json={
            "ticker": "BTC-USD",
        },
    )
    assert response.status_code == 200
    assert response.json()
    print(response.json())

def test_update_table(client):
    response = client.post("/update")
    assert response.status_code == 422

