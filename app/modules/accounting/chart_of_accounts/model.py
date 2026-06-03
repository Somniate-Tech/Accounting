from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class ChartOfAccount(Base):
    __tablename__ = "chart_of_accounts"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )

    account_code = Column(
        String,
        nullable=False
    )

    account_name = Column(
        String,
        nullable=False
    )

    account_type = Column(
        String,
        nullable=False
    )

    parent_account_id = Column(
        Integer,
        ForeignKey("chart_of_accounts.id"),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    parent_account = relationship(
        "ChartOfAccount",
        remote_side=[id]
    )