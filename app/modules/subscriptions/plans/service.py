from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.subscriptions.plans.repository import (
    SubscriptionPlanRepository
)

from app.modules.subscriptions.plans.schema import (
    SubscriptionPlanCreate
)
from app.modules.subscriptions.plans.schema import (
    SubscriptionPlanUpdate
)


class SubscriptionPlanService:

    @staticmethod
    def create_plan(
        db: Session,
        payload: SubscriptionPlanCreate
    ):

        existing_plan = (
            SubscriptionPlanRepository.get_by_code(
                db=db,
                code=payload.code
            )
        )

        if existing_plan:
            raise HTTPException(
                status_code=400,
                detail="Plan code already exists"
            )

        return (
            SubscriptionPlanRepository.create(
                db=db,
                payload=payload
            )
        )

    @staticmethod
    def get_all_plans(
        db: Session
    ):

        return (
            SubscriptionPlanRepository.get_all(
                db=db
            )
        )

    @staticmethod
    def get_plan_by_id(
        db: Session,
        plan_id: int
    ):

        plan = (
            SubscriptionPlanRepository.get_by_id(
                db=db,
                plan_id=plan_id
            )
        )

        if not plan:
            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        return plan
    


    @staticmethod
    def update_plan(
        db: Session,
        plan_id: int,
        payload: SubscriptionPlanUpdate
    ):

        plan = (
            SubscriptionPlanRepository.get_by_id(
                db=db,
                plan_id=plan_id
            )
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        return (
            SubscriptionPlanRepository.update(
                db=db,
                plan=plan,
                payload=payload
            )
        )


    @staticmethod
    def activate_plan(
        db: Session,
        plan_id: int
    ):

        plan = (
            SubscriptionPlanRepository.get_by_id(
                db=db,
                plan_id=plan_id
            )
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        return (
            SubscriptionPlanRepository.activate(
                db=db,
                plan=plan
            )
        )


    @staticmethod
    def deactivate_plan(
        db: Session,
        plan_id: int
    ):

        plan = (
            SubscriptionPlanRepository.get_by_id(
                db=db,
                plan_id=plan_id
            )
        )

        if not plan:

            raise HTTPException(
                status_code=404,
                detail="Plan not found"
            )

        return (
            SubscriptionPlanRepository.deactivate(
                db=db,
                plan=plan
            )
        )