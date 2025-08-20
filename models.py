from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many (task <-> shared users)
task_shares = Table(
    "task_shares", Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # store hashed password
    
    # Relationship to tasks
    owned_tasks = relationship("Task", back_populates="owner")
    shared_tasks = relationship("Task", secondary=task_shares, back_populates="shared_with")
    notifications = relationship("Notification", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

class Task(Base):
    """Task model for the database"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False, index=True)
    due_date = Column(Date, nullable=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    attachment = Column(String, nullable=True)  # store filename
    
    # Relationships
    owner = relationship("User", back_populates="owned_tasks")
    shared_with = relationship("User", secondary=task_shares, back_populates="shared_tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"

class Notification(Base):
    """Notification model for real-time updates"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    read = Column(Boolean, default=False, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, message='{self.message[:50]}...')>"
