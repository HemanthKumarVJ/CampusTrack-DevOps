
from fastapi.testclient import TestClient
from app.main import app
import app.main as main

client = TestClient(app)


def setup_function():
    main.tasks.clear()
    main.next_id = 1


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    response = client.post(
        "/todos",
        json={"title": "Learn DevOps", "completed": False}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Learn DevOps"


def test_get_tasks():
    client.post("/todos", json={"title": "Test task"})

    response = client.get("/todos")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_nonexistent_task():
    response = client.get("/todos/999")

    assert response.status_code == 404
