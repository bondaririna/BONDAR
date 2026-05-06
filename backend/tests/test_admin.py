from fastapi.testclient import TestClient


def test_admin_create_organizer(client: TestClient, admin_token: str) -> None:
    r = client.post(
        "/api/v1/admin/organizers",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "email": "new.organizer@example.com",
            "password": "StrongPass123",
            "full_name": "New Organizer",
            "role": "organizer",
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "new.organizer@example.com"
    assert body["role"] == "organizer"


def test_admin_create_organizer_rejects_invalid_role(client: TestClient, admin_token: str) -> None:
    r = client.post(
        "/api/v1/admin/organizers",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "email": "wrong-role@example.com",
            "password": "StrongPass123",
            "full_name": "Wrong Role",
            "role": "student",
        },
    )
    assert r.status_code == 400


def test_non_admin_cannot_create_organizer(client: TestClient, organizer_token: str) -> None:
    r = client.post(
        "/api/v1/admin/organizers",
        headers={"Authorization": f"Bearer {organizer_token}"},
        json={
            "email": "blocked@example.com",
            "password": "StrongPass123",
            "full_name": "Blocked",
            "role": "organizer",
        },
    )
    assert r.status_code == 403
