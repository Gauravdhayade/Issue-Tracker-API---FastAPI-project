from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.attachment import Attachment

router = APIRouter(prefix="/attachments", tags=["Attachments"])

@router.post("/{issue_id}")
def add_attachment(issue_id: int, file_name: str, db: Session = Depends(get_db)):

    attachment = Attachment(issue_id=issue_id, file_name=file_name)

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment