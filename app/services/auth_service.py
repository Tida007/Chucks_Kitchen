import bcrypt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.config import settings
from fastapi import Request
from app.database import get_db

from app.models.user import User
from app.utils import otp
from app.utils.otp import generate_otp, verify_otp
from app.utils.referral import generate_referral_code, validate_referral_code


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    # Find user by ID
    return db.query(User).filter(User.id == user_id).first()

def register_user(
        db: Session,
        email: str,
        phone: str,
        password: str,
        referral_code: str = None
):
    """Registers a new user, hashes password, genertes OTP and referral codes"""

    hashed_password = get_password_hash(password)

    # This generates OTP and set expiration (e.g 10 min from now)
    otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Generate a unique referral code for new user
    new_referral = generate_referral_code()

    # Admin check:
    is_first_user = db.query(User).count() == 0

    new_user = User(
        email=email,
        phone=phone,
        hashed_password=hashed_password,
        is_admin=is_first_user,
        otp_code=otp,
        otp_expires_at=expires_at,
        referral_code=new_referral
    )

    if referral_code:
        referral = validate_referral_code(db, referral_code)
        if referral:
            pass

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #return the OTP alongside the user 
    return new_user, otp

def verify_email(db: Session, email: str, otp_code: str) -> bool:
    user = get_user_by_email(db, email)

    if not user:
        return False
    
    # Utility function to check the code and expiration
    if verify_otp(user.otp_code, otp_code, user.otp_expires_at):
        #update user status
        user.is_verified = True
        #Clear OTP data so it can't be reused
        user.otp_code = None
        user.otp_expires_at = None

        db.commit()
        return True

    return False

def resend_verification_otp(db: Session, email: str) -> str | None:
    user = get_user_by_email(db, email)

    if not user:
        return None
    if user.is_verified:
        return "User already verified"
    
    # Generate new OTP and expiration
    new_otp = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

    # Update user record
    user.otp_code = new_otp
    user.otp_expires_at = expires_at

    db.commit()

    return new_otp