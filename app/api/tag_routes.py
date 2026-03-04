from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tag import Tag
from app.repositories.tag_repository import create_tag, get_issue_tags

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/{issue_id}")
def add_tag(issue_id: int, name: str, db: Session = Depends(get_db)):

    tag = Tag(issue_id=issue_id, name=name)
    return create_tag(db, tag)

@router.get("/{issue_id}")
def list_tags(issue_id: int, db: Session = Depends(get_db)):
    return get_issue_tags(db, issue_id)