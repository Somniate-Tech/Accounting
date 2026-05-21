from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.core.database import Base


class JournalEntry(Base):

    __tablename__ = "journal_entries"

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

    reference_type = Column(
        String,
        nullable=True
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    description = Column(
        String,
        nullable=True
    )

    entry_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    lines = relationship(
        "JournalEntryLine",
        back_populates="journal_entry",
        cascade="all, delete-orphan"
    )


class JournalEntryLine(Base):

    __tablename__ = "journal_entry_lines"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    journal_entry_id = Column(
        Integer,
        ForeignKey("journal_entries.id"),
        nullable=False
    )

    account_id = Column(
        Integer,
        ForeignKey("chart_of_accounts.id"),
        nullable=False
    )

    debit = Column(
        Numeric(12, 2),
        default=0
    )

    credit = Column(
        Numeric(12, 2),
        default=0
    )

    description = Column(
        String,
        nullable=True
    )

    journal_entry = relationship(
        "JournalEntry",
        back_populates="lines"
    )