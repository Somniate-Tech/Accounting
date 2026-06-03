from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.subscriptions.subscription_payments.model import (
    SubscriptionPayment
)

from app.modules.subscriptions.subscription_payments.repository import (
    create_subscription_payment_repo,
    get_subscription_payment_by_id_repo,
    get_subscription_payments_repo,
    update_subscription_payment_repo
)

from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)


def create_subscription_payment_service(
    db: Session,
    organization_id: int,
    plan_id: int,
    billing_cycle: str
):

    plan = (
        db.query(SubscriptionPlan)
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

    if billing_cycle.upper() == "MONTHLY":
        amount = plan.monthly_price

    elif billing_cycle.upper() == "YEARLY":
        amount = plan.yearly_price

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid billing cycle"
        )

    payment = SubscriptionPayment(
        organization_id=organization_id,
        plan_id=plan_id,
        amount=amount,
        billing_cycle=billing_cycle.upper(),
        gateway="RAZORPAY",
        status="PENDING"
    )

    return create_subscription_payment_repo(
        db,
        payment
    )


def get_subscription_payment_service(
    db: Session,
    payment_id: int
):

    payment = get_subscription_payment_by_id_repo(
        db,
        payment_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


def get_subscription_payments_service(
    db: Session,
    organization_id: int
):
    return get_subscription_payments_repo(
        db,
        organization_id
    )


def mark_payment_success_service(
    db: Session,
    payment_id: int,
    payment_id_razorpay: str,
    order_id: str,
    signature: str
):

    payment = get_subscription_payment_by_id_repo(
        db,
        payment_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payment.payment_id = payment_id_razorpay
    payment.order_id = order_id
    payment.signature = signature
    payment.status = "SUCCESS"

    return update_subscription_payment_repo(
        db,
        payment
    )