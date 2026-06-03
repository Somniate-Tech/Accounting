from sqlalchemy.orm import Session

from app.modules.accounting.journal_entries.model import (
    JournalEntry,
    JournalEntryLine
)


def get_account_ledger_repo(
    db: Session,
    account_id: int,
    organization_id: int
):

    return (
        db.query(
            JournalEntry.entry_date,
            JournalEntry.id.label("journal_entry_id"),
            JournalEntry.description,

            JournalEntryLine.debit,
            JournalEntryLine.credit
        )

        .join(
            JournalEntryLine,
            JournalEntry.id == JournalEntryLine.journal_entry_id
        )

        .filter(
            JournalEntry.organization_id == organization_id,
            JournalEntryLine.account_id == account_id
        )

        .order_by(
            JournalEntry.entry_date.asc(),
            JournalEntry.id.asc()
        )

        .all()
    )