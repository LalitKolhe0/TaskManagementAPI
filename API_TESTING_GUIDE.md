# 🧪 API Testing Guide with Postman

This guide demonstrates how to test the Task Management API using Postman, covering requests, responses, and validations.

---

## 📹 Video Demonstration Script

Use this script as a guide when recording your API testing video.

---

## Part 1: Introduction (1-2 minutes)

### What to Say:
> "Hi, I'm Lalit Kolhe, and today I'll demonstrate API testing using Postman with my Task Management API built in FastAPI. I'll cover making requests, understanding responses, and writing test validations."

### Show on Screen:
1. Open your GitHub repository
2. Show the README briefly
3. Open Postman with the imported collection

---

## Part 2: Setting Up (2-3 minutes)

### 2.1 Start the API Server

```bash
# Terminal command
cd task-api-project
uvicorn app.main:app --reload --port 8000
```

### What to Say:
> "First, let's start our FastAPI server. The `--reload` flag enables auto-reload during development."

### 2.2 Show the Swagger Documentation

- Navigate to: http://localhost:8000/docs
- Briefly show the auto-generated documentation

### What to Say:
> "FastAPI automatically generates interactive documentation. This Swagger UI shows all endpoints, request/response schemas, and lets you test directly."

---

## Part 3: Testing with Postman (10-12 minutes)

### 3.1 Health Check Endpoint

**Request:**
```
GET http://localhost:8000/api/health
```

**Expected Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-01-13T10:30:00.123456",
    "version": "1.0.0",
    "total_tasks": 3
}
```

**Tests to Explain:**
```javascript
// Test 1: Status Code
pm.test('Status code is 200', function() {
    pm.response.to.have.status(200);
});

// Test 2: Response Content
pm.test('API status is healthy', function() {
    const json = pm.response.json();
    pm.expect(json.status).to.eql('healthy');
});

// Test 3: Performance
pm.test('Response time < 500ms', function() {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### What to Say:
> "The health check endpoint verifies our API is running. Notice the tests: we check the status code is 200, the status field says 'healthy', and response time is acceptable."

---

### 3.2 GET All Tasks

**Request:**
```
GET http://localhost:8000/api/tasks
```

**Expected Response:**
```json
{
    "success": true,
    "count": 3,
    "data": [
        {
            "id": "task-001",
            "title": "Setup Development Environment",
            "description": "Install Python, FastAPI...",
            "status": "completed",
            "priority": "high",
            "created_at": "2025-01-10T09:00:00",
            "updated_at": "2025-01-14T15:30:00"
        }
        // ... more tasks
    ]
}
```

**Tests to Explain:**
```javascript
pm.test('Response has correct structure', function() {
    const json = pm.response.json();
    pm.expect(json.success).to.be.true;
    pm.expect(json).to.have.property('count');
    pm.expect(json.data).to.be.an('array');
});
```

### What to Say:
> "This returns all tasks. The response is wrapped with 'success', 'count', and 'data' fields. Our test validates this structure exists."

---

### 3.3 GET Tasks with Filters

**Request with Query Parameters:**
```
GET http://localhost:8000/api/tasks?status=pending&priority=high
```

**Tests to Explain:**
```javascript
pm.test('All tasks match filter criteria', function() {
    const json = pm.response.json();
    json.data.forEach(task => {
        pm.expect(task.status).to.eql('pending');
        pm.expect(task.priority).to.eql('high');
    });
});
```

### What to Say:
> "We can filter tasks using query parameters. Here we're filtering by 'pending' status and 'high' priority. The test iterates through results to verify each task matches our criteria."

---

### 3.4 POST - Create a New Task

**Request:**
```
POST http://localhost:8000/api/tasks
Content-Type: application/json

{
    "title": "Demo Task from Postman",
    "description": "Created during API testing demo",
    "status": "pending",
    "priority": "high",
    "due_date": "2025-02-01T18:00:00"
}
```

**Expected Response (201 Created):**
```json
{
    "success": true,
    "message": "Task created successfully",
    "data": {
        "id": "task-abc12345",
        "title": "Demo Task from Postman",
        "status": "pending",
        "priority": "high",
        "created_at": "2025-01-13T10:45:00",
        "updated_at": "2025-01-13T10:45:00"
    }
}
```

**Tests to Explain:**
```javascript
// Test status code
pm.test('Status code is 201 Created', function() {
    pm.response.to.have.status(201);
});

// Verify task creation
pm.test('Task has generated ID', function() {
    const json = pm.response.json();
    pm.expect(json.data.id).to.match(/^task-/);
});

// Save ID for later tests
const json = pm.response.json();
pm.collectionVariables.set('created_task_id', json.data.id);
```

### What to Say:
> "When creating a task, we send a POST request with JSON body. Notice the 201 status code indicating successful creation. The test verifies the ID format and saves it for subsequent requests."

---

### 3.5 Validation Error Testing

**Request (Missing Required Field):**
```
POST http://localhost:8000/api/tasks
Content-Type: application/json

{
    "description": "No title provided"
}
```

**Expected Response (422 Unprocessable Entity):**
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "title"],
            "msg": "Field required"
        }
    ]
}
```

**Tests to Explain:**
```javascript
pm.test('Status code is 422', function() {
    pm.response.to.have.status(422);
});

pm.test('Error mentions missing field', function() {
    const json = pm.response.json();
    const detail = JSON.stringify(json.detail);
    pm.expect(detail.toLowerCase()).to.include('title');
});
```

### What to Say:
> "Testing validation is crucial. When we omit the required 'title' field, the API returns 422 with detailed error information. Our test verifies both the status code and that the error mentions the missing field."

---

### 3.6 PUT - Update a Task

**Request:**
```
PUT http://localhost:8000/api/tasks/task-001
Content-Type: application/json

{
    "status": "completed",
    "priority": "low"
}
```

**Expected Response:**
```json
{
    "success": true,
    "message": "Task updated successfully",
    "data": {
        "id": "task-001",
        "status": "completed",
        "priority": "low",
        "updated_at": "2025-01-13T10:50:00"
    }
}
```

**Tests to Explain:**
```javascript
pm.test('Fields were updated', function() {
    const json = pm.response.json();
    pm.expect(json.data.status).to.eql('completed');
    pm.expect(json.data.priority).to.eql('low');
});

pm.test('Updated timestamp changed', function() {
    const json = pm.response.json();
    pm.expect(json.data.updated_at).to.not.eql(json.data.created_at);
});
```

### What to Say:
> "PUT requests update existing tasks. We're only sending fields we want to change - this is a partial update. Tests verify the changes were applied and the timestamp was updated."

---

### 3.7 DELETE a Task

**Request:**
```
DELETE http://localhost:8000/api/tasks/task-003
```

**Expected Response:**
```json
{
    "success": true,
    "message": "Task 'Write Unit Tests' deleted successfully",
    "deleted_id": "task-003"
}
```

**Tests to Explain:**
```javascript
pm.test('Status code is 200', function() {
    pm.response.to.have.status(200);
});

pm.test('Delete confirmed', function() {
    const json = pm.response.json();
    pm.expect(json.success).to.be.true;
    pm.expect(json.message).to.include('deleted');
});
```

### What to Say:
> "DELETE removes a task permanently. The response confirms which task was deleted. We verify success and the confirmation message."

---

### 3.8 Error Handling - 404 Not Found

**Request:**
```
GET http://localhost:8000/api/tasks/non-existent-id
```

**Expected Response (404):**
```json
{
    "detail": "Task with ID 'non-existent-id' not found"
}
```

**Tests to Explain:**
```javascript
pm.test('Status code is 404', function() {
    pm.response.to.have.status(404);
});

pm.test('Error message is descriptive', function() {
    const json = pm.response.json();
    pm.expect(json.detail).to.include('not found');
});
```

### What to Say:
> "Testing error scenarios is essential. When requesting a non-existent task, we get a 404 with a clear error message. Good APIs provide meaningful error responses."

---

## Part 4: Running the Collection (2-3 minutes)

### What to Say:
> "Postman lets us run all tests at once using the Collection Runner."

### Steps to Show:
1. Click **Run Collection** button
2. Select all requests
3. Click **Run Task Management API**
4. Show the results summary

### What to Explain:
- Green checkmarks = passed tests
- Red X = failed tests
- Total passed/failed count
- Individual test results

---

## Part 5: Conclusion (1-2 minutes)

### Key Points to Mention:

1. **Request Types Covered:**
   - GET (retrieve data)
   - POST (create data)
   - PUT (update data)
   - DELETE (remove data)

2. **Testing Best Practices:**
   - Always check status codes
   - Validate response structure
   - Test error scenarios
   - Use variables for dynamic data
   - Test edge cases

3. **Benefits of Postman:**
   - Easy request building
   - Test automation
   - Collection sharing
   - Environment variables
   - Documentation generation

### Closing Statement:
> "That concludes our API testing demonstration. The Postman collection and all source code is available in my GitHub repository. Thanks for watching!"

---

## 📋 Checklist for Recording

- [ ] API server running
- [ ] Postman collection imported
- [ ] Screen recording software ready
- [ ] Microphone tested
- [ ] Browser with Swagger UI open
- [ ] GitHub repository open
- [ ] Terminal visible for server logs

---

## 🎯 Key Validation Types Demonstrated

| Validation Type | Example |
|----------------|---------|
| Status Code | `pm.response.to.have.status(200)` |
| JSON Property | `pm.expect(json).to.have.property('data')` |
| Value Equality | `pm.expect(json.status).to.eql('healthy')` |
| Array Type | `pm.expect(json.data).to.be.an('array')` |
| String Contains | `pm.expect(message).to.include('success')` |
| Regex Match | `pm.expect(id).to.match(/^task-/)` |
| Boolean | `pm.expect(json.success).to.be.true` |
| Performance | `pm.expect(pm.response.responseTime).to.be.below(500)` |

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Postman Learning Center](https://learning.postman.com/)
- [REST API Best Practices](https://restfulapi.net/)
