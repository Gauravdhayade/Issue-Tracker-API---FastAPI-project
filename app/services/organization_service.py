from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.membership import Membership, RoleEnum
from app.repositories.organization_repository import create_organization, get_user_organizations
from app.repositories.membership_repository import create_membership, get_membership

def create_org(db: Session, name: str, user_id: int):
    org = Organization(name=name, created_by=user_id)
    org = create_organization(db, org)

    membership = Membership(
        user_id=user_id,
        organization_id=org.id,
        role=RoleEnum.Owner
    )
    create_membership(db, membership)

    return org

def add_member(db: Session, org_id: int, user_id: int, role: str, current_user_id: int):
    membership = get_membership(db, current_user_id, org_id)

    if not membership or membership.role not in [RoleEnum.Owner, RoleEnum.Admin]:
        raise Exception("Not authorized")

    new_member = Membership(
        user_id=user_id,
        organization_id=org_id,
        role=RoleEnum(role)
    )

    return create_membership(db, new_member)

def my_organizations(db: Session, user_id: int):
    return get_user_organizations(db, user_id)