from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_successful_audit():
    mock_result = {
        "url": "https://example.com",
        "status_code": 200,
        "response_time_ms": 120.5,
        "is_cached": False,
    }

    with patch(
        "app.api.routes.audit_service.audit_url",
        new_callable=AsyncMock,
        return_value=mock_result,
    ):
        response = client.post(
            "/audit",
            json={
                "url": "https://example.com"
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["url"] == "https://example.com"
    assert data["status_code"] == 200
    assert data["is_cached"] is False
    assert "request_id" in data

def test_invalid_url():
    response = client.post(
        "/audit",
        json={
            "url": "not-a-valid-url"
        },
    )

    assert response.status_code == 422

def test_missing_url():
    response = client.post(
        "/audit",
        json={}
    )

    assert response.status_code == 422