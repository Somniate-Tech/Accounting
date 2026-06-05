from pydantic import (
    BaseModel,
    EmailStr
)

from typing import Optional


class SendOTPSchema(BaseModel):

    email: EmailStr


class VerifyOTPSchema(BaseModel):

    email: EmailStr

    otp: str


class RegisterSchema(BaseModel):

    organization_type: str

    organization_name: str

    email: EmailStr

    password: str

    gst_number: Optional[str] = None

    phone: Optional[str] = None

    address: Optional[str] = None


class LoginSchema(BaseModel):

    email: EmailStr

    password: str


class ForgotPasswordSchema(BaseModel):
    email: str


class ResetPasswordSchema(BaseModel):
    email: str
    otp: str
    new_password: str