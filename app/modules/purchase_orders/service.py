from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.modules.purchase_orders.schema import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
)

from app.modules.purchase_orders.repository import (
    create_purchase_order_repo,
    get_all_purchase_orders_repo,
    get_total_purchase_orders_count_repo,
    delete_purchase_order_repo,
    get_purchase_order_by_code_repo,
    update_purchase_order_repo,
)

from app.modules.vendors.model import Vendor
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

def create_purchase_order_service(
    db: Session,
    purchase_order: PurchaseOrderCreate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == purchase_order.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    return create_purchase_order_repo(
        db=db,
        purchase_order=purchase_order,
        organization_id=organization_id
    )


def get_all_purchase_orders_service(
    db: Session,
    page: int,
    limit: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )

    skip = (page - 1) * limit

    purchase_orders = get_all_purchase_orders_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_purchase_orders_count_repo(
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
        "data": purchase_orders
    }


def delete_purchase_order_service(
    db: Session,
    po_code: str,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    purchase_order = get_purchase_order_by_code_repo(
        db=db,
        po_code=po_code,
        organization_id=organization_id
    )

    if not purchase_order:
        raise HTTPException(
            status_code=404,
            detail="Purchase Order not found"
        )

    delete_purchase_order_repo(
        db=db,
        purchase_order=purchase_order
    )

    return {
        "message": "Purchase Order deleted successfully"
    }


def update_purchase_order_service(
    db: Session,
    po_code: str,
    purchase_order_update: PurchaseOrderUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    purchase_order = get_purchase_order_by_code_repo(
        db=db,
        po_code=po_code,
        organization_id=organization_id
    )

    if not purchase_order:
        raise HTTPException(
            status_code=404,
            detail="Purchase Order not found"
        )

    return update_purchase_order_repo(
        db=db,
        purchase_order=purchase_order,
        purchase_order_update=purchase_order_update,
        organization_id=organization_id
    )