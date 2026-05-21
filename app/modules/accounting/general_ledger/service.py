from decimal import Decimal

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.journal_entries.model import (
    JournalEntryLine,
    JournalEntry
)


class GeneralLedgerService:

    @staticmethod
    def get_account_ledger(
        db: Session,
        organization_id: int,
        account_id: int
    ):

        account = db.query(
            ChartOfAccount
        ).filter(
            ChartOfAccount.id == account_id,
            ChartOfAccount.organization_id == organization_id
        ).first()

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        ledger_lines = db.query(
            JournalEntryLine,
            JournalEntry
        ).join(
            JournalEntry,
            JournalEntry.id == JournalEntryLine.journal_entry_id
        ).filter(
            JournalEntry.organization_id == organization_id,
            JournalEntryLine.account_id == account_id
        ).order_by(
            JournalEntry.entry_date.asc()
        ).all()

        running_balance = Decimal("0.00")

        ledger_data = []

        for line, entry in ledger_lines:

            running_balance += (
                Decimal(line.debit)
                -
                Decimal(line.credit)
            )

            ledger_data.append({

                "entry_date": entry.entry_date,

                "journal_entry_id": entry.id,

                "description": line.description,

                "debit": line.debit,

                "credit": line.credit,

                "balance": running_balance
            })

        return ledger_data