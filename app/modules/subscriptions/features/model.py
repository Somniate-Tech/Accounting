from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from app.core.database import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    code = Column(
        String,
        unique=True,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )
