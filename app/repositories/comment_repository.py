from sqlalchemy.orm import Session
from app.models.comment import Comment

def create_comment(db: Session, comment: Comment):
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments_by_issue(db: Session, issue_id: int):
    return db.query(Comment).filter(Comment.issue_id == issue_id).all()

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()