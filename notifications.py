from typing import Dict, List
from fastapi import WebSocket
import json
import asyncio
from sqlalchemy.orm import Session
import models

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        """Connect a user to WebSocket"""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        """Disconnect a user from WebSocket"""
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: str, user_id: int):
        """Send a message to a specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
            except Exception:
                # Connection might be closed, remove it
                self.disconnect(user_id)

    async def broadcast_to_users(self, message: str, user_ids: List[int]):
        """Send a message to multiple users"""
        for user_id in user_ids:
            await self.send_personal_message(message, user_id)

# Global connection manager instance
manager = ConnectionManager()

def create_notification(db: Session, user_id: int, message: str) -> models.Notification:
    """Create a notification in the database"""
    notification = models.Notification(
        user_id=user_id,
        message=message,
        read=False
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

async def notify_user(db: Session, user_id: int, message: str):
    """Create notification and send via WebSocket"""
    # Save to database
    notification = create_notification(db, user_id, message)
    
    # Send via WebSocket if user is connected
    notification_data = {
        "id": notification.id,
        "message": message,
        "created_at": notification.created_at.isoformat(),
        "read": notification.read
    }
    await manager.send_personal_message(json.dumps(notification_data), user_id)

def get_unread_notifications(db: Session, user_id: int) -> List[models.Notification]:
    """Get all unread notifications for a user"""
    return db.query(models.Notification).filter(
        models.Notification.user_id == user_id,
        models.Notification.read == False
    ).order_by(models.Notification.created_at.desc()).all()

def mark_notification_read(db: Session, notification_id: int, user_id: int):
    """Mark a notification as read"""
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user_id
    ).first()
    if notification:
        notification.read = True
        db.commit()
        return notification
    return None