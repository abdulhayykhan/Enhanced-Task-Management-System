from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TaskBase(BaseModel):
    """Base schema for Task with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: str = Field(default="Pending", description="Task status")
    due_date: Optional[date] = Field(None, description="Task due date")

class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class TaskUpdate(TaskBase):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    status: Optional[str] = Field(None, description="Task status")

class TaskOut(TaskBase):
    """Schema for task output with ID"""
    id: int

    class Config:
        from_attributes = True
        # For older Pydantic versions, use: orm_mode = True
