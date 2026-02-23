from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    phone: str = Field(..., pattern=r"^\d+$", min_length=10, max_length=15, description="Only numbers allowed")  # Basic phone number validation

# API recieves this during registration (POST request)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# API responds back to client with this (GET request)
class UserOut(UserBase):
    id: int
    is_admin: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

# OTP Verification Schema
class UserVerify(BaseModel):
    email: EmailStr
    otp_code: str

class OTPResend(BaseModel):
    email: EmailStr