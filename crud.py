from sqlalchemy.orm import Session
from sqlalchemy import func, extract
import models, schemas
from datetime import datetime, timedelta
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

# Analytics Functions
def get_analytics_overview(db: Session):
    """Get overview analytics for tasks"""
    total = db.query(func.count(models.Task.id)).scalar() or 0
    completed = db.query(func.count(models.Task.id)).filter(models.Task.status == "Completed").scalar() or 0
    pending = db.query(func.count(models.Task.id)).filter(models.Task.status == "Pending").scalar() or 0
    in_progress = db.query(func.count(models.Task.id)).filter(models.Task.status == "In Progress").scalar() or 0
    
    # Calculate completion rate
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Get overdue tasks (past due date and not completed)
    today = datetime.now().date()
    overdue = db.query(func.count(models.Task.id)).filter(
        models.Task.due_date < today,
        models.Task.status != "Completed"
    ).scalar() or 0
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "overdue": overdue,
        "completion_rate": round(completion_rate, 1)
    }

def get_weekly_trends(db: Session):
    """Get weekly task completion trends"""
    # Get tasks from last 8 weeks
    eight_weeks_ago = datetime.now().date() - timedelta(weeks=8)
    
    # Use PostgreSQL date functions for week grouping
    trends = db.query(
        extract('week', models.Task.due_date).label('week'),
        extract('year', models.Task.due_date).label('year'),
        models.Task.status,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.due_date >= eight_weeks_ago
    ).group_by(
        extract('week', models.Task.due_date),
        extract('year', models.Task.due_date),
        models.Task.status
    ).order_by('year', 'week').all()
    
    return trends

def get_monthly_stats(db: Session):
    """Get monthly task statistics"""
    # Get tasks from last 6 months
    six_months_ago = datetime.now().date() - timedelta(days=180)
    
    monthly_stats = db.query(
        extract('month', models.Task.due_date).label('month'),
        extract('year', models.Task.due_date).label('year'),
        models.Task.status,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.due_date >= six_months_ago
    ).group_by(
        extract('month', models.Task.due_date),
        extract('year', models.Task.due_date),
        models.Task.status
    ).order_by('year', 'month').all()
    
    return monthly_stats

def get_user_productivity(db: Session):
    """Get user productivity statistics"""
    from sqlalchemy import case
    
    user_stats = db.query(
        models.User.username,
        func.count(models.Task.id).label('total_tasks'),
        func.sum(case((models.Task.status == 'Completed', 1), else_=0)).label('completed_tasks')
    ).join(
        models.Task, models.User.id == models.Task.owner_id
    ).group_by(
        models.User.username
    ).all()
    
    return user_stats
