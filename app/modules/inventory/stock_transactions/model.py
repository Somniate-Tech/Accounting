from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Text,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=True
    )

    transaction_type = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Numeric(10, 2),
        nullable=False
    )

    before_stock = Column(
        Numeric(10, 2),
        nullable=False
    )

    after_stock = Column(
        Numeric(10, 2),
        nullable=False
    )

    reference_type = Column(
        String,
        nullable=True
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    remarks = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
