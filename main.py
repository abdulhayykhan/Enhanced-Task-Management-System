from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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

# Frontend HTML Routes
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    """Main page showing all tasks"""
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/tasks/new", response_class=HTMLResponse)
def new_task(request: Request):
    """Show form to create a new task"""
    return templates.TemplateResponse("form.html", {"request": request, "task": None})

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
    crud.create_task(db=db, task=task_data)
    return RedirectResponse("/", status_code=303)

@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def task_detail(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Show task detail page"""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("detail.html", {"request": request, "task": task})

@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def edit_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    """Show form to edit an existing task"""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("form.html", {"request": request, "task": task})

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
def read_tasks_api(db: Session = Depends(get_db)):
    """Get all tasks via API"""
    return crud.get_tasks(db)

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