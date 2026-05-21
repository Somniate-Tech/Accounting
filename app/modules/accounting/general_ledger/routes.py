from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.accounting.general_ledger.service import (
    GeneralLedgerService
)

from app.modules.accounting.general_ledger.schema import (
    LedgerEntryResponseSchema
)

router = APIRouter(
    prefix="/general-ledger",
    tags=["General Ledger"]
)


@router.get(
    "/{account_id}",
    response_model=list[LedgerEntryResponseSchema]
)
def get_account_ledger(
    account_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return GeneralLedgerService.get_account_ledger(
        db=db,
        organization_id=organization.id,
        account_id=account_id
    )