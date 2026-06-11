from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Text,
    Boolean
)

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

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

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    unit_id = Column(
        Integer,
        ForeignKey("units.id"),
        nullable=False
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )
    
    name = Column(
        String,
        nullable=False
    )

    sku = Column(
        String,
        nullable=True,
        unique=True
    )

    barcode = Column(
        String,
        nullable=True
    )

    purchase_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    selling_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    gst_percent = Column(
        Numeric(5, 2),
        nullable=False,
        default=0
    )

    opening_stock = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    current_stock = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    minimum_stock = Column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    description = Column(
        Text,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )