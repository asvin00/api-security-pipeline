import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200

def test_health(client):
    res = client.get("/health")
    assert res.json["status"] == "OK"

def test_create_item(client):
    res = client.post("/items", json={"name": "Test Item"})
    assert res.status_code == 201
    assert res.json["name"] == "Test Item"

def test_get_items(client):
    client.post("/items", json={"name": "Item1"})
    res = client.get("/items")
    assert res.status_code == 200
    assert len(res.json) >= 1
