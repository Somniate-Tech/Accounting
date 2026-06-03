from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.general_ledger.repository import (
    get_account_ledger_repo
)

from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)


def get_account_ledger_service(
    db: Session,
    account_id: int,
    organization_id: int
):
    # Feature Access Check
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.ACCOUNTING
    )

    # Validate Account Exists
    account = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == account_id,
            ChartOfAccount.organization_id == organization_id,
            ChartOfAccount.is_active == True
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    # Fetch Ledger Entries
    ledger_entries = get_account_ledger_repo(
        db=db,
        account_id=account_id,
        organization_id=organization_id
    )

    running_balance = 0

    entries = []

    for entry in ledger_entries:

        debit = float(entry.debit or 0)

        credit = float(entry.credit or 0)

        running_balance += (debit - credit)

        entries.append({
            "entry_date": entry.entry_date,
            "journal_entry_id": entry.journal_entry_id,
            "description": entry.description,
            "debit": debit,
            "credit": credit,
            "balance": running_balance
        })

    return {
        "account_id": account.id,
        "account_code": account.account_code,
        "account_name": account.account_name,
        "account_type": account.account_type,
        "entries": entries
    }