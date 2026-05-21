from sqlalchemy.orm import Session

from app.modules.accounting.journal_entries.model import (
    JournalEntry,
    JournalEntryLine
)

from app.modules.accounting.journal_entries.schema import (
    CreateJournalEntrySchema
)


class JournalEntryRepository:

    @staticmethod
    def create_journal_entry(
        db: Session,
        organization_id: int,
        payload: CreateJournalEntrySchema
    ):

        journal_entry = JournalEntry(

            organization_id=organization_id,

            reference_type=payload.reference_type,

            reference_id=payload.reference_id,

            description=payload.description
        )

        db.add(journal_entry)

        db.flush()

        for line in payload.lines:

            journal_line = JournalEntryLine(

                journal_entry_id=journal_entry.id,

                account_id=line.account_id,

                debit=line.debit,

                credit=line.credit,

                description=line.description
            )

            db.add(journal_line)

        db.commit()

        db.refresh(journal_entry)

        return journal_entry

    @staticmethod
    def get_all_entries(
        db: Session,
        organization_id: int
    ):

        return db.query(
            JournalEntry
        ).filter(
            JournalEntry.organization_id == organization_id
        ).all()

    @staticmethod
    def get_entry_by_id(
        db: Session,
        organization_id: int,
        entry_id: int
    ):

        return db.query(
            JournalEntry
        ).filter(
            JournalEntry.id == entry_id,
            JournalEntry.organization_id == organization_id
        ).first()