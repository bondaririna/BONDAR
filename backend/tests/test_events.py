from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def test_list_events_empty(client: TestClient) -> None:
    r = client.get("/api/v1/events")
    assert r.status_code == 200
    assert r.json() == []


def test_create_event_as_organizer_pending(
    client: TestClient, organizer_token: str, organizer_user
) -> None:
    start = datetime.utcnow() + timedelta(days=1)
    end = start + timedelta(hours=2)
    r = client.post(
        "/api/v1/events",
        headers={"Authorization": f"Bearer {organizer_token}"},
        json={
            "title": "Workshop AI",
            "description": "Desc",
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "location": "C209",
            "faculty_or_department": "FMI",
            "category": "academic",
            "participation_mode": "physical",
            "organizer_name": "FMI",
        },
    )
    assert r.status_code == 201
    ev = r.json()
    assert ev["status"] == "pending"
    assert ev["organizer_user_id"] == organizer_user.id


def test_public_list_hides_pending(
    client: TestClient, organizer_token: str
) -> None:
    start = datetime.utcnow() + timedelta(days=2)
    end = start + timedelta(hours=1)
    client.post(
        "/api/v1/events",
        headers={"Authorization": f"Bearer {organizer_token}"},
        json={
            "title": "Hidden",
            "description": "",
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "location": "X",
            "faculty_or_department": "",
            "category": "sport",
            "participation_mode": "online",
            "organizer_name": "Club",
        },
    )
    r = client.get("/api/v1/events")
    assert r.status_code == 200
    assert r.json() == []


def test_admin_publish_makes_visible(
    client: TestClient, organizer_token: str, admin_token: str
) -> None:
    start = datetime.utcnow() + timedelta(days=3)
    end = start + timedelta(hours=1)
    cr = client.post(
        "/api/v1/events",
        headers={"Authorization": f"Bearer {organizer_token}"},
        json={
            "title": "Public talk",
            "description": "D",
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "location": "Aula",
            "faculty_or_department": "Automatica",
            "category": "career",
            "participation_mode": "hybrid",
            "organizer_name": "ASMI",
        },
    )
    eid = cr.json()["id"]
    r = client.patch(
        f"/api/v1/admin/events/{eid}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "published"},
    )
    assert r.status_code == 200
    lst = client.get("/api/v1/events")
    assert len(lst.json()) == 1


def test_feedback_after_event(
    client: TestClient, organizer_token: str, admin_token: str, student_token: str
) -> None:
    start = datetime.utcnow() - timedelta(days=2)
    end = datetime.utcnow() - timedelta(days=1)
    cr = client.post(
        "/api/v1/events",
        headers={"Authorization": f"Bearer {organizer_token}"},
        json={
            "title": "Past",
            "description": "",
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "location": "L",
            "faculty_or_department": "",
            "category": "cultural",
            "participation_mode": "physical",
            "organizer_name": "X",
        },
    )
    eid = cr.json()["id"]
    client.patch(
        f"/api/v1/admin/events/{eid}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "published"},
    )
    r = client.post(
        f"/api/v1/events/{eid}/feedback",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"rating": 5, "comment": "Excelent"},
    )
    assert r.status_code == 201
    assert r.json()["rating"] == 5
