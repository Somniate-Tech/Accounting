from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    HTTPException
)

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.modules.auth.schema import (
    SendOTPSchema,
    VerifyOTPSchema,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)

from app.core.dependencies import (
    get_current_user,
    get_current_organization
)

from app.modules.users.model import User

from app.modules.auth.service import (
    send_otp_service,
    verify_otp_service,
    register_service,
    login_service,
    forgot_password_service,
    reset_password_service
)
from sqlalchemy.orm import joinedload

from app.modules.organization_members.model import (
    OrganizationMember
)

import shutil

import os


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/send-otp")
async def send_otp(
    payload: SendOTPSchema,
    db: Session = Depends(get_db)
):

    return await send_otp_service(
        db,
        payload.email
    )


@router.post("/verify-otp")
def verify_otp(
    payload: VerifyOTPSchema
):

    return verify_otp_service(
        payload.email,
        payload.otp
    )


@router.post("/register")
def register(

    organization_type: str = Form(...),

    organization_name: str = Form(...),

    email: str = Form(...),

    password: str = Form(...),

    gst_number: str = Form(None),

    phone: str = Form(None),

    address: str = Form(None),

    photo: UploadFile = File(None),

    db: Session = Depends(get_db)
):

    photo_path = None

    if photo:

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        ]

        file_extension = os.path.splitext(
            photo.filename
        )[1].lower()

        if file_extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail="Invalid image format"
            )

        filename = (
            f"{email.replace('@', '_')}"
            f"{file_extension}"
        )

        # Create upload directory if it doesn't exist
        upload_dir = os.path.join("uploads", "organizations")
        os.makedirs(upload_dir, exist_ok=True)

        # Full file path
        file_path = os.path.join(upload_dir, filename)

        # Save uploaded image
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        # Store relative path in database
        photo_path = file_path

    payload = RegisterSchema(

        organization_type=organization_type,

        organization_name=organization_name,

        email=email,

        password=password,

        gst_number=gst_number,

        phone=phone,

        address=address
    )

    return register_service(
        db=db,
        payload=payload,
        photo=photo_path
    )


@router.post("/login")
def login(
    payload: LoginSchema,
    db: Session = Depends(get_db)
):

    return login_service(
        db,
        payload.email,
        payload.password,
    )


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


@router.get("/my-organization")
def my_organization(
    organization = Depends(get_current_organization)
):

    return {
        "organization_id": organization.organization_id,
        "role": organization.role
    }


@router.get("/profile")
def get_profile(

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)
):

    organization_member = db.query(
        OrganizationMember
    ).options(
        joinedload(
            OrganizationMember.organization
        )
    ).filter(
        OrganizationMember.user_id == current_user.id
    ).first()

    if not organization_member:

        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    organization = organization_member.organization

    return {

        "user": {

            "id": current_user.id,

            "email": current_user.email
        },

        "organization": {

            "id": organization.id,

            "organization_name": organization.organization_name,

            "organization_type": organization.organization_type,

            "gst_number": organization.gst_number,

            "phone": organization.phone,

            "address": organization.address,

            "photo": organization.photo,

            "created_at": organization.created_at
        },

        "membership": {

            "role": organization_member.role
        }
    }


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordSchema,
    db: Session = Depends(get_db)
):

    return await forgot_password_service(
        db,
        payload.email
    )


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordSchema,
    db: Session = Depends(get_db)
):

    return reset_password_service(
        db,
        payload.email,
        payload.otp,
        payload.new_password
    )