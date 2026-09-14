from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest, LoginRequest, RegisterRequest,
    ResetPasswordRequest, TokenResponse, UserResponse, VerifyOtpRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    result = AuthService(db).register(payload)
    return {"access_token": result["access_token"], "token_type": "bearer", "user": result.get("user")}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    result = AuthService(db).login(payload)
    return {"access_token": result["access_token"], "token_type": "bearer", "user": result.get("user")}


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return AuthService(db).forgot_password(payload.email)


@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    return AuthService(db).verify_otp(payload.email, payload.otp)


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    return AuthService(db).reset_password(payload.token, payload.new_password)