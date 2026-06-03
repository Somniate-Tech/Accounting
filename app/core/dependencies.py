from fastapi import (
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.core.security import (
    decode_access_token
)
from app.modules.organizations.repository import (
    get_user_organization_repo
)

from app.modules.users.model import User
from app.modules.organizations.model import (
    Organization
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def get_current_organization(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    organization_member = (
        get_user_organization_repo(
            db,
            current_user.id
        )
    )

    if not organization_member:

        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    organization = (
        db.query(Organization)
        .filter(
            Organization.id ==
            organization_member.organization_id
        )
        .first()
    )

    if not organization:

        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    if not organization.is_active:

        raise HTTPException(
            status_code=403,
            detail=(
                "Organization has been deactivated. "
                "Please contact support."
            )
        )

    return organization.id