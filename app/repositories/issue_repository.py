from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.issue import Issue


def create_issue(db: Session, issue: Issue):
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_issues_by_project(db: Session, project_id: int):
    return db.query(Issue).filter(Issue.project_id == project_id).all()


def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()


def search_issues(
    db: Session,
    project_id=None,
    status=None,
    priority=None,
    assignee_id=None,
    keyword=None,
    sort=None,
    page=1,
    limit=10
):
    query = db.query(Issue)

    if project_id:
        query = query.filter(Issue.project_id == project_id)

    if status:
        query = query.filter(Issue.status == status)

    if priority:
        query = query.filter(Issue.priority == priority)

    if assignee_id:
        query = query.filter(Issue.assignee_id == assignee_id)

    if keyword:
        query = query.filter(
            or_(
                Issue.title.ilike(f"%{keyword}%"),
                Issue.description.ilike(f"%{keyword}%")
            )
        )

    if sort == "latest":
        query = query.order_by(Issue.created_at.desc())
    elif sort == "oldest":
        query = query.order_by(Issue.created_at.asc())

    total = query.count()

    results = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": results
    }