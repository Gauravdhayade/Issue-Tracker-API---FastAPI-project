from sqlalchemy.orm import Session
from app.models.project import Project

def create_project(db: Session, project: Project):
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects_by_org(db: Session, org_id: int):
    return db.query(Project).filter(Project.organization_id == org_id).all()