from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.organization_schema import OrganizationCreate, AddMember
from app.services.organization_service import create_org, add_member, my_organizations
from app.schemas.organization_schema import OrganizationCreate, OrganizationResponse

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.post("/", response_model=OrganizationResponse)
def create_organization_route(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_org(db, org.name, current_user.id)

@router.get("/my")
def get_my_orgs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return my_organizations(db, current_user.id)

@router.post("/{org_id}/members")
def add_member_route(
    org_id: int,
    member: AddMember,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return add_member(db, org_id, member.user_id, member.role, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))