from fastapi.testclient import TestClient

from tick_manager.api.example_main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tick Manager API"}


def test_add():
    response = client.post("/add", json={"a": 1, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 3}


def test_subtract():
    response = client.post("/subtract", json={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_multiply():
    response = client.post("/multiply", json={"a": 4, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_divide():
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_divide_by_zero():
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "division by zero"}
