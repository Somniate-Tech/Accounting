from typing import List

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.subscriptions.subscription_payments.schema import (
    SubscriptionPaymentCreate,
    SubscriptionPaymentResponse,
    VerifyPaymentRequest
)

from app.modules.subscriptions.subscription_payments.service import (
    create_subscription_payment_service,
    get_subscription_payment_service,
    get_subscription_payments_service,
    create_razorpay_order_service,
    verify_razorpay_payment_service,
)

router = APIRouter(
    prefix="/subscription-payments",
    tags=["Subscription Payments"]
)


@router.post(
    "/",
    response_model=SubscriptionPaymentResponse
)
def create_subscription_payment(
    payment: SubscriptionPaymentCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(
        get_current_organization
    )
):
    return create_subscription_payment_service(
        db=db,
        organization_id=organization_id,
        plan_id=payment.plan_id,
        billing_cycle=payment.billing_cycle
    )

@router.post(
    "/create-order"
)
def create_razorpay_order(
        payment: SubscriptionPaymentCreate,
        db: Session = Depends(get_db),
        organization_id: int = Depends(
            get_current_organization
        )
    
):

    return create_razorpay_order_service(
        db=db,
        organization_id=organization_id,
        plan_id=payment.plan_id,
        billing_cycle=payment.billing_cycle
    )

@router.post(
    "/verify-payment"
)
def verify_payment(

        payload: VerifyPaymentRequest,

        db: Session = Depends(
            get_db
        ),
        organization_id=Depends(get_current_organization)

):

    return (
        verify_razorpay_payment_service(

            db=db,
            organization_id=organization_id,

            payment_id=payload.payment_id,

            razorpay_payment_id=payload.razorpay_payment_id,

            razorpay_order_id=payload.razorpay_order_id,

            razorpay_signature=payload.razorpay_signature

        )
    )

@router.get(
    "/",
    response_model=List[SubscriptionPaymentResponse]
)
def get_subscription_payments(
    db: Session = Depends(get_db),
    organization_id: int = Depends(
        get_current_organization
    )
):
    return get_subscription_payments_service(
        db,
        organization_id
    )


@router.get(
    "/{payment_id}",
    response_model=SubscriptionPaymentResponse
)
def get_subscription_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    organization_id=Depends(get_current_organization)
):  
    return get_subscription_payment_service(
        db,
        payment_id
    )