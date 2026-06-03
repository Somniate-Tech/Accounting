from sqlalchemy.orm import Session

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)

from app.modules.subscriptions.plans.schema import (
    SubscriptionPlanCreate,
    SubscriptionPlanUpdate
)


class SubscriptionPlanRepository:

    @staticmethod
    def create(
        db: Session,
        payload: SubscriptionPlanCreate
    ):

        plan = SubscriptionPlan(
            name=payload.name,
            code=payload.code,
            description=payload.description,

            monthly_price=payload.monthly_price,
            yearly_price=payload.yearly_price,

            max_users=payload.max_users,
            max_customers=payload.max_customers,
            max_vendors=payload.max_vendors,
            max_products=payload.max_products
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def get_all(
        db: Session
    ):

        return (
            db.query(SubscriptionPlan)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        plan_id: int
    ):

        return (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.id == plan_id
            )
            .first()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        code: str
    ):

        return (
            db.query(SubscriptionPlan)
            .filter(
                SubscriptionPlan.code == code
            )
            .first()
        )
    



    @staticmethod
    def update(
        db: Session,
        plan: SubscriptionPlan,
        payload: SubscriptionPlanUpdate
    ):

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():

            setattr(
                plan,
                field,
                value
            )

        db.commit()

        db.refresh(plan)

        return plan


    @staticmethod
    def activate(
        db: Session,
        plan: SubscriptionPlan
    ):

        plan.is_active = True

        db.commit()

        db.refresh(plan)

        return plan


    @staticmethod
    def deactivate(
        db: Session,
        plan: SubscriptionPlan
    ):

        plan.is_active = False

        db.commit()

        db.refresh(plan)

        return plan