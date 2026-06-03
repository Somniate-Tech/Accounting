from fastapi import (
    Depends,
    HTTPException
)

from app.modules.users.model import User

from app.core.dependencies import (
    get_current_user
)

from app.core.constants import (
    UserRoles
)


def get_current_super_admin(
    current_user: User = Depends(
        get_current_user
    )
):

    if current_user.role != UserRoles.SUPER_ADMIN:

        raise HTTPException(
            status_code=403,
            detail="Super Admin access required"
        )

    return current_user