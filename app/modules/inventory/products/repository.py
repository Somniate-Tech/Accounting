from sqlalchemy.orm import Session

from app.modules.inventory.products.model import Product

from app.modules.inventory.products.schema import (
    ProductUpdate
)


def create_product_repo(
    db: Session,
    product: Product
):

    db.add(product)

    db.commit()

    db.refresh(product)

    return product


def get_all_products_repo(
    db: Session,
    organization_id: int
):

    return db.query(Product).filter(
        Product.organization_id == organization_id,
        Product.is_active == True
    ).all()


def get_product_by_id_repo(
    db: Session,
    product_id: int,
    organization_id: int
):

    return db.query(Product).filter(
        Product.id == product_id,
        Product.organization_id == organization_id,
        Product.is_active == True
    ).first()


def get_product_by_sku_repo(
    db: Session,
    sku: str,
    organization_id: int
):

    return db.query(Product).filter(
        Product.sku == sku,
        Product.organization_id == organization_id
    ).first()


def get_last_product_repo(
    db: Session
):

    return db.query(Product).order_by(
        Product.id.desc()
    ).first()


def update_product_repo(
    db: Session,
    product_obj: Product,
    product_data: ProductUpdate
):

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(product_obj, key, value)

    db.commit()

    db.refresh(product_obj)

    return product_obj


def delete_product_repo(
    db: Session,
    product_obj: Product
):

    product_obj.is_active = False

    db.commit()

    db.refresh(product_obj)

    return product_obj