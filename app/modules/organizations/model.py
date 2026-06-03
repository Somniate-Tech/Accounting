from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)

from sqlalchemy.sql import func

from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    photo = Column(String, nullable=True)
    
    organization_name = Column(
        String,
        nullable=False
    )

    organization_type = Column(
        String,
        nullable=False
    )

    gst_number = Column(
        String,
        nullable=True
    )

    phone = Column(
        String,
        nullable=True
    )

    address = Column(
        String,
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    is_active = Column(
    Boolean,
    nullable=False,
    default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )