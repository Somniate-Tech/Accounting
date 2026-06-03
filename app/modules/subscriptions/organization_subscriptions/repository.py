from sqlalchemy.orm import Session

from app.modules.subscriptions.organization_subscriptions.model import (
    OrganizationSubscription
)

from app.modules.subscriptions.organization_subscriptions.schema import (
    OrganizationSubscriptionCreate
)


class OrganizationSubscriptionRepository:

    @staticmethod
    def create(
        db: Session,
        payload: OrganizationSubscriptionCreate
    ):

        subscription = OrganizationSubscription(
            organization_id=payload.organization_id,
            plan_id=payload.plan_id,

            status=payload.status,

            start_date=payload.start_date,
            end_date=payload.end_date,

            is_trial=payload.is_trial
        )

        db.add(subscription)

        db.commit()

        db.refresh(subscription)

        return subscription

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        subscription_id: int
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.id == subscription_id
            )
            .first()
        )

    @staticmethod
    def get_active_subscription(
        db: Session,
        organization_id: int
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.organization_id == organization_id,
                OrganizationSubscription.status == "ACTIVE"
            )
            .first()
        )
    

    @staticmethod
    def get_by_organization(
        db: Session,
        organization_id: int
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.organization_id
                == organization_id
            )
            .order_by(
                OrganizationSubscription.id.desc()
            )
            .all()
        )
    

    @staticmethod
    def get_active_subscription_by_organization(
        db,
        organization_id: int
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.organization_id == organization_id,
                OrganizationSubscription.status == "ACTIVE"
            )
            .first()
        )