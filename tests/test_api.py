from fastapi.testclient import TestClient
from tick_manager.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Tick Manager API"}

