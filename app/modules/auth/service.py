from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.auth.repository import (
    get_user_by_email_repo,
    create_user_repo,
    create_organization_repo,
    create_organization_member_repo,
    update_user_password_repo,
)

from app.modules.auth.utils import (
    send_otp_email,
    verify_otp,
    is_email_verified
)

from app.modules.auth.schema import (
    RegisterSchema
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.modules.organization_members.model import (
    OrganizationMember
)

from app.modules.organizations.model import (
    Organization
)
from datetime import datetime, timedelta

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)

from app.modules.subscriptions.organization_subscriptions.model import (
    OrganizationSubscription
)
from app.modules.accounting.chart_of_accounts.service import (
    ChartOfAccountService
)

async def send_otp_service(
    db: Session,
    email: str
):

    existing_user = get_user_by_email_repo(
        db,
        email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    await send_otp_email(email)

    return {
        "message": "OTP sent successfully"
    }


def verify_otp_service(
    email: str,
    otp: str
):

    is_valid = verify_otp(
        email,
        otp
    )

    if not is_valid:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    return {
        "message": "OTP verified successfully"
    }


def register_service(
    db: Session,
    payload: RegisterSchema,
    photo=None
):

    if not is_email_verified(payload.email):

        raise HTTPException(
            status_code=400,
            detail="Email not verified"
        )

    existing_user = get_user_by_email_repo(
        db,
        payload.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        payload.password
    )

    user = create_user_repo(
        db=db,
        email=payload.email,
        password=hashed_password
    )

    organization = create_organization_repo(
        db=db,
        organization_name=payload.organization_name,
        organization_type=payload.organization_type,
        gst_number=payload.gst_number,
        phone=payload.phone,
        address=payload.address,
        created_by=user.id,
        photo=photo
    )

    ChartOfAccountService.create_default_chart_of_accounts(
    db=db,
    organization_id=organization.id
    )

    create_organization_member_repo(
        db=db,
        organization_id=organization.id,
        user_id=user.id
    )
    starter_plan = (
        db.query(SubscriptionPlan)
        .filter(
            SubscriptionPlan.code == "STARTER",
            SubscriptionPlan.is_active == True
        )
        .first()
    )

    if not starter_plan:

        raise HTTPException(
            status_code=500,
            detail="Starter plan not configured"
        )

    trial_subscription = OrganizationSubscription(
        organization_id=organization.id,

        plan_id=starter_plan.id,

        status="ACTIVE",

        start_date=datetime.utcnow(),

        end_date=datetime.utcnow() + timedelta(days=30),

        is_trial=True
    )

    db.add(trial_subscription)

    db.commit()
    db.refresh(trial_subscription)

    return {
        "message": "Account created successfully"
    }


def login_service(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email_repo(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    is_valid_password = verify_password(
        password,
        user.password
    )

    if not is_valid_password:

        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    organization_member = db.query(
        OrganizationMember
    ).filter(
        OrganizationMember.user_id == user.id
    ).first()

    if not organization_member:

        raise HTTPException(
            status_code=404,
            detail="Organization membership not found"
        )

    organization = db.query(
        Organization
    ).filter(
        Organization.id == organization_member.organization_id
    ).first()

    if not organization:

        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email
        }
    )

    return {

        "access_token": access_token,

        "token_type": "bearer",

        "user": {

            "id": user.id,

            "email": user.email,

            "role": user.role,
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
        }
    }


async def forgot_password_service(
    db: Session,
    email: str
):

    user = get_user_by_email_repo(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await send_otp_email(email)

    return {
        "message": "OTP sent successfully"
    }

def reset_password_service(
    db: Session,
    email: str,
    otp: str,
    new_password: str
):

    is_valid = verify_otp(
        email,
        otp
    )

    if not is_valid:

        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    user = get_user_by_email_repo(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    hashed_password = hash_password(
        new_password
    )

    update_user_password_repo(
        db,
        user,
        hashed_password
    )

    return {
        "message": "Password reset successfully"
    }