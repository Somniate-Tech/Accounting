from fastapi import APIRouter
from fastapi import Depends
from typing import List
from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db
)

from app.core.admin_guard import (
    get_current_super_admin
)

from app.modules.admin.service import (
    AdminService
)

from app.modules.admin.schema import (
    AdminDashboardResponse,
    OrganizationResponse,
    UserResponse,
    SubscriptionResponse,
    RevenueDashboardResponse
)

router = APIRouter(
    prefix="/admin",
    tags=["Super Admin"]
)


@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_dashboard(
            db=db
        )
    )


@router.get(
    "/organizations",
    response_model=List[
        OrganizationResponse
    ]
)
def get_all_organizations(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_all_organizations(
            db=db
        )
    )

@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_all_users(
            db=db
        )
    )

@router.get(
    "/subscriptions",
    response_model=list[
        SubscriptionResponse
    ]
)
def get_all_subscriptions(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_all_subscriptions(
            db=db
        )
    )

@router.patch(
    "/organizations/{organization_id}/deactivate"
)
def deactivate_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.deactivate_organization(
            db=db,
            organization_id=organization_id
        )
    )


@router.patch(
    "/organizations/{organization_id}/activate"
)
def activate_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.activate_organization(
            db=db,
            organization_id=organization_id
        )
    )


@router.get(
    "/subscriptions/expired",
    response_model=list[
        SubscriptionResponse
    ]
)
def get_expired_subscriptions(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_expired_subscriptions(
            db=db
        )
    )


@router.get(
    "/subscriptions/trials",
    response_model=list[
        SubscriptionResponse
    ]
)
def get_trial_subscriptions(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_trial_subscriptions(
            db=db
        )
    )



@router.get(
    "/subscriptions/expiring",
    response_model=list[
        SubscriptionResponse
    ]
)
def get_expiring_subscriptions(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_expiring_subscriptions(
            db=db
        )
    )


@router.get(
    "/revenue",
    response_model=
    RevenueDashboardResponse
)
def get_revenue_dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(
        get_current_super_admin
    )
):

    return (
        AdminService.get_revenue_dashboard(
            db=db
        )
    )