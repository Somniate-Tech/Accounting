from fastapi import HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from app.modules.inventory.stock_transactions.model import (
    StockTransaction
)

from app.modules.inventory.stock_transactions.schema import (
    StockTransactionCreate
)

from app.modules.inventory.stock_transactions.repository import (
    create_stock_transaction_repo,
    get_all_stock_transactions_repo,
    get_product_stock_transactions_repo
)

from app.modules.inventory.products.model import Product

from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)


def create_stock_transaction_service(
    db: Session,
    transaction: StockTransactionCreate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    product = (
        db.query(Product)
        .filter(
            Product.id == transaction.product_id,
            Product.organization_id == organization_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Warehouse Validation
    if (
        transaction.warehouse_id is not None
        and
        transaction.warehouse_id != product.warehouse_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Product does not belong to the selected warehouse"
        )

    before_stock = Decimal(str(product.current_stock))

    transaction_type = (
        transaction.transaction_type.upper().strip()
    )

    if transaction_type in [
        "OPENING",
        "PURCHASE",
        "RETURN",
        "ADJUSTMENT_IN"
    ]:

        after_stock = (
            before_stock +
            transaction.quantity
        )

    elif transaction_type in [
        "SALE",
        "DAMAGE",
        "ADJUSTMENT_OUT"
    ]:

        after_stock = (
            before_stock -
            transaction.quantity
        )

        if after_stock < 0:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction type"
        )

    product.current_stock = after_stock

    stock_transaction = StockTransaction(
        organization_id=organization_id,

        product_id=transaction.product_id,

        warehouse_id=(
            transaction.warehouse_id
            if transaction.warehouse_id is not None
            else product.warehouse_id
        ),

        transaction_type=transaction_type,

        quantity=transaction.quantity,

        before_stock=before_stock,

        after_stock=after_stock,

        reference_type=transaction.reference_type,

        reference_id=transaction.reference_id,

        remarks=transaction.remarks
    )

    db.add(stock_transaction)

    db.commit()

    db.refresh(stock_transaction)

    return stock_transaction


def get_all_stock_transactions_service(
    db: Session,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    return get_all_stock_transactions_repo(
        db,
        organization_id
    )


def get_product_stock_transactions_service(
    db: Session,
    product_id: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.INVENTORY
    )

    return get_product_stock_transactions_repo(
        db,
        product_id,
        organization_id
    )