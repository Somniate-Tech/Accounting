from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.modules.customers.model import (
    Customer
)

from app.modules.quotations.model import (
    Quotation
)

from app.modules.sales_invoices.model import (
    SalesInvoice
)

from app.modules.sales_orders.schema import (
    SalesOrderCreate,
    SalesOrderUpdate
)

from app.modules.sales_orders.repository import (
    create_sales_order_repo,
    get_all_sales_orders_repo,
    get_total_sales_orders_count_repo,
    get_sales_order_by_id_repo,
    update_sales_order_repo,
    delete_sales_order_repo
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)


def create_sales_order_service(
    db: Session,
    sales_order: SalesOrderCreate,
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
            Customer.id == sales_order.customer_id,
            Customer.organization_id == organization_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if sales_order.quotation_id:

        quotation = (
            db.query(Quotation)
            .filter(
                Quotation.id == sales_order.quotation_id,
                Quotation.organization_id == organization_id
            )
            .first()
        )

        if not quotation:
            raise HTTPException(
                status_code=404,
                detail="Quotation not found"
            )

    return create_sales_order_repo(
        db=db,
        sales_order=sales_order,
        organization_id=organization_id,
        user_id=user_id
    )


def get_all_sales_orders_service(
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

    sales_orders = get_all_sales_orders_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_sales_orders_count_repo(
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
        "data": sales_orders
    }


def get_single_sales_order_service(
    db: Session,
    sales_order_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    sales_order = get_sales_order_by_id_repo(
        db=db,
        sales_order_id=sales_order_id,
        organization_id=organization_id
    )

    if not sales_order:
        raise HTTPException(
            status_code=404,
            detail="Sales Order not found"
        )

    return sales_order


def update_sales_order_service(
    db: Session,
    sales_order_id: int,
    sales_order_update: SalesOrderUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    sales_order = get_sales_order_by_id_repo(
        db=db,
        sales_order_id=sales_order_id,
        organization_id=organization_id
    )

    if not sales_order:
        raise HTTPException(
            status_code=404,
            detail="Sales Order not found"
        )

    return update_sales_order_repo(
        db=db,
        sales_order=sales_order,
        sales_order_update=sales_order_update
    )


def delete_sales_order_service(
    db: Session,
    sales_order_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.SALES
    )
    sales_order = get_sales_order_by_id_repo(
        db=db,
        sales_order_id=sales_order_id,
        organization_id=organization_id
    )

    if not sales_order:
        raise HTTPException(
            status_code=404,
            detail="Sales Order not found"
        )

    existing_invoice = (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.sales_order_id == sales_order.id
        )
        .first()
    )

    if existing_invoice:
        raise HTTPException(
            status_code=400,
            detail=(
                "Cannot delete Sales Order. "
                "Invoice already exists."
            )
        )

    delete_sales_order_repo(
        db=db,
        sales_order=sales_order
    )

    return {
        "message": "Sales Order deleted successfully"
    }