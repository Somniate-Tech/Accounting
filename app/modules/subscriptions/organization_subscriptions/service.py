from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.modules.organizations.model import (
    Organization
)

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)

from app.modules.subscriptions.organization_subscriptions.repository import (
    OrganizationSubscriptionRepository
)

from app.modules.subscriptions.organization_subscriptions.schema import (
    OrganizationSubscriptionCreate
)


from app.modules.organization_members.model import (
    OrganizationMember,
    OrganizationMember,
)

from app.modules.subscriptions.organization_subscriptions.model import (
    OrganizationSubscription
)


class OrganizationSubscriptionService:

    @staticmethod
    def create_subscription(
        db: Session,
        payload: OrganizationSubscriptionCreate
    ):

        organization = (
            db.query(Organization)
            .filter(
                Organization.id == payload.organization_id
            )
            .first()
        )

        if not organization:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        plan = (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.id == payload.plan_id
            )
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        existing_subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=payload.organization_id
            )
        )

        if existing_subscription:
            raise HTTPException(
                status_code=400,
                detail="Organization already has an active subscription"
            )

        return (
            OrganizationSubscriptionRepository.create(
                db=db,
                payload=payload
            )
        )

    @staticmethod
    def get_all_subscriptions(
        db: Session
    ):

        return (
            OrganizationSubscriptionRepository.get_all(
                db=db
            )
        )

    @staticmethod
    def get_subscription_by_id(
        db: Session,
        subscription_id: int
    ):

        subscription = (
            OrganizationSubscriptionRepository.get_by_id(
                db=db,
                subscription_id=subscription_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found"
            )

        return subscription
    

    @staticmethod
    def choose_plan(
        db: Session,
        plan_id: int,
        user_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        organization_id = (
            organization_member.organization_id
        )

        plan = (
            db.query(
                SubscriptionPlan
            )
            .filter(
                SubscriptionPlan.id == plan_id
            )
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        existing_subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=organization_id
            )
        )

        if existing_subscription:
            raise HTTPException(
                status_code=400,
                detail="Organization already has an active subscription"
            )

        subscription = OrganizationSubscription(
            organization_id=organization_id,
            plan_id=plan_id,

            status="ACTIVE",

            start_date=datetime.utcnow(),

            end_date=datetime.utcnow()
            + timedelta(days=30),

            is_trial=False
        )

        db.add(subscription)

        db.commit()

        db.refresh(subscription)

        return subscription
    

    @staticmethod
    def get_current_subscription(
        db: Session,
        user_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        subscription = (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.organization_id
                == organization_member.organization_id,

                OrganizationSubscription.status
                == "ACTIVE"
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )

        return subscription
    

    @staticmethod
    def upgrade_plan(
        db: Session,
        user_id: int,
        plan_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=organization_member.organization_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )

        plan = (
            db.query(
                SubscriptionPlan
            )
            .filter(
                SubscriptionPlan.id == plan_id
            )
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        subscription.plan_id = plan_id

        db.commit()

        db.refresh(subscription)

        return {
            "message": "Subscription upgraded successfully",
            "plan_id": plan_id
        }
    

    @staticmethod
    def renew_subscription(
        db: Session,
        user_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=organization_member.organization_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )

        subscription.end_date = (
            subscription.end_date
            + timedelta(days=30)
        )

        db.commit()

        db.refresh(subscription)

        return {
            "message": "Subscription renewed successfully",
            "new_end_date": subscription.end_date
        }
    

    @staticmethod
    def cancel_subscription(
        db: Session,
        user_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=organization_member.organization_id
            )
        )

        if not subscription:
            raise HTTPException(
                status_code=404,
                detail="No active subscription found"
            )

        subscription.status = "CANCELLED"

        db.commit()

        db.refresh(subscription)

        return {
            "message": "Subscription cancelled successfully"
        }
    


    @staticmethod
    def get_subscription_history(
        db: Session,
        user_id: int
    ):

        organization_member = (
            db.query(
                OrganizationMember
            )
            .filter(
                OrganizationMember.user_id == user_id
            )
            .first()
        )

        if not organization_member:
            raise HTTPException(
                status_code=404,
                detail="Organization not found"
            )

        return (
            OrganizationSubscriptionRepository
            .get_by_organization(
                db=db,
                organization_id=
                organization_member.organization_id
            )
        )
    
    @staticmethod
    def activate_paid_subscription(
            db: Session,
            organization_id: int,
            plan_id: int,
            billing_cycle: str
    ):

        existing_subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription(
                db=db,
                organization_id=organization_id
            )
        )

        if existing_subscription:
            existing_subscription.status = "EXPIRED"

        start_date = datetime.utcnow()

        billing_cycle = billing_cycle.upper()

        if billing_cycle == "MONTHLY":
            end_date = (
                start_date +
                timedelta(days=30)
            )

        elif billing_cycle == "YEARLY":
            end_date = (
                start_date +
                timedelta(days=365)
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid billing cycle"
            )

        subscription = OrganizationSubscription(

            organization_id=organization_id,

            plan_id=plan_id,

            status="ACTIVE",

            start_date=start_date,

            end_date=end_date,

            is_trial=False
        )

        db.add(
            subscription
        )

        db.flush()

        db.refresh(
            subscription
        )

        return subscription