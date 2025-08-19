from sqlalchemy.orm import Session
import models, schemas
from typing import List, Optional

def get_tasks(db: Session) -> List[models.Task]:
    """Retrieve all tasks from the database"""
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Retrieve a specific task by ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Create a new task in the database"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
    """Update an existing task in the database"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        # Only update fields that were provided (exclude_unset=True)
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Delete a task from the database"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def get_tasks_by_status(db: Session, status: str) -> List[models.Task]:
    """Retrieve tasks filtered by status"""
    return db.query(models.Task).filter(models.Task.status == status).all()

def get_tasks_by_due_date(db: Session, due_date: str) -> List[models.Task]:
    """Retrieve tasks filtered by due date"""
    return db.query(models.Task).filter(models.Task.due_date == due_date).all()
