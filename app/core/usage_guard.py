from fastapi import HTTPException

from app.modules.subscriptions.organization_subscriptions.repository import (
    OrganizationSubscriptionRepository
)

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)


class UsageGuard:

    @staticmethod
    def check_limit(
        db,
        organization_id: int,
        current_count: int,
        limit_field: str,
        resource_name: str
    ):

        subscription = (
            OrganizationSubscriptionRepository
            .get_active_subscription_by_organization(
                db=db,
                organization_id=organization_id
            )
        )

        if not subscription:

            raise HTTPException(
                status_code=403,
                detail="No active subscription found"
            )

        plan = (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.id == subscription.plan_id
            )
            .first()
        )

        if not plan:

            raise HTTPException(
                status_code=403,
                detail="Subscription plan not found"
            )

        allowed_limit = getattr(
            plan,
            limit_field,
            0
        )

        # Unlimited
        if allowed_limit == -1:

            return True

        if current_count >= allowed_limit:

            raise HTTPException(
                status_code=403,
                detail=(
                    f"{resource_name} limit reached. "
                    "Please upgrade your plan."
                )
            )

        return True