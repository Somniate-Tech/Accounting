from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.modules.customers.model import Customer

from app.modules.customers.schema import (
    CustomerCreate,
    CustomerUpdate
)

from app.modules.customers.repository import (
    create_customer_repo,
    get_all_customers_repo,
    get_single_customer_repo,
    update_customer_repo,
    delete_customer_repo
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)
from app.core.usage_guard import (
    UsageGuard
)

def create_customer_service(
    db: Session,
    customer: CustomerCreate,
    organization_id: int,
    user_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.CUSTOMERS
    )
    current_customer_count = (
        db.query(Customer)
        .filter(
            Customer.organization_id == organization_id
        )
    .count()
    )

    UsageGuard.check_limit(
        db=db,
        organization_id=organization_id,
        current_count=current_customer_count,
        limit_field="max_customers",
        resource_name="Customer"
    )
        
    # Duplicate email validation
    if customer.email:
        existing_email = db.query(Customer).filter(
            Customer.email == customer.email,
            Customer.organization_id == organization_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer email already exists"
            )

    # Duplicate GST validation
    if customer.gst_number:
        existing_gst = db.query(Customer).filter(
            Customer.gst_number == customer.gst_number,
            Customer.organization_id == organization_id
        ).first()

        if existing_gst:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="GST number already exists"
            )

    return create_customer_repo(
        db,
        customer,
        organization_id,
        user_id
    )


def get_all_customers_service(
    db: Session,
    organization_id: int,
    page: int,
    limit: int,
    search: str = None
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.CUSTOMERS
    )
    return get_all_customers_repo(
        db,
        organization_id,
        page,
        limit,
        search
    )


def get_single_customer_service(
    db: Session,
    customer_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.CUSTOMERS
    )
    customer = get_single_customer_repo(
        db,
        customer_id,
        organization_id
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return customer


def update_customer_service(
    db: Session,
    customer_id: int,
    customer: CustomerUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.CUSTOMERS
    )
    existing_customer = get_single_customer_repo(
        db,
        customer_id,
        organization_id
    )

    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return update_customer_repo(
        db,
        existing_customer,
        customer
    )


def delete_customer_service(
    db: Session,
    customer_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.CUSTOMERS
    )
    customer = get_single_customer_repo(
        db,
        customer_id,
        organization_id
    )

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    delete_customer_repo(
        db,
        customer
    )

    return {
        "message": "Customer deleted successfully"
    }