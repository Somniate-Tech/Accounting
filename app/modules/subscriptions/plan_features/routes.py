from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.modules.subscriptions.plan_features.schema import (
    PlanFeatureCreate,
    PlanFeatureResponse
)

from app.modules.subscriptions.plan_features.service import (
    PlanFeatureService
)
from app.core.admin_guard import (get_current_super_admin)

router = APIRouter(
    prefix="/plan-features",
    tags=["Plan Features"]
)


@router.post(
    "",
    response_model=PlanFeatureResponse
)
def create_plan_feature(
    payload: PlanFeatureCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        PlanFeatureService.create_plan_feature(
            db=db,
            payload=payload
        )
    )


@router.get(
    "",
    response_model=list[PlanFeatureResponse]
)
def get_all_plan_features(
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        PlanFeatureService.get_all_plan_features(
            db=db
        )
    )


@router.get(
    "/plan/{plan_id}",
    response_model=list[PlanFeatureResponse]
)
def get_plan_features(
    plan_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        PlanFeatureService.get_plan_features(
            db=db,
            plan_id=plan_id
        )
    )