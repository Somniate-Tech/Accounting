from sqlalchemy.orm import Session

from app.modules.accounting.general_ledger.repository import (
    get_account_ledger_repo
)


def get_account_ledger_service(
    db: Session,
    account_id: int,
    organization_id: int
):

    ledger_entries = get_account_ledger_repo(
        db=db,
        account_id=account_id,
        organization_id=organization_id
    )

    balance = 0

    result = []

    for entry in ledger_entries:

        debit = float(entry.debit or 0)

        credit = float(entry.credit or 0)

        balance += debit - credit

        result.append({
            "entry_date": entry.entry_date,
            "journal_entry_id": entry.journal_entry_id,
            "description": entry.description,
            "debit": debit,
            "credit": credit,
            "balance": balance
        })

    return result