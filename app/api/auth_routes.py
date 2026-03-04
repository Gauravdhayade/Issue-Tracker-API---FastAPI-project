from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.core.database import get_db
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import RefreshTokenRequest
from app.services.auth_service import register_user, login_user
from app.core.security import create_access_token, REFRESH_SECRET_KEY, ALGORITHM
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["Auth"])


# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    try:
        created_user = register_user(db, user.name, user.email, user.password)

        return {
            "id": created_user.id,
            "name": created_user.name,
            "email": created_user.email
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    try:
        return login_user(db, form_data.username, form_data.password)

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# REFRESH TOKEN
@router.post("/refresh")
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):

    token = data.refresh_token

    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.email == email).first()

    if not user or user.refresh_token != token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }