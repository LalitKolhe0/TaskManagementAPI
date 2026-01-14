"""
Test Suite for Task Management API
===================================
Run with: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app



# FIXTURES


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def sample_task():
    """Sample task data for testing"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }


# HEALTH & ROOT TESTS


class TestHealthEndpoints:
    """Tests for health and root endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_health_check(self, client):
        """Test health check returns healthy status"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data



# GET TASKS TESTS


class TestGetTasks:
    """Tests for retrieving tasks"""

    def test_get_all_tasks(self, client):
        """Test getting all tasks"""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "count" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_tasks_filter_by_status(self, client):
        """Test filtering tasks by status"""
        response = client.get("/api/tasks?status=pending")
        assert response.status_code == 200
        data = response.json()
        for task in data["data"]:
            assert task["status"] == "pending"

    def test_get_tasks_filter_by_priority(self, client):
        """Test filtering tasks by priority"""
        response = client.get("/api/tasks?priority=high")
        assert response.status_code == 200
        data = response.json()
        for task in data["data"]:
            assert task["priority"] == "high"

    def test_get_tasks_search(self, client):
        """Test searching tasks"""
        response = client.get("/api/tasks?search=API")
        assert response.status_code == 200
        data = response.json()
        for task in data["data"]:
            assert "api" in task["title"].lower() or \
                   (task["description"] and "api" in task["description"].lower())

    def test_get_tasks_pagination(self, client):
        """Test pagination"""
        response = client.get("/api/tasks?limit=1&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) <= 1

    def test_get_single_task(self, client):
        """Test getting a specific task"""
        response = client.get("/api/tasks/task-001")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == "task-001"

    def test_get_task_not_found(self, client):
        """Test 404 for non-existent task"""
        response = client.get("/api/tasks/non-existent-id")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()



# CREATE TASK TESTS


class TestCreateTask:
    """Tests for creating tasks"""

    def test_create_task_full_data(self, client, sample_task):
        """Test creating task with all fields"""
        response = client.post("/api/tasks", json=sample_task)
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == sample_task["title"]
        assert data["data"]["id"].startswith("task-")
        assert "created_at" in data["data"]
        assert "updated_at" in data["data"]

    def test_create_task_minimal(self, client):
        """Test creating task with only required field"""
        response = client.post("/api/tasks", json={"title": "Minimal Task"})
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["status"] == "pending"  # Default
        assert data["data"]["priority"] == "medium"  # Default

    def test_create_task_empty_title(self, client):
        """Test validation error for empty title"""
        response = client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422

    def test_create_task_missing_title(self, client):
        """Test validation error for missing title"""
        response = client.post("/api/tasks", json={"description": "No title"})
        assert response.status_code == 422

    def test_create_task_invalid_status(self, client):
        """Test validation error for invalid status"""
        response = client.post("/api/tasks", json={
            "title": "Test",
            "status": "invalid-status"
        })
        assert response.status_code == 422

    def test_create_task_invalid_priority(self, client):
        """Test validation error for invalid priority"""
        response = client.post("/api/tasks", json={
            "title": "Test",
            "priority": "super-urgent"
        })
        assert response.status_code == 422



# UPDATE TASK TESTS


class TestUpdateTask:
    """Tests for updating tasks"""

    def test_update_task_status(self, client):
        """Test updating task status"""
        response = client.put(
            "/api/tasks/task-001",
            json={"status": "in-progress"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["status"] == "in-progress"

    def test_update_task_multiple_fields(self, client):
        """Test updating multiple fields"""
        response = client.put(
            "/api/tasks/task-002",
            json={
                "title": "Updated Title",
                "priority": "urgent"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["title"] == "Updated Title"
        assert data["data"]["priority"] == "urgent"

    def test_update_task_not_found(self, client):
        """Test 404 when updating non-existent task"""
        response = client.put(
            "/api/tasks/fake-id",
            json={"status": "completed"}
        )
        assert response.status_code == 404



# DELETE TASK TESTS

class TestDeleteTask:
    """Tests for deleting tasks"""

    def test_delete_task(self, client, sample_task):
        """Test deleting a task"""
        # First create a task to delete
        create_response = client.post("/api/tasks", json=sample_task)
        task_id = create_response.json()["data"]["id"]
        
        # Delete the task
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "deleted" in data["message"].lower()
        
        # Verify task is gone
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client):
        """Test 404 when deleting non-existent task"""
        response = client.delete("/api/tasks/fake-id")
        assert response.status_code == 404



# STATISTICS TESTS

class TestStatistics:
    """Tests for statistics endpoint"""

    def test_get_statistics(self, client):
        """Test statistics endpoint"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_tasks" in data
        assert "by_status" in data
        assert "by_priority" in data
        assert isinstance(data["total_tasks"], int)


