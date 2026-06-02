from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.modules.vendors.schema import (
    VendorCreate,
    VendorUpdate
)

from app.modules.vendors.model import Vendor

from app.modules.vendors.repository import (
    create_vendor_repo,
    get_all_vendors_repo,
    get_vendor_by_code_repo,
    update_vendor_repo,
    delete_vendor_repo
)
from app.core.feature_guard import (
    FeatureGuard
)
from app.core.usage_guard import (
    UsageGuard
)

from app.core.constants import (
    FeatureCodes
)

def create_vendor_service(
    db: Session,
    vendor: VendorCreate,
    organization_id
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.VENDORS
    )
    current_vendor_count = (
        db.query(Vendor)
        .filter(
            Vendor.organization_id == organization_id
        )
        .count()
    )

    UsageGuard.check_limit(
        db=db,
        organization_id=organization_id,
        current_count=current_vendor_count,
        limit_field="max_vendors",
        resource_name="Vendor"
    )

    existing_email = (
        db.query(Vendor)
        .filter(
            Vendor.email == vendor.email,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return create_vendor_repo(
        db=db,
        vendor=vendor,
        organization_id=organization_id
    )


def get_all_vendors_service(
    db: Session,
    organization_id,
    page: int,
    limit: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.VENDORS
    )


    skip = (page - 1) * limit

    return get_all_vendors_repo(
        db=db,
        organization_id=organization_id,
        skip=skip,
        limit=limit
    )


def get_vendor_by_code_service(
    db: Session,
    vendor_code: str,
    organization_id,
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.VENDORS
    )


    vendor = get_vendor_by_code_repo(
        db=db,
        vendor_code=vendor_code,
        organization_id=organization_id
    )

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    return vendor


def update_vendor_service(
    db: Session,
    vendor_code: str,
    vendor_update: VendorUpdate,
    organization_id,
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.VENDORS
    )

    vendor = get_vendor_by_code_repo(
        db=db,
        vendor_code=vendor_code,
        organization_id=organization_id
    )

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    updated_vendor = update_vendor_repo(
        db=db,
        vendor_data=vendor,
        vendor_update=vendor_update
    )

    return updated_vendor


def delete_vendor_service(
    db: Session,
    vendor_code: str,
    organization_id
):
    
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.VENDORS
    )

    vendor = get_vendor_by_code_repo(
        db=db,
        vendor_code=vendor_code,
        organization_id=organization_id
    )

    if not vendor:

        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    delete_vendor_repo(
        db=db,
        vendor_data=vendor
    )

    return {
        "message": "Vendor deleted successfully"
    }