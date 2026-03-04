from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

def register_user(db: Session, name: str, email: str, password: str):
    existing = get_user_by_email(db, email)
    if existing:
        raise Exception("Email already registered")

    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    return create_user(db, new_user)


def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise Exception("Invalid credentials")

    # 🔐 Create access token
    access_token = create_access_token({"sub": user.email})

    # 🔁 Create refresh token
    refresh_token = create_refresh_token({"sub": user.email})

    # 💾 Store refresh token in DB
    user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }