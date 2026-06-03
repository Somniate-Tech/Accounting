from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.modules.subscriptions.plans.schema import (
    SubscriptionPlanCreate,
    SubscriptionPlanResponse
)

from app.modules.subscriptions.plans.service import (
    SubscriptionPlanService,
    SubscriptionPlanUpdate
)

router = APIRouter(
    prefix="/subscription-plans",
    tags=["Subscription Plans"]
)


@router.post(
    "",
    response_model=SubscriptionPlanResponse
)
def create_plan(
    payload: SubscriptionPlanCreate,
    db: Session = Depends(get_db)
):

    return SubscriptionPlanService.create_plan(
        db=db,
        payload=payload
    )


@router.get(
    "",
    response_model=list[SubscriptionPlanResponse]
)
def get_all_plans(
    db: Session = Depends(get_db)
):

    return SubscriptionPlanService.get_all_plans(
        db=db
    )


@router.get(
    "/{plan_id}",
    response_model=SubscriptionPlanResponse
)
def get_plan_by_id(
    plan_id: int,
    db: Session = Depends(get_db)
):

    return SubscriptionPlanService.get_plan_by_id(
        db=db,
        plan_id=plan_id
    )


@router.put(
    "/{plan_id}",
    response_model=SubscriptionPlanResponse
)
def update_plan(
    plan_id: int,
    payload: SubscriptionPlanUpdate,
    db: Session = Depends(get_db)
):

    return (
        SubscriptionPlanService.update_plan(
            db=db,
            plan_id=plan_id,
            payload=payload
        )
    )

@router.patch(
    "/{plan_id}/activate"
)
def activate_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    return (
        SubscriptionPlanService.activate_plan(
            db=db,
            plan_id=plan_id
        )
    )


@router.patch(
    "/{plan_id}/deactivate"
)
def deactivate_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    return (
        SubscriptionPlanService.deactivate_plan(
            db=db,
            plan_id=plan_id
        )
    )