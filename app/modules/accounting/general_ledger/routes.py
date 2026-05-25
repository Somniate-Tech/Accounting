from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import get_current_organization

from app.modules.accounting.general_ledger.service import (
    get_account_ledger_service
)


router = APIRouter(
    prefix="/general-ledger",
    tags=["General Ledger"]
)


@router.get("/{account_id}")
def get_account_ledger(
    account_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return get_account_ledger_service(
        db=db,
        account_id=account_id,
        organization_id=organization
    )