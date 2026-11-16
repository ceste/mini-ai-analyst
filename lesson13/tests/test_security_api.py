import pytest
from fastapi.testclient import TestClient

from lesson12.security_api import app


@pytest.fixture
def client(monkeypatch):
    # Isolated test credentials.
    # No dependency on lesson12/.env.
    monkeypatch.setenv(
        "AI_ANALYST_KEY",
        "test-analyst-key",
    )
    monkeypatch.setenv(
        "AI_ADMIN_KEY",
        "test-admin-key",
    )

    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_analyst_can_access_secure(client):
    response = client.get(
        "/secure",
        headers={
            "X-API-Key": "test-analyst-key"
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "analyst"


def test_admin_can_access_secure(client):
    response = client.get(
        "/secure",
        headers={
            "X-API-Key": "test-admin-key"
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_analyst_cannot_access_admin(client):
    response = client.get(
        "/admin",
        headers={
            "X-API-Key": "test-analyst-key"
        },
    )

    assert response.status_code == 403


def test_admin_can_access_admin(client):
    response = client.get(
        "/admin",
        headers={
            "X-API-Key": "test-admin-key"
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_invalid_api_key(client):
    response = client.get(
        "/secure",
        headers={
            "X-API-Key": "wrong-key"
        },
    )

    assert response.status_code == 401


def test_missing_api_key(client):
    response = client.get("/secure")

    assert response.status_code == 401


def test_missing_auth_configuration(
    client,
    monkeypatch,
):
    monkeypatch.delenv("AI_ANALYST_KEY")
    monkeypatch.delenv("AI_ADMIN_KEY")

    response = client.get(
        "/secure",
        headers={
            "X-API-Key": "test-analyst-key"
        },
    )

    assert response.status_code == 503


def test_duplicate_api_keys_rejected(
    client,
    monkeypatch,
):
    monkeypatch.setenv(
        "AI_ADMIN_KEY",
        "test-analyst-key",
    )

    response = client.get(
        "/secure",
        headers={
            "X-API-Key": "test-analyst-key"
        },
    )

    assert response.status_code == 503
