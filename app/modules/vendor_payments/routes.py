from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization,
    get_current_user
)

from app.modules.vendor_payments.schema import (
    VendorPaymentCreate,
    VendorPaymentUpdate,
    VendorPaymentResponse
)

from app.modules.vendor_payments.service import (
    VendorPaymentService
)
from fastapi import Query

router = APIRouter(
    prefix="/vendor-payments",
    tags=["Vendor Payments"]
)


@router.post(
    "/",
    response_model=VendorPaymentResponse
)
def create_vendor_payment(
    payment_data: VendorPaymentCreate,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization),
    current_user=Depends(get_current_user)
):

    return VendorPaymentService.create_payment(
        db=db,
        payment_data=payment_data,
        organization_id=organization,
        user_id=current_user.id
    )

@router.get(
    "/",
    response_model=list[VendorPaymentResponse]
)
def get_all_vendor_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),

    db: Session = Depends(get_db),

    organization=Depends(
        get_current_organization
    ),

    current_user=Depends(
        get_current_user
    )
):

    return VendorPaymentService.get_all_payments(
        db=db,
        organization_id=organization,
        page=page,
        limit=limit
    )

@router.get(
    "/{payment_id}",
    response_model=VendorPaymentResponse
)
def get_single_vendor_payment(
    payment_id: int,

    db: Session = Depends(get_db),

    organization=Depends(
        get_current_organization
    ),

    current_user=Depends(
        get_current_user
    )
):

    return VendorPaymentService.get_single_payment(
        db=db,
        payment_id=payment_id,
        organization_id=organization
    )


@router.patch(
    "/{payment_id}",
    response_model=VendorPaymentResponse
)
def update_vendor_payment(
    payment_id: int,

    payment_data: VendorPaymentUpdate,

    db: Session = Depends(get_db),

    organization=Depends(
        get_current_organization
    ),

    current_user=Depends(
        get_current_user
    )
):

    return VendorPaymentService.update_payment(
        db=db,
        payment_id=payment_id,
        payment_data=payment_data,
        organization_id=organization
    )