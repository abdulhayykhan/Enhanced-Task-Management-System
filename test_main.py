from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_home_page():
    """Test that the home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Management System" in response.text

def test_api_home():
    """Test the API endpoint"""
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Management System Backend Running"}

def test_create_task_api():
    """Test creating a task via API"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "Pending"
    }
    response = client.post("/api/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "Pending"
    assert "id" in data

def test_get_tasks_api():
    """Test getting all tasks via API"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_tasks_api():
    """Test searching tasks via API"""
    # First create a task
    task_data = {
        "title": "Searchable Task",
        "description": "This task should be found in search",
        "status": "Pending"
    }
    create_response = client.post("/api/tasks", json=task_data)
    assert create_response.status_code == 200
    
    # Now search for it
    search_response = client.get("/api/tasks?q=Searchable")
    assert search_response.status_code == 200
    tasks = search_response.json()
    assert len(tasks) > 0
    assert any("Searchable" in task["title"] for task in tasks)

def test_filter_tasks_by_status_api():
    """Test filtering tasks by status via API"""
    # Create a completed task
    task_data = {
        "title": "Completed Task",
        "description": "This task is completed",
        "status": "Completed"
    }
    create_response = client.post("/api/tasks", json=task_data)
    assert create_response.status_code == 200
    
    # Filter by completed status
    filter_response = client.get("/api/tasks?status=Completed")
    assert filter_response.status_code == 200
    tasks = filter_response.json()
    assert all(task["status"] == "Completed" for task in tasks)

def test_register_page():
    """Test that the register page loads"""
    response = client.get("/register")
    assert response.status_code == 200
    assert "Register" in response.text

def test_login_page():
    """Test that the login page loads"""
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text

def test_new_task_page():
    """Test that the new task form loads"""
    response = client.get("/tasks/new")
    assert response.status_code == 200
    assert "Create" in response.text or "Task" in response.text

if __name__ == "__main__":
    pytest.main([__file__])