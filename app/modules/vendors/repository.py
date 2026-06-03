from sqlalchemy.orm import Session

from app.modules.vendors.model import Vendor

from app.modules.vendors.schema import (
    VendorCreate,
    VendorUpdate
)


def create_vendor_repo(
    db: Session,
    vendor: VendorCreate,
    organization_id
):

    last_vendor = (
        db.query(Vendor)
        .order_by(Vendor.created_at.desc())
        .first()
    )

    if last_vendor:

        last_number = int(
            last_vendor.vendor_code.replace("V", "")
        )

        new_vendor_code = f"V{last_number + 1}"

    else:

        new_vendor_code = "V1"

    new_vendor = Vendor(

        vendor_code=new_vendor_code,

        vendor_name=vendor.vendor_name,

        email=vendor.email,

        phone=vendor.phone,

        gst_number=vendor.gst_number,

        address=vendor.address,

        city=vendor.city,

        state=vendor.state,

        pincode=vendor.pincode,

        status=vendor.status,

        organization_id=organization_id
    )

    db.add(new_vendor)

    db.commit()

    db.refresh(new_vendor)

    return new_vendor


def update_vendor_repo(
    db: Session,
    vendor_data,
    vendor_update: VendorUpdate
):

    update_data = vendor_update.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(vendor_data, key, value)

    db.commit()

    db.refresh(vendor_data)

    return vendor_data


def get_all_vendors_repo(
    db: Session,
    organization_id,
    skip: int,
    limit: int
):

    return (
        db.query(Vendor)
        .filter(
            Vendor.organization_id == organization_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_vendor_by_code_repo(
    db: Session,
    vendor_code: str,
    organization_id: int
):

    return (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )


def delete_vendor_repo(
    db: Session,
    vendor_data
):

    db.delete(vendor_data)

    db.commit()

    return True