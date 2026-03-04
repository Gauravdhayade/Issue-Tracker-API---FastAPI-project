from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.activity_log import ActivityLog
from app.models.issue import Issue
from app.repositories.membership_repository import get_membership

def get_issue_timeline(db: Session, issue_id: int, current_user_id: int):

    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise Exception("Issue not found")

    from app.models.project import Project
    project = db.query(Project).filter(Project.id == issue.project_id).first()

    membership = get_membership(db, current_user_id, project.organization_id)
    if not membership:
        raise Exception("Not organization member")

    comments = db.query(Comment).filter(Comment.issue_id == issue_id).all()
    activities = db.query(ActivityLog).filter(ActivityLog.issue_id == issue_id).all()

    timeline = []

    for c in comments:
        timeline.append({
            "type": "comment",
            "content": c.content,
            "user_id": c.user_id,
            "timestamp": c.created_at
        })

    for a in activities:
        timeline.append({
            "type": "activity",
            "field": a.field_name,
            "old_value": a.old_value,
            "new_value": a.new_value,
            "user_id": a.changed_by,
            "timestamp": a.changed_at
        })

    # Sort by timestamp
    timeline.sort(key=lambda x: x["timestamp"])

    return timeline