from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_organization

from app.modules.reports.service import ReportService
from app.modules.reports.schema import (
    PurchaseRegisterResponse,
    VendorLedgerResponse,
    OutstandingPayablesResponse,
    ExpenseReportResponse,
    SalesRegisterResponse,
    CustomerLedgerResponse,
    OutstandingReceivablesResponse,
    CustomerAgingResponse,
    ProfitByCustomerResponse,
    VendorAgingResponse,
)

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


@router.get(
    "/purchase-register",
    response_model=PurchaseRegisterResponse
)
def get_purchase_register(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_purchase_register(
        db=db,
        organization_id=organization
    )

@router.get(
    "/vendor-ledger/{vendor_id}",
    response_model=VendorLedgerResponse
)
def get_vendor_ledger(
    vendor_id,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_vendor_ledger(
        db=db,
        organization_id=organization,
        vendor_id=vendor_id
    )


@router.get(
    "/outstanding-payables",
    response_model=OutstandingPayablesResponse
)
def get_outstanding_payables(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_outstanding_payables(
        db=db,
        organization_id=organization
    )


@router.get(
    "/expense-report",
    response_model=ExpenseReportResponse
)
def get_expense_report(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_expense_report(
        db=db,
        organization_id=organization
    )


@router.get(
    "/vendor-aging",
    response_model=VendorAgingResponse
)
def get_vendor_aging(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_vendor_aging(
        db=db,
        organization_id=organization
    )


@router.get(
    "/sales-register",
    response_model=SalesRegisterResponse
)
def get_sales_register(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_sales_register(
        db=db,
        organization_id=organization
    )


@router.get(
    "/customer-ledger/{customer_id}",
    response_model=CustomerLedgerResponse
)
def get_customer_ledger(
    customer_id: int,
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_customer_ledger(
        db=db,
        organization_id=organization,
        customer_id=customer_id
    )


@router.get(
    "/outstanding-receivables",
    response_model=OutstandingReceivablesResponse
)
def get_outstanding_receivables(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_outstanding_receivables(
        db=db,
        organization_id=organization
    )


@router.get(
    "/customer-aging",
    response_model=CustomerAgingResponse
)
def get_customer_aging(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_customer_aging(
        db=db,
        organization_id=organization
    )


@router.get(
    "/profit-by-customer",
    response_model=ProfitByCustomerResponse
)
def get_profit_by_customer(
    db: Session = Depends(get_db),
    organization=Depends(get_current_organization)
):

    return ReportService.get_profit_by_customer(
        db=db,
        organization_id=organization
    )