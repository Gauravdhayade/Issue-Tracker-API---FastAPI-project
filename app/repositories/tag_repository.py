from sqlalchemy.orm import Session
from app.models.tag import Tag

def create_tag(db: Session, tag: Tag):
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

def get_issue_tags(db: Session, issue_id: int):
    return db.query(Tag).filter(Tag.issue_id == issue_id).all()