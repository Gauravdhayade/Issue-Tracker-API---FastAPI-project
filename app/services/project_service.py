from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.membership import RoleEnum
from app.repositories.project_repository import create_project, get_projects_by_org
from app.repositories.membership_repository import get_membership

def create_project_service(db: Session, org_id: int, data, current_user_id: int):
    membership = get_membership(db, current_user_id, org_id)

    if not membership:
        raise Exception("Not organization member")

    if membership.role not in [RoleEnum.Owner, RoleEnum.Admin, RoleEnum.Developer]:
        raise Exception("Permission denied")

    project = Project(
        name=data.name,
        project_key=data.project_key,
        description=data.description,
        visibility=data.visibility,
        organization_id=org_id,
        created_by=current_user_id
    )

    return create_project(db, project)

def list_projects(db: Session, org_id: int, current_user_id: int):
    membership = get_membership(db, current_user_id, org_id)

    if not membership:
        raise Exception("Not organization member")

    return get_projects_by_org(db, org_id)