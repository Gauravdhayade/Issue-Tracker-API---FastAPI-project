from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

def create_activity(db: Session, activity: ActivityLog):
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity