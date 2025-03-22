import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.create_all()
    yield app.test_client()
    db.drop_all()

def test_add_task(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 200
    assert b"Task added successfully!" in response.data

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Sample Task"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert b"Sample Task" in response.data

def test_delete_task(client):
    client.post("/tasks", json={"title": "Task to Delete"})
    response = client.get("/tasks")
    task_id = response.json[0]["id"]
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert b"Task deleted!" in delete_response.data
