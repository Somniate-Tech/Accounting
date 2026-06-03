from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.categories.model import Category

from app.modules.inventory.categories.schema import (
    CategoryCreate,
    CategoryUpdate
)
from app.core.feature_guard import (
    FeatureGuard
)
from app.core.constants import (
    FeatureCodes
)

from app.modules.inventory.categories.repository import (
    create_category_repo,
    get_all_categories_repo,
    get_category_by_id_repo,
    update_category_repo,
    delete_category_repo
)


def create_category_service(
    db: Session,
    category: CategoryCreate,
    organization_id: int
):
    
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    existing_category = db.query(Category).filter(
        Category.name == category.name,
        Category.organization_id == organization_id
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    new_category = Category(
        organization_id=organization_id,
        name=category.name,
        description=category.description
    )

    return create_category_repo(
        db,
        new_category
    )


def get_all_categories_service(
    db: Session,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )
    return get_all_categories_repo(
        db,
        organization_id
    )


def get_category_by_id_service(
    db: Session,
    category_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    category = get_category_by_id_repo(
        db,
        category_id,
        organization_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def update_category_service(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    category = get_category_by_id_repo(
        db,
        category_id,
        organization_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return update_category_repo(
        db,
        category,
        category_data
    )


def delete_category_service(
    db: Session,
    category_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    category = get_category_by_id_repo(
        db,
        category_id,
        organization_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    delete_category_repo(
        db,
        category
    )

    return {
        "message": "Category deleted successfully"
    }