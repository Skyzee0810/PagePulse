from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.exceptions import (
    AuditConnectionError,
    AuditTimeoutError,
)
from app.main import app

client = TestClient(app)


def test_audit_timeout():
    with patch(
        "app.api.routes.audit_service.audit_url",
        new_callable=AsyncMock,
        side_effect=AuditTimeoutError(
            "The target URL timed out"
        ),
    ):
        response = client.post(
            "/audit",
            json={
                "url": "https://example.com"
            },
        )

    assert response.status_code == 504

    data = response.json()

    assert data["error"]["code"] == (
        "AUDIT_TIMEOUT"
    )

    assert "request_id" in data["error"]


def test_connection_error():
    with patch(
        "app.api.routes.audit_service.audit_url",
        new_callable=AsyncMock,
        side_effect=AuditConnectionError(
            "Unable to connect to the target URL"
        ),
    ):
        response = client.post(
            "/audit",
            json={
                "url": "https://example.com"
            },
        )

    assert response.status_code == 502

    data = response.json()

    assert data["error"]["code"] == (
        "AUDIT_CONNECTION_ERROR"
    )