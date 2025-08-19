from fastapi import FastAPI, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas, crud
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import auth

# Create FastAPI app instance
app = FastAPI(title="Task Management System", version="1.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Add CORS middleware for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication Routes
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Show registration form"""
    return templates.TemplateResponse("auth.html", {
        "request": request, 
        "action": "register"
    })

@app.post("/register")
def register_user(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Create a new user account"""
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "action": "register",
            "error": "Username already exists",
            "username": username
        })
    
    # Create new user
    user = models.User(username=username, password=auth.hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Show login form"""
    return templates.TemplateResponse("auth.html", {
        "request": request,
        "action": "login"
    })

@app.post("/login")
def login_user(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Authenticate user and create session"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, str(user.password)):
        return templates.TemplateResponse("auth.html", {
            "request": request,
            "action": "login",
            "error": "Invalid username or password",
            "username": username
        })
    
    token = auth.create_access_token({"sub": user.username})
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@app.get("/logout")
def logout_user():
    """Logout user by clearing session"""
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(key="access_token")
    return response

# Frontend HTML Routes with Search and Filtering
@app.get("/", response_class=HTMLResponse)
def read_root(
    request: Request, 
    q: str = Query(None, description="Search query"),
    status: str = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Main page showing all tasks with search and filter functionality"""
    current_user = auth.get_current_user(request, db)
    
    # Build query
    query = db.query(models.Task)
    
    # Filter by user if authenticated (optional for now)
    if current_user:
        # Show all tasks for now, but could filter by user_id
        pass
    
    # Apply search filter
    if q:
        query = query.filter(
            or_(
                models.Task.title.contains(q),
                models.Task.description.contains(q)
            )
        )
    
    # Apply status filter
    if status:
        query = query.filter(models.Task.status == status)
    
    tasks = query.all()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "tasks": tasks,
        "q": q,
        "status": status,
        "current_user": current_user
    })

@app.get("/tasks/new", response_class=HTMLResponse)
def new_task(request: Request, db: Session = Depends(get_db)):
    """Show form to create a new task"""
    current_user = auth.get_current_user(request, db)
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "task": None,
        "current_user": current_user
    })

@app.post("/tasks/new")
def create_task_form(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    status: str = Form("Pending"),
    due_date: str = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new task from form submission"""
    current_user = auth.get_current_user(request, db)
    
    # Convert due_date string to date object if provided
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            parsed_due_date = None
    
    # Create task using schema
    task_data = schemas.TaskCreate(
        title=title,
        description=description if description else None,
        status=status,
        due_date=parsed_due_date
    )
    
    # Create task with user association if logged in
    task = crud.create_task(db=db, task=task_data)
    if current_user:
        task.user_id = current_user.id
        db.commit()
    
    return RedirectResponse("/", status_code=303)

@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def task_detail(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Show task detail page"""
    current_user = auth.get_current_user(request, db)
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("detail.html", {
        "request": request, 
        "task": task,
        "current_user": current_user
    })

@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def edit_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Show form to edit an existing task"""
    current_user = auth.get_current_user(request, db)
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("form.html", {
        "request": request, 
        "task": task,
        "current_user": current_user
    })

@app.post("/tasks/{task_id}/edit")
def update_task_form(
    task_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    status: str = Form("Pending"),
    due_date: str = Form(None),
    db: Session = Depends(get_db)
):
    """Update an existing task from form submission"""
    # Convert due_date string to date object if provided
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            parsed_due_date = None
    
    # Update task using schema
    task_data = schemas.TaskUpdate(
        title=title,
        description=description if description else None,
        status=status,
        due_date=parsed_due_date
    )
    updated = crud.update_task(db, task_id, task_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse("/", status_code=303)

@app.get("/tasks/{task_id}/delete")
def delete_task_form(task_id: int, db: Session = Depends(get_db)):
    """Delete a task and redirect to home"""
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse("/", status_code=303)

# API Routes (for programmatic access)
@app.get("/api")
def api_home():
    """API endpoint to verify backend is running"""
    return {"message": "Task Management System Backend Running"}

@app.post("/api/tasks", response_model=schemas.TaskOut)
def create_task_api(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task via API"""
    return crud.create_task(db=db, task=task)

@app.get("/api/tasks", response_model=list[schemas.TaskOut])
def read_tasks_api(
    q: str = Query(None), 
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get all tasks via API with optional search and filter"""
    query = db.query(models.Task)
    
    if q:
        query = query.filter(
            or_(
                models.Task.title.contains(q),
                models.Task.description.contains(q)
            )
        )
    
    if status:
        query = query.filter(models.Task.status == status)
    
    return query.all()

@app.get("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task_api(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID via API"""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/api/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task_api(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task via API"""
    updated = crud.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@app.delete("/api/tasks/{task_id}")
def delete_task_api(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID via API"""
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)