from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.issue_schema import IssueCreate, IssueStatusUpdate

from app.services.issue_service import (
    create_issue_service,
    list_issues_service,
    update_status_service,
    search_issues_service
)

from app.services.timeline_service import get_issue_timeline


router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/{project_id}")
async def create_issue(
    project_id: int,
    issue: IssueCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_issue_service(db, project_id, issue, current_user.id)

@router.get("/project/{project_id}")
async def list_issues(
    project_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return list_issues_service(
        db,
        project_id,
        current_user.id,
        page,
        limit
    )

@router.put("/{issue_id}/status")
async def update_status(
    issue_id: int,
    status_data: IssueStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return update_status_service(db, issue_id, status_data.status, current_user.id)

@router.get("/{issue_id}/timeline")
async def issue_timeline(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_issue_timeline(db, issue_id, current_user.id)

@router.get("/search")
async def search(
    project_id: int = None,
    status: str = None,
    priority: str = None,
    assignee_id: int = None,
    keyword: str = None,
    sort: str = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    filters = {
        "project_id": project_id,
        "status": status,
        "priority": priority,
        "assignee_id": assignee_id,
        "keyword": keyword,
        "sort": sort,
        "page": page,
        "limit": limit
    }

    return search_issues_service(db, filters, current_user.id)