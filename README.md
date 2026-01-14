# 📋 Task Management API

A production-ready RESTful API built with **FastAPI** for managing tasks. This project demonstrates best practices in API development, testing, and documentation.

---

## 🔗 GitHub Profile

**Profile**: [github.com/lalitkolhe0](https://github.com/lalitkolhe0)

### About This Project

This API project showcases:
- ✅ RESTful API design principles
- ✅ Input validation with Pydantic models
- ✅ Auto-generated OpenAPI documentation
- ✅ Error handling and HTTP status codes
- ✅ Filtering, pagination, and search
- ✅ Unit testing with pytest
- ✅ Postman collection for API testing

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/lalitkolhe0/TaskManagementAPI.git
cd TaskManagementAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Access the API
- **API Base URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/tasks` | Get all tasks (with filters) |
| `GET` | `/api/tasks/{id}` | Get specific task |
| `POST` | `/api/tasks` | Create new task |
| `PUT` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `GET` | `/api/stats` | Task statistics |

### Query Parameters for GET /api/tasks

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by: pending, in-progress, completed, cancelled |
| `priority` | string | Filter by: low, medium, high, urgent |
| `search` | string | Search in title and description |
| `limit` | integer | Max results (1-100, default: 100) |
| `offset` | integer | Pagination offset (default: 0) |

---

## 📝 Request/Response Examples

### Create a Task

**Request:**
```http
POST /api/tasks
Content-Type: application/json

{
    "title": "Complete API Documentation",
    "description": "Write comprehensive docs with examples",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-02-01T10:00:00"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Task created successfully",
    "data": {
        "id": "task-a1b2c3d4",
        "title": "Complete API Documentation",
        "description": "Write comprehensive docs with examples",
        "status": "pending",
        "priority": "high",
        "due_date": "2025-02-01T10:00:00",
        "created_at": "2025-01-13T10:30:00",
        "updated_at": "2025-01-13T10:30:00"
    }
}
```

### Get Tasks with Filters

**Request:**
```http
GET /api/tasks?status=pending&priority=high&limit=10
```

**Response (200 OK):**
```json
{
    "success": true,
    "count": 2,
    "data": [
        {
            "id": "task-001",
            "title": "Complete API Documentation",
            "status": "pending",
            "priority": "high",
            ...
        }
    ]
}
```

### Error Response (404)

```json
{
    "detail": "Task with ID 'invalid-id' not found"
}
```

---

## 🧪 Testing with Postman

### Import the Collection

1. Open Postman
2. Click **Import** button
3. Select the file: `postman/Task_API_Collection.json`
4. The collection includes all endpoints with examples

### Test Scenarios

The Postman collection includes tests for:

1. **Health Check** - Verify API is running
2. **CRUD Operations** - Create, Read, Update, Delete tasks
3. **Validation Tests** - Test required fields and constraints
4. **Filter Tests** - Test query parameters
5. **Error Handling** - Test 404 and 400 responses

---

## 🏗️ Project Structure

```
task-api-fastapi/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── 
│   └── test_api.py      # Unit tests
├── 
│   └── Task_API_Collection.json
├── 
│   └── API_TESTING_GUIDE.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔒 Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `400` | Bad Request (validation error) |
| `404` | Not Found |
| `422` | Unprocessable Entity |
| `500` | Internal Server Error |

---

## 🛠️ Development

### Run Tests
```bash
pytest tests/ -v
```

### Run with Auto-reload
```bash
uvicorn app.main:app --reload
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
