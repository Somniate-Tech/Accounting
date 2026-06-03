from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.modules.subscriptions.organization_subscriptions.repository import (
    OrganizationSubscriptionRepository
)

from app.modules.subscriptions.plan_features.repository import (
    PlanFeatureRepository
)

from app.modules.subscriptions.features.repository import (
    FeatureRepository
)


class FeatureGuard:

    @staticmethod
    def check_feature_access(
        db: Session,
        organization_id: int,
        feature_code: str
    ) -> bool:

        # Get active subscription
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
        
        # Check subscription expiry

        current_time = datetime.now(timezone.utc)

        subscription_end = subscription.end_date

        if subscription_end.tzinfo is None:
            subscription_end = subscription_end.replace(
                tzinfo=timezone.utc
            )

        if subscription_end <= current_time:

            subscription.status = "EXPIRED"
            db.add(subscription)

            db.commit()
            db.refresh(subscription)

            raise HTTPException(
                status_code=403,
                detail=(
                    "Your subscription has expired. "
                    "Please renew or upgrade your plan."
                )
            )

        # Get feature by code
        feature = FeatureRepository.get_by_code(
            db=db,
            code=feature_code
        )

        if not feature:
            raise HTTPException(
                status_code=404,
                detail=f"Feature '{feature_code}' not found"
            )

        # Get all plan features
        plan_features = (
            PlanFeatureRepository
            .get_by_plan(
                db=db,
                plan_id=subscription.plan_id
            )
        )

        # Check access
        has_access = any(
            pf.feature_id == feature.id
            for pf in plan_features
        )

        if not has_access:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"Feature '{feature_code}' is not available "
                    f"in your current subscription plan. "
                    f"Please upgrade your plan."
                )
            )

        return True