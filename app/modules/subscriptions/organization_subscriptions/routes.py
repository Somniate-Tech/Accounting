from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.modules.users.model import User

from app.modules.subscriptions.organization_subscriptions.schema import (
    OrganizationSubscriptionCreate,
    OrganizationSubscriptionResponse,
    ChoosePlanSchema,
    UpgradePlanSchema
)

from app.modules.subscriptions.organization_subscriptions.service import (
    OrganizationSubscriptionService
)
from app.core.admin_guard import (get_current_super_admin)
router = APIRouter(
    prefix="/organization-subscriptions",
    tags=["Organization Subscriptions"]
)


# ==================================================
# BASIC CRUD
# ==================================================

@router.post(
    "",
    response_model=OrganizationSubscriptionResponse
)
def create_subscription(
    payload: OrganizationSubscriptionCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    ),
    current_user: User = Depends(
        get_current_user
    ),
):

    return (
        OrganizationSubscriptionService.create_subscription(
            db=db,
            payload=payload
        )
    )


@router.get(
    "",
    response_model=list[OrganizationSubscriptionResponse]
)
def get_all_subscriptions(
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        OrganizationSubscriptionService.get_all_subscriptions(
            db=db
        )
    )


# ==================================================
# CURRENT SUBSCRIPTION
# ==================================================

@router.get("/current")
def get_current_subscription(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .get_current_subscription(
            db=db,
            user_id=current_user.id
        )
    )


# ==================================================
# SUBSCRIPTION HISTORY
# ==================================================

@router.get("/history")
def get_subscription_history(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .get_subscription_history(
            db=db,
            user_id=current_user.id
        )
    )


# ==================================================
# CHOOSE PLAN
# ==================================================

@router.post("/choose-plan")
def choose_plan(

    payload: ChoosePlanSchema,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .choose_plan(
            db=db,
            plan_id=payload.plan_id,
            user_id=current_user.id
        )
    )


# ==================================================
# UPGRADE PLAN
# ==================================================

@router.post("/upgrade-plan")
def upgrade_plan(

    payload: UpgradePlanSchema,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .upgrade_plan(
            db=db,
            user_id=current_user.id,
            plan_id=payload.plan_id
        )
    )


# ==================================================
# RENEW SUBSCRIPTION
# ==================================================

@router.post("/renew")
def renew_subscription(

    current_user: User = Depends(
        get_current_user
    ),


    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .renew_subscription(
            db=db,
            user_id=current_user.id
        )
    )


# ==================================================
# CANCEL SUBSCRIPTION
# ==================================================

@router.post("/cancel")
def cancel_subscription(

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(get_db)
):

    return (
        OrganizationSubscriptionService
        .cancel_subscription(
            db=db,
            user_id=current_user.id
        )
    )


# ==================================================
# GET BY ID (KEEP LAST)
# ==================================================

@router.get(
    "/{subscription_id}",
    response_model=OrganizationSubscriptionResponse
)
def get_subscription_by_id(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    ),
    current_user: User = Depends(
        get_current_user
    ),
):

    return (
        OrganizationSubscriptionService.get_subscription_by_id(
            db=db,
            subscription_id=subscription_id
        )
    )