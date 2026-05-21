from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.journal_entries.repository import (
    JournalEntryRepository
)

from app.modules.accounting.journal_entries.schema import (
    CreateJournalEntrySchema
)


class JournalEntryService:

    @staticmethod
    def create_journal_entry(
        db: Session,
        organization_id: int,
        payload: CreateJournalEntrySchema
    ):

        for line in payload.lines:

            account = db.query(
                ChartOfAccount
            ).filter(
                ChartOfAccount.id == line.account_id,
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.is_active == True
            ).first()

            if not account:

                raise HTTPException(
                    status_code=404,
                    detail=f"Account ID {line.account_id} not found"
                )

        return (
            JournalEntryRepository.create_journal_entry(
                db=db,
                organization_id=organization_id,
                payload=payload
            )
        )

    @staticmethod
    def get_all_entries(
        db: Session,
        organization_id: int
    ):

        return (
            JournalEntryRepository.get_all_entries(
                db=db,
                organization_id=organization_id
            )
        )

    @staticmethod
    def get_entry_by_id(
        db: Session,
        organization_id: int,
        entry_id: int
    ):

        entry = (
            JournalEntryRepository.get_entry_by_id(
                db=db,
                organization_id=organization_id,
                entry_id=entry_id
            )
        )

        if not entry:

            raise HTTPException(
                status_code=404,
                detail="Journal entry not found"
            )

        return entry