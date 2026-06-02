from sqlalchemy.orm import Session

from app.modules.subscriptions.plan_features.model import (
    PlanFeature
)

from app.modules.subscriptions.plan_features.schema import (
    PlanFeatureCreate
)


class PlanFeatureRepository:

    @staticmethod
    def create(
        db: Session,
        payload: PlanFeatureCreate
    ):

        plan_feature = PlanFeature(
            plan_id=payload.plan_id,
            feature_id=payload.feature_id
        )

        db.add(plan_feature)

        db.commit()

        db.refresh(plan_feature)

        return plan_feature

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(
                PlanFeature
            )
            .all()
        )

    @staticmethod
    def get_by_plan_and_feature(
        db: Session,
        plan_id: int,
        feature_id: int
    ):

        return (
            db.query(
                PlanFeature
            )
            .filter(
                PlanFeature.plan_id == plan_id,
                PlanFeature.feature_id == feature_id
            )
            .first()
        )

    @staticmethod
    def get_by_plan(
        db: Session,
        plan_id: int
    ):

        return (
            db.query(
                PlanFeature
            )
            .filter(
                PlanFeature.plan_id == plan_id
            )
            .all()
        )