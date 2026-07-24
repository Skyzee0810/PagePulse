from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Page Pulse is running"}

def test_request_id_is_returned(client):
    response = client.get("/")

    assert response.status_code == 200

    assert "X-Request-ID" in response.headers