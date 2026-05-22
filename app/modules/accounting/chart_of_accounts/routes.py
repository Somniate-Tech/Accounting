from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.accounting.chart_of_accounts.schema import (
    CreateChartOfAccountSchema,
    UpdateChartOfAccountSchema,
    ChartOfAccountResponseSchema
)

from app.modules.accounting.chart_of_accounts.service import (
    ChartOfAccountService
)

router = APIRouter(
    prefix="/chart-of-accounts",
    tags=["Chart Of Accounts"]
)


@router.post(
    "/",
    response_model=ChartOfAccountResponseSchema
)
def create_account(
    payload: CreateChartOfAccountSchema,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ChartOfAccountService.create_account(
        db=db,
        organization_id=organization,
        payload=payload
    )


@router.get(
    "/",
    response_model=list[ChartOfAccountResponseSchema]
)
def get_all_accounts(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ChartOfAccountService.get_all_accounts(
        db=db,
        organization_id=organization
    )


@router.get(
    "/{account_id}",
    response_model=ChartOfAccountResponseSchema
)
def get_account_by_id(
    account_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ChartOfAccountService.get_account_by_id(
        db=db,
        organization_id=organization,
        account_id=account_id
    )


@router.put(
    "/{account_id}",
    response_model=ChartOfAccountResponseSchema
)
def update_account(
    account_id: int,
    payload: UpdateChartOfAccountSchema,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ChartOfAccountService.update_account(
        db=db,
        organization_id=organization,
        account_id=account_id,
        payload=payload
    )


@router.delete(
    "/{account_id}"
)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ChartOfAccountService.delete_account(
        db=db,
        organization_id=organization,
        account_id=account_id
    )