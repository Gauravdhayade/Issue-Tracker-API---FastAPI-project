from sqlalchemy.orm import Session
from fastapi import HTTPException
import asyncio

from app.models.issue import Issue, StatusEnum
from app.models.activity_log import ActivityLog
from app.models.project import Project

from app.repositories.issue_repository import (
    create_issue,
    get_issues_by_project,
    get_issue,
    search_issues
)

from app.repositories.membership_repository import get_membership
from app.repositories.activity_repository import create_activity
from app.services.notification_service import send_notification


# Create Issue
def create_issue_service(db: Session, project_id: int, data, current_user_id: int):

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not organization member")

    issue = Issue(
        title=data.title,
        description=data.description,
        priority=data.priority,
        project_id=project_id,
        reporter_id=current_user_id,
        assignee_id=data.assignee_id
    )

    issue = create_issue(db, issue)

    # Async notification
    if issue.assignee_id:
        try:
            asyncio.create_task(
                send_notification(
                    issue.assignee_id,
                    f"You have been assigned issue: {issue.title}"
                )
            )
        except RuntimeError:
            pass

    return issue


# List Issues (with pagination)
def list_issues_service(db: Session, project_id: int, current_user_id: int, page: int = 1, limit: int = 10):

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not organization member")

    offset = (page - 1) * limit

    return db.query(Issue)\
        .filter(Issue.project_id == project_id)\
        .offset(offset)\
        .limit(limit)\
        .all()


# Update Issue Status
def update_status_service(db: Session, issue_id: int, status: StatusEnum, current_user_id: int):

    issue = get_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    project = db.query(Project).filter(Project.id == issue.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise HTTPException(status_code=403, detail="Not organization member")

    old_status = issue.status

    issue.status = status
    db.commit()
    db.refresh(issue)

    # Activity Log
    activity = ActivityLog(
        issue_id=issue.id,
        changed_by=current_user_id,
        field_name="status",
        old_value=old_status.value,
        new_value=status.value
    )

    create_activity(db, activity)

    # Notification
    if issue.assignee_id:
        try:
            asyncio.create_task(
                send_notification(
                    issue.assignee_id,
                    f"Issue status changed to {status.value}"
                )
            )
        except RuntimeError:
            pass

    return issue


# Search Issues
def search_issues_service(db: Session, filters: dict, current_user_id: int):

    return search_issues(db, **filters)