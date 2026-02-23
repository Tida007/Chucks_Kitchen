import random
import string
from datetime import datetime, timezone

def generate_otp() -> str:
    simulated_number = random.randint(100000, 999999)
    return str(simulated_number)

def is_otp_expired(expires_at: datetime) -> bool:
    # Checks if current utc time has passed the expiration time
    if not expires_at:
        return True
    
    # Get current UTC time
    now = datetime.now(timezone.utc)

    # Crash Prevention: If Sqlite stripped timezone info, this adds it back safely
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    # Returns True if current time has expired
    return now > expires_at

def verify_otp(stored_code: str, provided_code: str, expires_at: datetime) -> bool:
    # If OTP is not correct or expired, return False cleanly
    if stored_code != provided_code:
        return False
    
    if is_otp_expired(expires_at):
        return False
    return True