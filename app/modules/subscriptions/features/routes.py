from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.modules.subscriptions.features.schema import (
    FeatureCreate,
    FeatureResponse
)

from app.modules.subscriptions.features.service import (
    FeatureService
)
from app.core.admin_guard import (
    get_current_super_admin
)

router = APIRouter(
    prefix="/features",
    tags=["Features"]
)


@router.post(
    "",
    response_model=FeatureResponse
)
def create_feature(
    payload: FeatureCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        FeatureService.create_feature(
            db=db,
            payload=payload
        )
    )


@router.get(
    "",
    response_model=list[FeatureResponse]
)
def get_all_features(
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        FeatureService.get_all_features(
            db=db
        )
    )


@router.get(
    "/{feature_id}",
    response_model=FeatureResponse
)
def get_feature_by_id(
    feature_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(
        get_current_super_admin
    )
):

    return (
        FeatureService.get_feature_by_id(
            db=db,
            feature_id=feature_id
        )
    )