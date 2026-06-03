from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Numeric,
    Integer,
    Text
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

import uuid
import enum

from datetime import datetime


class BillPaymentStatus(str, enum.Enum):
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class Bill(Base):
    __tablename__ = "bills"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    bill_code = Column(
        String,
        unique=True,
        nullable=False
    )

    vendor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vendors.id"),
        nullable=False
    )

    purchase_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id"),
        nullable=True
    )

    invoice_number = Column(
        String,
        nullable=False
    )

    invoice_date = Column(
        Date,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    payment_status = Column(
        Enum(BillPaymentStatus),
        default=BillPaymentStatus.UNPAID,
        nullable=False
    )

    subtotal = Column(
        Numeric(18, 2),
        default=0
    )

    tax_amount = Column(
        Numeric(18, 2),
        default=0
    )

    total_amount = Column(
        Numeric(18, 2),
        default=0
    )
    paid_amount = Column(
        Numeric(18, 2),
        default=0
    )
    due_amount = Column(
        Numeric(18, 2),
        default=0
    )
    organization_id = Column(
    Integer,
    ForeignKey("organizations.id"),
    nullable=False
    )

    notes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        backref="bills"
    )

    purchase_order = relationship(
        "PurchaseOrder",
        backref="bills"
    )

    items = relationship(
        "BillItem",
        back_populates="bill",
        cascade="all, delete"
    )


class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    bill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bills.id"),
        nullable=False
    )

    item_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Numeric(18, 2),
        nullable=False
    )

    tax_percent = Column(
        Numeric(5, 2),
        default=0
    )

    total = Column(
        Numeric(18, 2),
        nullable=False
    )

    bill = relationship(
        "Bill",
        back_populates="items"
    )