import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import settings
from app.models.otp import OtpCode
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.email_service import send_email
from app.utils.security import create_access_token, decode_token, hash_password, verify_password

OTP_EXPIRE_MINUTES = 10
OTP_MAX_ATTEMPTS = 5


def _hash_otp(code: str) -> str:
    return hashlib.sha256(f"{code}:{settings.SECRET_KEY}".encode("utf-8")).hexdigest()


def _to_user_dict(user: User) -> dict:
    return {"id": user.id, "email": user.email, "phone_number": user.phone_number or ""}


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, payload: RegisterRequest) -> dict:
        email = payload.email.lower()
        existing = self.db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = User(
            email=email,
            password_hash=hash_password(payload.password),
            phone_number=self._normalize_phone(payload.phone_number),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer", "user": _to_user_dict(user)}

    def login(self, payload: LoginRequest) -> dict:
        email = payload.email.lower()
        user = self.db.query(User).filter(or_(User.email == email)).first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        user.last_login = datetime.utcnow()
        self.db.commit()
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer", "user": _to_user_dict(user)}

    def me(self, user: User) -> dict:
        return _to_user_dict(user)

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        digits = "".join(ch for ch in str(phone or "") if ch.isdigit())
        return digits[-10:] if digits else ""

    def _deliver_otp(self, user: User, otp: str) -> None:
        subject = "Your VittVaani password reset OTP"
        body = (
            f"Hello,\n\n"
            f"Use this one-time code to reset your password:\n\n"
            f"    {otp}\n\n"
            f"This code expires in {OTP_EXPIRE_MINUTES} minutes.\n"
            f"If you didn't request this, you can safely ignore this email.\n\n"
            f"- VittVaani Team"
        )
        delivered = send_email(user.email, subject, body)
        print(f"[OTP] For {user.email}: code {otp} -> email delivery {'OK' if delivered else 'SKIPPED (SMTP not configured)'}")

    def forgot_password(self, email: str) -> dict:
        user = self.db.query(User).filter(User.email == email.lower()).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        self.db.query(OtpCode).filter(
            OtpCode.email == user.email, OtpCode.purpose == "password_reset"
        ).delete()
        self.db.commit()

        otp = f"{secrets.randbelow(1000000):06d}"
        new_code = OtpCode(
            email=user.email,
            code_hash=_hash_otp(otp),
            purpose="password_reset",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
        )
        self.db.add(new_code)
        self.db.commit()
        self._deliver_otp(user, otp)

        result = {
            "message": f"An OTP has been sent to your registered email (valid for {OTP_EXPIRE_MINUTES} minutes)",
            "expires_in_minutes": OTP_EXPIRE_MINUTES,
        }
        return result

    def verify_otp(self, email: str, otp: str) -> dict:
        normalized_email = email.lower()
        user = self.db.query(User).filter(User.email == normalized_email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        code = (
            self.db.query(OtpCode)
            .filter(
                OtpCode.email == normalized_email,
                OtpCode.purpose == "password_reset",
                OtpCode.used.is_(False),
            )
            .order_by(OtpCode.id.desc())
            .first()
        )
        if code is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No OTP requested for this account")
        if code.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP has expired. Please request a new one")
        if code.attempts >= OTP_MAX_ATTEMPTS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Too many incorrect attempts. Please request a new OTP")

        if not secrets.compare_digest(code.code_hash, _hash_otp(otp.strip())):
            code.attempts += 1
            self.db.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP. Please try again")

        code.used = True
        self.db.commit()
        reset_token = create_access_token(user.id, expires_delta=timedelta(minutes=15), token_type="reset")
        return {"reset_token": reset_token, "message": "OTP verified. You can now set a new password"}

    def reset_password(self, token: str, new_password: str) -> dict:
        payload = decode_token(token)
        if payload.get("typ") != "reset":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid reset token")
        user = self.db.query(User).filter(User.id == payload["user_id"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.password_hash = hash_password(new_password)
        self.db.commit()
        return {"message": "Password reset successfully"}