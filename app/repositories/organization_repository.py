from sqlalchemy.orm import Session
from app.models.organization import Organization

def create_organization(db: Session, org: Organization):
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def get_user_organizations(db: Session, user_id: int):
    from app.models.membership import Membership
    return db.query(Organization).join(Membership).filter(
        Membership.user_id == user_id
    ).all()