from decimal import Decimal

from datetime import datetime

from pydantic import BaseModel


class LedgerEntryResponseSchema(BaseModel):

    entry_date: datetime

    journal_entry_id: int

    description: str | None = None

    debit: Decimal

    credit: Decimal

    balance: Decimal

    class Config:

        from_attributes = True