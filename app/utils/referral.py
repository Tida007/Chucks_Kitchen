import secrets
import string
from sqlalchemy.orm import Session
from app.models.user import User

def generate_referral_code() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(alphabet) for i in range(8))

def validate_referral_code(db: Session, code: str) -> User | None:
    user = db.query(User).filter(User.referral_code == code).first()
    return user