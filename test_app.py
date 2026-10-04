import pytest

from app import app, tasks


@pytest.fixture
def client():
    # Keep tests isolated because the application uses an in-memory store.
    app.config["TESTING"] = True
    tasks.clear()

    with app.test_client() as client:
        yield client

    tasks.clear()


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Learn Flask"})

    assert response.status_code == 201
    data = response.get_json()

    assert data["title"] == "Learn Flask"
    assert data["completed"] is False
    assert "id" in data


def test_get_all_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    data = response.get_json()

    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task_by_id(client):
    create_response = client.post("/tasks", json={"title": "Find me"})
    task_id = create_response.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Find me"


def test_update_task(client):
    create_response = client.post("/tasks", json={"title": "Old title"})
    task_id = create_response.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["title"] == "New title"
    assert data["completed"] is True


def test_get_missing_task_returns_404(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "task not found"}
