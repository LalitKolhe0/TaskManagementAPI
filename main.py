"""
Task Management API
====================
A RESTful API built with FastAPI for managing tasks.

GitHub Repository: https://github.com/lalitkolhe0/task-api-fastapi
Author: Your Name
Version: 1.0.0

Features:
- Full CRUD operations for tasks
- Input validation with Pydantic
- Filtering and search capabilities
- Auto-generated API documentation (Swagger UI)
"""

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid

# ENUMS & MODELS


class TaskStatus(str, Enum):
    """Task status options"""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Priority level")
    due_date: Optional[datetime] = Field(None, description="Due date for the task")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete API Documentation",
                "description": "Write comprehensive docs with examples",
                "status": "pending",
                "priority": "high",
                "due_date": "2025-02-01T10:00:00"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed",
                "priority": "low"
            }
        }


class Task(BaseModel):
    """Complete task model with all fields"""
    id: str = Field(..., description="Unique task identifier")
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class TaskResponse(BaseModel):
    """Standard response wrapper for single task"""
    success: bool = True
    message: str
    data: Task


class TaskListResponse(BaseModel):
    """Standard response wrapper for task list"""
    success: bool = True
    count: int
    data: List[Task]


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    detail: str


# ============================================
# APPLICATION SETUP
# ============================================

app = FastAPI(
    title="Task Management API",
    description="""
## 📋 Task Management REST API

A fully-featured API for managing tasks with the following capabilities:

### Features
- **Create** new tasks with validation
- **Read** tasks with filtering options
- **Update** existing tasks (partial updates supported)
- **Delete** tasks

### Authentication
Currently using open access (add JWT/OAuth for production)

### Rate Limiting
No rate limiting in demo mode

---
**GitHub**: [github.com/yourusername/task-api-fastapi](https://github.com/yourusername/task-api-fastapi)
    """,
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
        "url": "https://github.com/yourusername"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# IN-MEMORY DATABASE (Demo purposes)
# ============================================

tasks_db: dict[str, Task] = {}

# Add sample data
sample_tasks = [
    {
        "id": "task-001",
        "title": "Setup Development Environment",
        "description": "Install Python, FastAPI, and configure IDE",
        "status": TaskStatus.COMPLETED,
        "priority": TaskPriority.HIGH,
        "due_date": datetime(2025, 1, 15, 10, 0, 0),
        "created_at": datetime(2025, 1, 10, 9, 0, 0),
        "updated_at": datetime(2025, 1, 14, 15, 30, 0)
    },
    {
        "id": "task-002",
        "title": "Create API Endpoints",
        "description": "Implement CRUD operations for task management",
        "status": TaskStatus.IN_PROGRESS,
        "priority": TaskPriority.HIGH,
        "due_date": datetime(2025, 1, 20, 18, 0, 0),
        "created_at": datetime(2025, 1, 12, 10, 0, 0),
        "updated_at": datetime(2025, 1, 13, 11, 0, 0)
    },
    {
        "id": "task-003",
        "title": "Write Unit Tests",
        "description": "Create comprehensive test suite using pytest",
        "status": TaskStatus.PENDING,
        "priority": TaskPriority.MEDIUM,
        "due_date": datetime(2025, 1, 25, 17, 0, 0),
        "created_at": datetime(2025, 1, 13, 8, 0, 0),
        "updated_at": datetime(2025, 1, 13, 8, 0, 0)
    }
]

for task_data in sample_tasks:
    tasks_db[task_data["id"]] = Task(**task_data)


# ============================================
# API ENDPOINTS
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Welcome to Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    
    Returns the API status and current timestamp.
    Useful for load balancers and monitoring systems.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "total_tasks": len(tasks_db)
    }


# ---------- TASK ENDPOINTS ----------

@app.get(
    "/api/tasks",
    response_model=TaskListResponse,
    tags=["Tasks"],
    summary="Get all tasks"
)
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    limit: int = Query(100, ge=1, le=100, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    Retrieve all tasks with optional filtering
    
    ### Query Parameters:
    - **status**: Filter tasks by status (pending, in-progress, completed, cancelled)
    - **priority**: Filter tasks by priority (low, medium, high, urgent)
    - **search**: Search keyword in title and description
    - **limit**: Maximum number of results (1-100)
    - **offset**: Pagination offset
    
    ### Response:
    Returns a list of tasks matching the criteria
    """
    filtered_tasks = list(tasks_db.values())
    
    # Apply filters
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.status == status]
    
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
    
    if search:
        search_lower = search.lower()
        filtered_tasks = [
            t for t in filtered_tasks 
            if search_lower in t.title.lower() or 
               (t.description and search_lower in t.description.lower())
        ]
    
    # Apply pagination
    paginated_tasks = filtered_tasks[offset:offset + limit]
    
    return TaskListResponse(
        success=True,
        count=len(paginated_tasks),
        data=paginated_tasks
    )


@app.get(
    "/api/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Get a specific task",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def get_task(task_id: str):
    """
    Retrieve a specific task by its ID
    
    ### Path Parameters:
    - **task_id**: Unique identifier of the task
    
    ### Response:
    Returns the task details if found, otherwise 404 error
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    return TaskResponse(
        success=True,
        message="Task retrieved successfully",
        data=tasks_db[task_id]
    )


@app.post(
    "/api/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def create_task(task: TaskCreate):
    """
    Create a new task
    
    ### Request Body:
    - **title** (required): Task title (1-200 characters)
    - **description** (optional): Task description (max 1000 characters)
    - **status** (optional): Initial status (default: pending)
    - **priority** (optional): Priority level (default: medium)
    - **due_date** (optional): Due date in ISO format
    
    ### Response:
    Returns the created task with generated ID and timestamps
    """
    now = datetime.now()
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    
    new_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        created_at=now,
        updated_at=now
    )
    
    tasks_db[task_id] = new_task
    
    return TaskResponse(
        success=True,
        message="Task created successfully",
        data=new_task
    )


@app.put(
    "/api/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Update an existing task",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def update_task(task_id: str, task_update: TaskUpdate):
    """
    Update an existing task (partial update supported)
    
    ### Path Parameters:
    - **task_id**: ID of the task to update
    
    ### Request Body:
    Only include fields you want to update:
    - **title**: New title
    - **description**: New description
    - **status**: New status
    - **priority**: New priority
    - **due_date**: New due date
    
    ### Response:
    Returns the updated task
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    existing_task = tasks_db[task_id]
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Update only provided fields
    updated_task = existing_task.model_copy(
        update={**update_data, "updated_at": datetime.now()}
    )
    
    tasks_db[task_id] = updated_task
    
    return TaskResponse(
        success=True,
        message="Task updated successfully",
        data=updated_task
    )


@app.delete(
    "/api/tasks/{task_id}",
    tags=["Tasks"],
    summary="Delete a task",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def delete_task(task_id: str):
    """
    Delete a task by ID
    
    ### Path Parameters:
    - **task_id**: ID of the task to delete
    
    ### Response:
    Returns confirmation message
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    deleted_task = tasks_db.pop(task_id)
    
    return {
        "success": True,
        "message": f"Task '{deleted_task.title}' deleted successfully",
        "deleted_id": task_id
    }


# ============================================
# STATISTICS ENDPOINT
# ============================================

@app.get("/api/stats", tags=["Statistics"])
async def get_statistics():
    """
    Get task statistics
    
    Returns counts grouped by status and priority
    """
    tasks = list(tasks_db.values())
    
    status_counts = {}
    for s in TaskStatus:
        status_counts[s.value] = len([t for t in tasks if t.status == s])
    
    priority_counts = {}
    for p in TaskPriority:
        priority_counts[p.value] = len([t for t in tasks if t.priority == p])
    
    return {
        "total_tasks": len(tasks),
        "by_status": status_counts,
        "by_priority": priority_counts
    }


# ============================================
# RUN APPLICATION
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
