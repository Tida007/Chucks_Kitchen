from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut, UserVerify, OTPResend, UserLogin
from datetime import timedelta
from app.database import get_db, SessionLocal
from app.services.auth_service import get_user_by_email, register_user, verify_email, resend_verification_otp, verify_password


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    # check if email already exist
    existing_user = get_user_by_email(db, email=user_data.email)
    if existing_user :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credentials already exists"
        )

    # Call service logic
    new_user, otp = register_user(
        db=db,
        email=user_data.email,
        phone=user_data.phone,
        password=user_data.password
    )

    # Simulate sending OTP to console
    print(f"\n--- OTP SIMULATED CODE ---")
    print(f"Code for {new_user.email}: {otp}")
    print(f"---------------\n")

    return new_user

@router.post("/verify")
def verify_account(verify_data: UserVerify, db: Session = Depends(get_db)):
    success = verify_email(db, verify_data.email, verify_data.otp_code)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Credentials/expired OTP"
        )
    
    return {"message": "Account verified successfully"}

@router.post("/login")
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):

    # Find user by email
    user = get_user_by_email(db, credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if verified
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified please verify your email")
    
    # Store user_id in Session (secure cookie)
    request.session["user_id"] = user.id
    request.session["email"] = user.email

    return {
        "message": "Login successful",
        "user": UserOut.from_orm(user)
    }

@router.post("/resend-otp")
def resend_otp(request: OTPResend, db: Session = Depends(get_db)):
    result = resend_verification_otp(db, request.email)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if result == "already_verified":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Acoount is already verified")
    
    print((f"\n---- NEW OTP SIMULATED CODE ----"))
    print(f"New Code for {request.email}: {result}")
    print(f"-------------------\n")

    return {"message": "A new verification code has been sent to your email"}

@router.post("/logout")
def logout(request: Request):
    """Clear session (logout)"""

    request.session.clear()

    return{"message": "Logout out successfully"}