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
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
    """Update an existing task in the database"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        # Only update fields that were provided (exclude_unset=True)
        update_data = task.model_dump(exclude_unset=True)
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
def get_analytics_overview(db: Session, user_id: int = None):
    """Get overview analytics for tasks - user-specific if user_id provided"""
    base_query = db.query(func.count(models.Task.id))
    
    # Filter by user if user_id provided
    if user_id:
        base_query = base_query.filter(models.Task.owner_id == user_id)
    
    total = base_query.scalar() or 0
    
    # Get status counts
    status_query = db.query(func.count(models.Task.id))
    if user_id:
        status_query = status_query.filter(models.Task.owner_id == user_id)
    
    completed = status_query.filter(models.Task.status == "Completed").scalar() or 0
    pending = status_query.filter(models.Task.status == "Pending").scalar() or 0
    in_progress = status_query.filter(models.Task.status == "In Progress").scalar() or 0
    
    # Calculate completion rate
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Get overdue tasks (past due date and not completed)
    today = datetime.now().date()
    overdue_query = db.query(func.count(models.Task.id)).filter(
        models.Task.due_date < today,
        models.Task.status != "Completed"
    )
    if user_id:
        overdue_query = overdue_query.filter(models.Task.owner_id == user_id)
    
    overdue = overdue_query.scalar() or 0
    
    # Get upcoming tasks (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_query = db.query(func.count(models.Task.id)).filter(
        models.Task.due_date >= today,
        models.Task.due_date <= next_week,
        models.Task.status != "Completed"
    )
    if user_id:
        upcoming_query = upcoming_query.filter(models.Task.owner_id == user_id)
    
    upcoming = upcoming_query.scalar() or 0
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress,
        "overdue": overdue,
        "upcoming": upcoming,
        "completion_rate": round(completion_rate, 1)
    }

def get_weekly_trends(db: Session, user_id: int = None):
    """Get weekly task completion trends - user-specific if user_id provided"""
    # Get tasks from last 8 weeks
    eight_weeks_ago = datetime.now().date() - timedelta(weeks=8)
    
    # Use PostgreSQL date functions for week grouping
    query = db.query(
        extract('week', models.Task.due_date).label('week'),
        extract('year', models.Task.due_date).label('year'),
        models.Task.status,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.due_date >= eight_weeks_ago
    )
    
    # Filter by user if user_id provided
    if user_id:
        query = query.filter(models.Task.owner_id == user_id)
    
    trends = query.group_by(
        extract('week', models.Task.due_date),
        extract('year', models.Task.due_date),
        models.Task.status
    ).order_by('year', 'week').all()
    
    return trends

def get_monthly_stats(db: Session, user_id: int = None):
    """Get monthly task statistics - user-specific if user_id provided"""
    # Get tasks from last 6 months
    six_months_ago = datetime.now().date() - timedelta(days=180)
    
    query = db.query(
        extract('month', models.Task.due_date).label('month'),
        extract('year', models.Task.due_date).label('year'),
        models.Task.status,
        func.count(models.Task.id).label('count')
    ).filter(
        models.Task.due_date >= six_months_ago
    )
    
    # Filter by user if user_id provided
    if user_id:
        query = query.filter(models.Task.owner_id == user_id)
    
    monthly_stats = query.group_by(
        extract('month', models.Task.due_date),
        extract('year', models.Task.due_date),
        models.Task.status
    ).order_by('year', 'month').all()
    
    return monthly_stats

def get_user_productivity(db: Session, user_id: int = None):
    """Get user productivity statistics - user-specific if user_id provided"""
    from sqlalchemy import case
    
    query = db.query(
        models.User.name,
        func.count(models.Task.id).label('total_tasks'),
        func.sum(case((models.Task.status == 'Completed', 1), else_=0)).label('completed_tasks'),
        func.sum(case((models.Task.status == 'In Progress', 1), else_=0)).label('in_progress_tasks'),
        func.sum(case((models.Task.status == 'Pending', 1), else_=0)).label('pending_tasks')
    ).join(
        models.Task, models.User.id == models.Task.owner_id
    )
    
    # Filter by user if user_id provided
    if user_id:
        query = query.filter(models.User.id == user_id)
    
    user_stats = query.group_by(
        models.User.name
    ).all()
    
    return user_stats
