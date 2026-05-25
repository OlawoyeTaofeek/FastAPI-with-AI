from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator, ConfigDict
import re

def validate_password_strength(password: str) ->str:
    """
    Enforces password rules at the schema level — before it
    ever reaches the service or database.
 
    Rules:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    return password

class RegisterRequest(BaseModel):
    """Payload for POST /auth/register"""
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
 
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Full name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Full name must be under 100 characters")
        return v
 
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)
 
    @model_validator(mode="after")
    def passwords_must_match(self) -> "RegisterRequest":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class LoginRequest(BaseModel):
    """Payload for POST /auth/login"""
    email: EmailStr
    password: str
 
 
class RefreshTokenRequest(BaseModel):
    """Payload for POST /auth/refresh"""
    refresh_token: str
 
 
class EmailVerifyRequest(BaseModel):
    """Payload for POST /auth/verify-email"""
    token: str                  # token from the email link
 
 
class ResendVerificationRequest(BaseModel):
    """Payload for POST /auth/resend-verification"""
    email: EmailStr
 
 
class PasswordResetRequest(BaseModel):
    """Payload for POST /auth/forgot-password"""
    email: EmailStr             # triggers sending reset email
 
 
class PasswordResetConfirmRequest(BaseModel):
    """Payload for POST /auth/reset-password"""
    token: str                  # token from reset email
    new_password: str
    confirm_password: str
 
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)
 
    @model_validator(mode="after")
    def passwords_must_match(self) -> "PasswordResetConfirmRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
 
 
class ChangePasswordRequest(BaseModel):
    """Payload for POST /auth/change-password (logged in user)"""
    current_password: str
    new_password: str
    confirm_password: str
 
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return validate_password_strength(v)
 
    @model_validator(mode="after")
    def passwords_must_match(self) -> "ChangePasswordRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
 
class UserResponse(BaseModel):
    """
    Safe user representation — whitelisted fields only.
    Never return the full DB model directly.
    """
    id: str
    full_name: str
    email: EmailStr
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
 
    model_config = ConfigDict(from_attributes=True)
 
 
class TokenResponse(BaseModel):
    """
    Returned on login and token refresh.
    expires_in lets the frontend know exactly when to refresh.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int             
 
 
class LoginResponse(BaseModel):
    """
    Full login response — tokens + user in one payload.
    Frontend gets everything it needs in one request.
    """
    tokens: TokenResponse
    user: UserResponse
 
 
class MessageResponse(BaseModel):
    """
    Generic success response for operations that don't return data.
    e.g. "Verification email sent", "Password reset successfully"
    """
    message: str
    success: bool = True
 