from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.modules.customers.model import Customer

from app.modules.sales_orders.model import (
    SalesOrder
)

from app.modules.quotations.schema import (
    QuotationCreate,
    QuotationUpdate
)

from app.modules.quotations.repository import (
    create_quotation_repo,
    get_all_quotations_repo,
    get_total_quotations_count_repo,
    get_quotation_by_id_repo,
    update_quotation_repo,
    delete_quotation_repo
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

def create_quotation_service(
    db: Session,
    quotation: QuotationCreate,
    organization_id: int,
    user_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == quotation.customer_id,
            Customer.organization_id == organization_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return create_quotation_repo(
        db=db,
        quotation=quotation,
        organization_id=organization_id,
        user_id=user_id
    )


def get_all_quotations_service(
    db: Session,
    page: int,
    limit: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    skip = (page - 1) * limit

    quotations = get_all_quotations_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_quotations_count_repo(
        db=db,
        organization_id=organization_id
    )

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": quotations
    }


def get_single_quotation_service(
    db: Session,
    quotation_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    quotation = get_quotation_by_id_repo(
        db=db,
        quotation_id=quotation_id,
        organization_id=organization_id
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    return quotation


def update_quotation_service(
    db: Session,
    quotation_id: int,
    quotation_update: QuotationUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    quotation = get_quotation_by_id_repo(
        db=db,
        quotation_id=quotation_id,
        organization_id=organization_id
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    return update_quotation_repo(
        db=db,
        quotation=quotation,
        quotation_update=quotation_update
    )


def delete_quotation_service(
    db: Session,
    quotation_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    quotation = get_quotation_by_id_repo(
        db=db,
        quotation_id=quotation_id,
        organization_id=organization_id
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    existing_sales_order = (
        db.query(SalesOrder)
        .filter(
            SalesOrder.quotation_id == quotation.id,
            SalesOrder.organization_id == organization_id
        )
        .first()
    )

    if existing_sales_order:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete quotation. "
                "Sales Order already exists."
            )
        )

    delete_quotation_repo(
        db=db,
        quotation=quotation
    )

    return {
        "message": "Quotation deleted successfully"
    }