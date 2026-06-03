from fastapi import APIRouter
from fastapi import Depends, Query

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization,
    get_current_user
)

from app.modules.customer_payments.schema import (
    CustomerPaymentCreate,
    CustomerPaymentUpdate,
    CustomerPaymentResponse
)

from app.modules.customer_payments.service import (
    CustomerPaymentService,
)

router = APIRouter(
    prefix="/customer-payments",
    tags=["Customer Payments"]
)


@router.post(
    "/",
    response_model=CustomerPaymentResponse
)
def create_customer_payment(
    payment_data: CustomerPaymentCreate,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization),
    current_user=Depends(get_current_user)
):

    return CustomerPaymentService.create_payment(
        db=db,
        payment_data=payment_data,
        organization_id=organization,
        user_id=current_user.id
    )

@router.get("/")
def get_vendors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    vendors = CustomerPaymentService.get_all_payments(
        db=db,
        organization_id=organization_id,
        page=page,
        limit=limit
    )

    return {
        "page": page,
        "limit": limit,
        "data": vendors
    }

@router.get(
    "/{payment_id}",
    response_model=CustomerPaymentResponse
)
def get_single_customer_payment(
    payment_id: int,

    db: Session = Depends(get_db),

    organization=Depends(
        get_current_organization
    ),

    current_user=Depends(
        get_current_user
    )
):

    return CustomerPaymentService.get_single_payment(
        db=db,
        payment_id=payment_id,
        organization_id=organization
    )

@router.patch(
    "/{payment_id}",
    response_model=CustomerPaymentResponse
)
def update_customer_payment(
    payment_id: int,

    payment_data: CustomerPaymentUpdate,

    db: Session = Depends(get_db),

    organization=Depends(
        get_current_organization
    ),

    current_user=Depends(
        get_current_user
    )
):

    return CustomerPaymentService.update_payment(
        db=db,
        payment_id=payment_id,
        payment_data=payment_data,
        organization_id=organization
    )