from sqlalchemy.orm import Session

from app.modules.users.model import User

from app.modules.organizations.model import Organization

from app.modules.organization_members.model import (
    OrganizationMember
)
from app.core.constants import UserRoles


def get_user_by_email_repo(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def create_user_repo(
    db: Session,
    email: str,
    password: str
):

    user = User(
        email=email,
        password=password,
        role=UserRoles.OWNER
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def create_organization_repo(
    db: Session,
    organization_name: str,
    organization_type: str,
    gst_number: str,
    phone: str,
    address: str,
    created_by: int,
    photo=None
):

    organization = Organization(
        organization_name=organization_name,
        organization_type=organization_type,
        gst_number=gst_number,
        phone=phone,
        address=address,
        created_by=created_by,
        photo=photo
    )

    db.add(organization)

    db.commit()

    db.refresh(organization)

    return organization


def create_organization_member_repo(
    db: Session,
    organization_id: int,
    user_id: int
):

    member = OrganizationMember(
        organization_id=organization_id,
        user_id=user_id,
        role="owner"
    )

    db.add(member)

    db.commit()

    db.refresh(member)

    return member