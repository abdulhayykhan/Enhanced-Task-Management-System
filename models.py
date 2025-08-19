from sqlalchemy import Column, Integer, String, Date
from database import Base

class Task(Base):
    """Task model for the database"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)
    due_date = Column(Date, nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
