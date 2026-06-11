from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.core.database import Base

from sqlalchemy.dialects.postgresql import UUID
class VendorPayment(Base):
    __tablename__ = "vendor_payments"

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

    vendor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vendors.id"),
        nullable=False
    )

    bill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bills.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    reference_number = Column(
        String,
        nullable=True
    )

    notes = Column(
        String,
        nullable=True
    )

    payment_date = Column(
        DateTime,
        nullable=False
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    vendor = relationship("Vendor")

    bill = relationship("Bill")