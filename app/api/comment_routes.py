from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.services.comment_service import add_comment_service, list_comments_service, edit_comment_service
from fastapi import BackgroundTasks

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/{issue_id}")
def add_comment(
    issue_id: int,
    data: CommentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return add_comment_service(
            db,
            issue_id,
            data.content,
            current_user.id,
            background_tasks
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/{issue_id}")
def list_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return list_comments_service(db, issue_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.put("/{comment_id}")
def edit_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return edit_comment_service(db, comment_id, data.content, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))