
import pytest
from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_data():
    main.students.clear()
    main.attendance_records.clear()
    main.next_student_id = 1


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["documentation"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_student():
    response = client.post(
        "/students",
        json={
            "name": "Rahul Kumar",
            "roll_number": "CSE001",
            "section": "A"
        }
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_duplicate_roll_number():
    student = {
        "name": "Rahul Kumar",
        "roll_number": "CSE001",
        "section": "A"
    }

    client.post("/students", json=student)
    response = client.post("/students", json=student)

    assert response.status_code == 409


def test_mark_attendance():
    student = client.post(
        "/students",
        json={
            "name": "Rahul Kumar",
            "roll_number": "CSE001",
            "section": "A"
        }
    )

    response = client.post(
        "/attendance",
        json={
            "student_id": student.json()["id"],
            "attendance_date": "2026-11-18",
            "status": "present"
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "present"


def test_attendance_percentage():
    student = client.post(
        "/students",
        json={
            "name": "Rahul Kumar",
            "roll_number": "CSE001",
            "section": "A"
        }
    )

    student_id = student.json()["id"]

    client.post(
        "/attendance",
        json={
            "student_id": student_id,
            "attendance_date": "2026-11-17",
            "status": "present"
        }
    )

    client.post(
        "/attendance",
        json={
            "student_id": student_id,
            "attendance_date": "2026-11-18",
            "status": "absent"
        }
    )

    response = client.get(f"/students/{student_id}/percentage")

    assert response.status_code == 200
    assert response.json()["total_classes"] == 2
    assert response.json()["attendance_percentage"] == 50.0


def test_attendance_for_unknown_student():
    response = client.post(
        "/attendance",
        json={
            "student_id": 999,
            "attendance_date": "2026-11-18",
            "status": "present"
        }
    )

    assert response.status_code == 404
