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
from app.core.razorpay_client import razorpay_client
from app.core.config import settings
from datetime import datetime
from razorpay.errors import SignatureVerificationError
from app.modules.subscriptions.organization_subscriptions.service import (
    OrganizationSubscriptionService
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


def create_razorpay_order_service(
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

    billing_cycle = billing_cycle.upper()

    if billing_cycle == "MONTHLY":
        amount = plan.monthly_price

    elif billing_cycle == "YEARLY":
        amount = plan.yearly_price

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid billing cycle"
        )

    amount_in_paise = int(amount * 100)

    razorpay_order = razorpay_client.order.create(
        {
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        }
    )

    payment = SubscriptionPayment(
        organization_id=organization_id,
        plan_id=plan_id,
        amount=amount,
        billing_cycle=billing_cycle,
        gateway="RAZORPAY",
        order_id=razorpay_order["id"],
        status="PENDING"
    )

    payment = create_subscription_payment_repo(
        db,
        payment
    )

    return {
        "payment_id": payment.id,
        "order_id": razorpay_order["id"],
        "amount": amount_in_paise,
        "currency": "INR",
        "key_id": settings.RAZORPAY_KEY_ID
    }


def verify_razorpay_payment_service(
        db: Session,
        organization_id:int,
        payment_id: int,
        razorpay_payment_id: str,
        razorpay_order_id: str,
        razorpay_signature: str
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
    
    if payment.organization_id != organization_id:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )
    

    if payment.status == "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Payment already processed"
        )

    try:

        razorpay_client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            }
        )

    except SignatureVerificationError:

        raise HTTPException(
            status_code=400,
            detail="Invalid payment signature"
        )
    
    if payment.order_id != razorpay_order_id:
        raise HTTPException(
            status_code=400,
            detail="Order ID mismatch"
        )
    
    try:
        payment_details = (
            razorpay_client.payment.fetch(
                razorpay_payment_id
            )
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to fetch payment details"
        )

    amount_received = (
        payment_details["amount"] / 100
    )

    if float(payment.amount) != amount_received:
        raise HTTPException(
            status_code=400,
            detail="Amount mismatch"
        )

    payment.payment_id = razorpay_payment_id

    payment.order_id = razorpay_order_id

    payment.signature = razorpay_signature

    payment.status = "SUCCESS"

    payment.paid_at = datetime.utcnow()


    try:
        subscription = (
            OrganizationSubscriptionService
            .activate_paid_subscription(
                db=db,
                organization_id=payment.organization_id,
                plan_id=payment.plan_id,
                billing_cycle=payment.billing_cycle
            )
        )
    except Exception:
        db.rollback()
        raise

    db.refresh(payment)

    return {

        "message":
        "Payment verified successfully",

        "payment_id":
        payment.id,

        "subscription_id":
        subscription.id
    }