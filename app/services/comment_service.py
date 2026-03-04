from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.user import User
from app.repositories.comment_repository import (
    create_comment,
    get_comments_by_issue,
    get_comment
)
from app.repositories.membership_repository import get_membership
from app.services.notification_service import send_notification

import re


def add_comment_service(
    db: Session,
    issue_id: int,
    content: str,
    current_user_id: int,
    background_tasks
):

    # Get issue
    from app.models.issue import Issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise Exception("Issue not found")

    # Get project
    from app.models.project import Project
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    # Check membership
    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise Exception("Not organization member")

    # Create comment
    comment = Comment(
        issue_id=issue_id,
        user_id=current_user_id,
        content=content
    )

    comment = create_comment(db, comment)

    # Notify issue assignee
    if issue.assignee_id and issue.assignee_id != current_user_id:
        background_tasks.add_task(
            send_notification,
            issue.assignee_id,
            f"New comment added on issue: {issue.title}"
        )

    # 🔔 Detect @mentions
    mentions = re.findall(r'@(\w+)', content)

    for username in mentions:

        user = db.query(User).filter(User.name == username).first()

        if user and user.id != current_user_id:

            background_tasks.add_task(
                send_notification,
                user.id,
                f"You were mentioned in comment on issue: {issue.title}"
            )

    return comment


def list_comments_service(db: Session, issue_id: int, current_user_id: int):

    from app.models.issue import Issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise Exception("Issue not found")

    from app.models.project import Project
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise Exception("Not organization member")

    return get_comments_by_issue(db, issue_id)


def edit_comment_service(db: Session, comment_id: int, content: str, current_user_id: int):

    comment = get_comment(db, comment_id)

    if not comment:
        raise Exception("Comment not found")

    if comment.user_id != current_user_id:
        raise Exception("Cannot edit others comment")

    comment.content = content

    db.commit()
    db.refresh(comment)

    return comment