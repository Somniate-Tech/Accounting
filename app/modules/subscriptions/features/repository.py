from sqlalchemy.orm import Session

from app.modules.subscriptions.features.model import (
    Feature
)

from app.modules.subscriptions.features.schema import (
    FeatureCreate
)


class FeatureRepository:

    @staticmethod
    def create(
        db: Session,
        payload: FeatureCreate
    ):

        feature = Feature(
            name=payload.name,
            code=payload.code,
            description=payload.description
        )

        db.add(feature)

        db.commit()

        db.refresh(feature)

        return feature

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(
                Feature
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        feature_id: int
    ):

        return (
            db.query(
                Feature
            )
            .filter(
                Feature.id == feature_id
            )
            .first()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        code: str
    ):

        return (
            db.query(
                Feature
            )
            .filter(
                Feature.code == code
            )
            .first()
        )