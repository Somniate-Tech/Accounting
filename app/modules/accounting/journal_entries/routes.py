from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.accounting.journal_entries.schema import (
    CreateJournalEntrySchema
)

from app.modules.accounting.journal_entries.service import (
    JournalEntryService
)

router = APIRouter(
    prefix="/journal-entries",
    tags=["Journal Entries"]
)


@router.post("/")
def create_journal_entry(
    payload: CreateJournalEntrySchema,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return JournalEntryService.create_journal_entry(
        db=db,
        organization_id=organization,
        payload=payload
    )


@router.get("/")
def get_all_entries(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return JournalEntryService.get_all_entries(
        db=db,
        organization_id=organization
    )


@router.get("/{entry_id}")
def get_entry_by_id(
    entry_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return JournalEntryService.get_entry_by_id(
        db=db,
        organization_id=organization,
        entry_id=entry_id
    )