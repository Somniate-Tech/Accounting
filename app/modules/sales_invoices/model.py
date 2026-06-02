from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

import enum

from app.core.database import Base


class InvoiceStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class SalesInvoice(Base):
    __tablename__ = "sales_invoices"

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

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    sales_order_id = Column(
        Integer,
        ForeignKey("sales_orders.id"),
        nullable=True
    )

    invoice_number = Column(
        String,
        unique=True,
        nullable=False
    )

    status = Column(
        Enum(InvoiceStatus),
        default=InvoiceStatus.DRAFT
    )

    subtotal = Column(
        Float,
        default=0
    )

    tax_amount = Column(
        Float,
        default=0
    )

    total_amount = Column(
        Float,
        default=0
    )

    paid_amount = Column(
        Float,
        default=0
    )

    due_amount = Column(
        Float,
        default=0
    )

    notes = Column(
        String,
        nullable=True
    )

    due_date = Column(
        DateTime,
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    customer = relationship("Customer")

    sales_order = relationship("SalesOrder")

    items = relationship(
        "SalesInvoiceItem",
        back_populates="invoice",
        cascade="all, delete"
    )


class SalesInvoiceItem(Base):
    __tablename__ = "sales_invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("sales_invoices.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=True
    )

    item_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    tax_percent = Column(
        Float,
        default=0
    )

    total = Column(
        Float,
        nullable=False
    )

    invoice = relationship(
        "SalesInvoice",
        back_populates="items"
    )

    product = relationship(
        "Product"
    )