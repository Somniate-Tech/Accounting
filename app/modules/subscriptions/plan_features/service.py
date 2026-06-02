from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.subscriptions.plan_features.repository import (
    PlanFeatureRepository
)

from app.modules.subscriptions.plan_features.schema import (
    PlanFeatureCreate
)


class PlanFeatureService:

    @staticmethod
    def create_plan_feature(
        db: Session,
        payload: PlanFeatureCreate
    ):

        existing = (
            PlanFeatureRepository
            .get_by_plan_and_feature(
                db=db,
                plan_id=payload.plan_id,
                feature_id=payload.feature_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Feature already assigned to this plan"
            )

        return (
            PlanFeatureRepository.create(
                db=db,
                payload=payload
            )
        )

    @staticmethod
    def get_all_plan_features(
        db: Session
    ):

        return (
            PlanFeatureRepository.get_all(
                db=db
            )
        )

    @staticmethod
    def get_plan_features(
        db: Session,
        plan_id: int
    ):

        return (
            PlanFeatureRepository.get_by_plan(
                db=db,
                plan_id=plan_id
            )
        )