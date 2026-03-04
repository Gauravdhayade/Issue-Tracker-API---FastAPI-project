from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.project_schema import ProjectCreate
from app.services.project_service import create_project_service, list_projects

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/{org_id}")
def create_project(
    org_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return create_project_service(db, org_id, project, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/{org_id}")
def get_projects(
    org_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return list_projects(db, org_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))