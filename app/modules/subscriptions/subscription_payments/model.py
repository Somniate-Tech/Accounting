from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class SubscriptionPayment(Base):
    __tablename__ = "subscription_payments"

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

    plan_id = Column(
        Integer,
        ForeignKey("subscription_plans.id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    billing_cycle = Column(
        String,
        nullable=False
    )

    gateway = Column(
        String,
        nullable=False,
        default="RAZORPAY"
    )

    order_id = Column(
        String,
        nullable=True
    )

    payment_id = Column(
        String,
        nullable=True
    )

    signature = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )

    paid_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )