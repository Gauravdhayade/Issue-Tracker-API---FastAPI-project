from sqlalchemy.orm import Session
from app.models.membership import Membership

def create_membership(db: Session, membership: Membership):
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

def get_membership(db: Session, user_id: int, org_id: int):
    return db.query(Membership).filter(
        Membership.user_id == user_id,
        Membership.organization_id == org_id
    ).first()