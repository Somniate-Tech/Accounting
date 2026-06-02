from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.core.database import Base


class OrganizationSubscription(Base):
    __tablename__ = "organization_subscriptions"

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

    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    start_date = Column(
        DateTime(timezone=True),
        nullable=False
    )

    end_date = Column(
        DateTime(timezone=True),
        nullable=False
    )

    is_trial = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )