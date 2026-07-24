from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "Page Pulse" in response.text
    assert "Built for Digital Heroes Training Task" in response.text
    assert "https://digitalheroesco.com" in (response.text)
