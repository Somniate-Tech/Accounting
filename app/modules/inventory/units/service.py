from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.units.model import Unit

from app.modules.inventory.units.schema import (
    UnitCreate,
    UnitUpdate
)
from app.core.feature_guard import (
    FeatureGuard
)
from app.core.constants import (
    FeatureCodes
)

from app.modules.inventory.units.repository import (
    create_unit_repo,
    get_all_units_repo,
    get_unit_by_id_repo,
    update_unit_repo,
    delete_unit_repo
)


def create_unit_service(
    db: Session,
    unit: UnitCreate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    existing_unit = db.query(Unit).filter(
        Unit.name == unit.name,
        Unit.organization_id == organization_id
    ).first()

    if existing_unit:

        raise HTTPException(
            status_code=400,
            detail="Unit already exists"
        )

    new_unit = Unit(
        organization_id=organization_id,
        name=unit.name,
        short_name=unit.short_name
    )

    return create_unit_repo(
        db,
        new_unit
    )


def get_all_units_service(
    db: Session,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    return get_all_units_repo(
        db,
        organization_id
    )


def get_unit_by_id_service(
    db: Session,
    unit_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    unit = get_unit_by_id_repo(
        db,
        unit_id,
        organization_id
    )

    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

    return unit


def update_unit_service(
    db: Session,
    unit_id: int,
    unit_data: UnitUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    unit = get_unit_by_id_repo(
        db,
        unit_id,
        organization_id
    )

    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

    return update_unit_repo(
        db,
        unit,
        unit_data
    )


def delete_unit_service(
    db: Session,
    unit_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )


    unit = get_unit_by_id_repo(
        db,
        unit_id,
        organization_id
    )

    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

    delete_unit_repo(
        db,
        unit
    )

    return {
        "message": "Unit deleted successfully"
    }