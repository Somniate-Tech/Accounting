from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.subscriptions.features.repository import (
    FeatureRepository
)

from app.modules.subscriptions.features.schema import (
    FeatureCreate
)


class FeatureService:

    @staticmethod
    def create_feature(
        db: Session,
        payload: FeatureCreate
    ):

        existing_feature = (
            FeatureRepository.get_by_code(
                db=db,
                code=payload.code
            )
        )

        if existing_feature:
            raise HTTPException(
                status_code=400,
                detail="Feature code already exists"
            )

        return (
            FeatureRepository.create(
                db=db,
                payload=payload
            )
        )

    @staticmethod
    def get_all_features(
        db: Session
    ):

        return (
            FeatureRepository.get_all(
                db=db
            )
        )

    @staticmethod
    def get_feature_by_id(
        db: Session,
        feature_id: int
    ):

        feature = (
            FeatureRepository.get_by_id(
                db=db,
                feature_id=feature_id
            )
        )

        if not feature:
            raise HTTPException(
                status_code=404,
                detail="Feature not found"
            )

        return feature