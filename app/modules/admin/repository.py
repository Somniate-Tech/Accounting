from sqlalchemy.orm import Session

from app.modules.users.model import User

from app.modules.organizations.model import (
    Organization
)

from app.modules.subscriptions.organization_subscriptions.model import (
    OrganizationSubscription
)
from app.modules.organizations.model import (
    Organization
)
from datetime import datetime
from datetime import timedelta

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)

class AdminRepository:

    @staticmethod
    def get_dashboard_stats(
        db: Session
    ):

        total_users = (
            db.query(User)
            .count()
        )

        total_organizations = (
            db.query(Organization)
            .count()
        )

        active_subscriptions = (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.status == "ACTIVE"
            )
            .count()
        )

        trial_subscriptions = (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.is_trial == True
            )
            .count()
        )

        expired_subscriptions = (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.status == "EXPIRED"
            )
            .count()
        )

        return {
            "total_users": total_users,
            "total_organizations": total_organizations,
            "active_subscriptions": active_subscriptions,
            "trial_subscriptions": trial_subscriptions,
            "expired_subscriptions": expired_subscriptions
        }
    

    @staticmethod
    def get_all_organizations(
        db: Session
    ):

        return (
            db.query(
                Organization
            )
            .order_by(
                Organization.id.desc()
            )
            .all()
        )
    

    @staticmethod
    def get_all_users(
        db: Session
    ):

        return (
            db.query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )
    

    @staticmethod
    def get_all_subscriptions(
        db: Session
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .order_by(
                OrganizationSubscription.id.desc()
            )
            .all()
        )
    
    @staticmethod
    def get_organization_by_id(
        db: Session,
        organization_id: int
    ):

        return (
            db.query(Organization)
            .filter(
                Organization.id == organization_id
            )
            .first()
        )
    
    @staticmethod
    def get_expired_subscriptions(
        db: Session
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.status
                == "EXPIRED"
            )
            .all()
        )
    
    @staticmethod
    def get_trial_subscriptions(
        db: Session
    ):

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.is_trial == True
            )
            .all()
        )
    
    @staticmethod
    def get_expiring_subscriptions(
        db: Session
    ):

        today = datetime.utcnow()

        next_week = today + timedelta(days=7)

        return (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.end_date >= today,
                OrganizationSubscription.end_date <= next_week,
                OrganizationSubscription.status == "ACTIVE"
            )
            .all()
        )
    
    @staticmethod
    def get_revenue_dashboard(
        db: Session
    ):

        active_subscriptions = (
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.status == "ACTIVE"
            )
            .all()
        )

        monthly_revenue = 0
        yearly_revenue = 0

        for subscription in active_subscriptions:

            plan = (
                db.query(
                    SubscriptionPlan
                )
                .filter(
                    SubscriptionPlan.id ==
                    subscription.plan_id
                )
                .first()
            )

            if plan:

                monthly_revenue += (
                    plan.monthly_price or 0
                )

                yearly_revenue += (
                    plan.yearly_price or 0
                )

        return {

            "active_subscriptions":
            len(active_subscriptions),

            "trial_subscriptions":
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.is_trial == True
            )
            .count(),

            "expired_subscriptions":
            db.query(
                OrganizationSubscription
            )
            .filter(
                OrganizationSubscription.status ==
                "EXPIRED"
            )
            .count(),

            "monthly_revenue":
            monthly_revenue,

            "yearly_revenue":
            yearly_revenue
        }