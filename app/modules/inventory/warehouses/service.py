from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.warehouses.model import (
    Warehouse
)

from app.modules.inventory.warehouses.schema import (
    WarehouseCreate,
    WarehouseUpdate
)

from app.modules.inventory.warehouses.repository import (
    create_warehouse_repo,
    get_all_warehouses_repo,
    get_warehouse_by_id_repo,
    get_warehouse_by_code_repo,
    update_warehouse_repo,
    delete_warehouse_repo
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

def create_warehouse_service(
    db: Session,
    warehouse: WarehouseCreate,
    organization_id: int
):
    
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.MULTI_WAREHOUSE
)

    existing_code = get_warehouse_by_code_repo(
        db,
        warehouse.code,
        organization_id
    )

    if existing_code:

        raise HTTPException(
            status_code=400,
            detail="Warehouse code already exists"
        )

    new_warehouse = Warehouse(
        organization_id=organization_id,

        name=warehouse.name,
        code=warehouse.code,

        address=warehouse.address
    )

    return create_warehouse_repo(
        db,
        new_warehouse
    )


def get_all_warehouses_service(
    db: Session,
    organization_id: int
):
    
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.MULTI_WAREHOUSE
)

    return get_all_warehouses_repo(
        db,
        organization_id
    )


def get_warehouse_by_id_service(
    db: Session,
    warehouse_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.MULTI_WAREHOUSE
)

    warehouse = get_warehouse_by_id_repo(
        db,
        warehouse_id,
        organization_id
    )

    if not warehouse:

        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    return warehouse


def update_warehouse_service(
    db: Session,
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.MULTI_WAREHOUSE
)

    warehouse = get_warehouse_by_id_repo(
        db,
        warehouse_id,
        organization_id
    )

    if not warehouse:

        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    if warehouse_data.code:

        existing_code = get_warehouse_by_code_repo(
            db,
            warehouse_data.code,
            organization_id
        )

        if existing_code and existing_code.id != warehouse.id:

            raise HTTPException(
                status_code=400,
                detail="Warehouse code already exists"
            )

    return update_warehouse_repo(
        db,
        warehouse,
        warehouse_data
    )


def delete_warehouse_service(
    db: Session,
    warehouse_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.MULTI_WAREHOUSE
)

    warehouse = get_warehouse_by_id_repo(
        db,
        warehouse_id,
        organization_id
    )

    if not warehouse:

        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )

    delete_warehouse_repo(
        db,
        warehouse
    )

    return {
        "message": "Warehouse deleted successfully"
    }