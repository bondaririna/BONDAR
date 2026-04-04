import pytest
from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_google_auth_creates_student(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_verify(_token: str) -> dict:
        return {
            "sub": "google-sub-xyz",
            "email": "ion@student.usv.ro",
            "email_verified": True,
            "name": "Ion Popescu",
        }

    monkeypatch.setattr("app.routers.auth.verify_google_id_token", fake_verify)
    r = client.post("/api/v1/auth/google", json={"id_token": "fake.jwt.token"})
    assert r.status_code == 200
    data = r.json()
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_google_auth_rejects_non_student_domain(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_verify(_token: str) -> dict:
        return {
            "sub": "sub",
            "email": "user@gmail.com",
            "email_verified": True,
        }

    monkeypatch.setattr("app.routers.auth.verify_google_id_token", fake_verify)
    r = client.post("/api/v1/auth/google", json={"id_token": "x" * 20})
    assert r.status_code == 400


def test_password_login_organizer(client: TestClient, organizer_user) -> None:
    r = client.post(
        "/api/v1/auth/login",
        json={"username": "org@test.local", "password": "orgpass123"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_me_requires_token(client: TestClient) -> None:
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_me_with_token(client: TestClient, student_token: str, student_user) -> None:
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {student_token}"})
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == "student@student.usv.ro"
    assert body["role"] == "student"
