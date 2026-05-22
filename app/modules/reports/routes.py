from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_organization

from app.modules.reports.service import ReportService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/trial-balance")
def get_trial_balance(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_trial_balance(
        db=db,
        organization_id=organization
    )


@router.get("/profit-loss")
def get_profit_and_loss(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_profit_and_loss(
        db=db,
        organization_id=organization
    )

@router.get("/balance-sheet")
def get_balance_sheet(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_balance_sheet(
        db=db,
        organization_id=organization
    )