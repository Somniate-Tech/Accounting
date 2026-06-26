from sqlalchemy.orm import Session

from fastapi import HTTPException
from sqlalchemy import func
from app.modules.bills.schema import (
    BillCreate,
    BillUpdate
)

from app.modules.bills.repository import (
    create_bill_repo,
    get_all_bills_repo,
    get_total_bills_count_repo,
    get_bill_by_code_repo,
    delete_bill_repo,
    update_bill_repo
)

from app.modules.vendors.model import Vendor

from app.modules.purchase_orders.model import (
    PurchaseOrder
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

from app.modules.accounting.journal_entries.model import (
    JournalEntry,
    JournalEntryLine
)

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

def get_system_account(
        db: Session,
        organization_id: int,
        account_name: str
):

    account = (

        db.query(ChartOfAccount)

        .filter(

            ChartOfAccount.organization_id
            ==
            organization_id,


            func.lower(
                ChartOfAccount.account_name
            )

            ==


            account_name.lower()

        )

        .first()

    )


    if not account:

        raise HTTPException(

            status_code=400,

            detail=(
                f"{account_name} account is not configured."
            )

        )



    return account


def create_bill_service(
    db: Session,
    bill: BillCreate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == bill.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if bill.po_code:

        purchase_order = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.po_code == bill.po_code,
                PurchaseOrder.organization_id == organization_id
            )
            .first()
        )

        if not purchase_order:
            raise HTTPException(
                status_code=404,
                detail="Purchase Order not found"
            )
        
    created_bill = create_bill_repo(
        db=db,
        bill=bill,
        organization_id=organization_id
    )

    create_bill_journal(
        db=db,
        bill=created_bill,
        organization_id=organization_id
    )

    db.commit()

    db.refresh(created_bill)


    return {

        "id": str(created_bill.id),
        "bill_code": created_bill.bill_code,
        "vendor_id": str(created_bill.vendor_id),
        "invoice_number": created_bill.invoice_number,
        "invoice_date": created_bill.invoice_date,
        "due_date": created_bill.due_date,
        "subtotal": float(created_bill.subtotal),
        "tax_amount": float(created_bill.tax_amount),
        "total_amount": float(created_bill.total_amount),
        "paid_amount": float(created_bill.paid_amount),
        "due_amount": float(created_bill.due_amount),
        "payment_status":
            created_bill.payment_status.value,
        "notes": created_bill.notes

    }


def get_all_bills_service(
    db: Session,
    page: int,
    limit: int,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    skip = (page - 1) * limit

    bills = get_all_bills_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_bills_count_repo(
        db=db,
        organization_id=organization_id
    )

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": bills
    }


def get_bill_by_code_service(
    db: Session,
    bill_code: str,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    return bill


def delete_bill_service(
    db: Session,
    bill_code: str,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    delete_bill_repo(
        db=db,
        bill=bill
    )

    return {
        "message": "Bill deleted successfully"
    }


def update_bill_service(
    db: Session,
    bill_code: str,
    bill_update: BillUpdate,
    organization_id: int
):
    FeatureGuard.check_feature_access(
        db=db,
        organization_id=organization_id,
        feature_code=FeatureCodes.PURCHASE
    )
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    return update_bill_repo(
        db=db,
        bill=bill,
        bill_update=bill_update,
        organization_id=organization_id
    )


def create_bill_journal(
    db: Session,
    bill,
    organization_id: int
):

    purchase_expense = (

        get_system_account(
            db=db,
            organization_id=organization_id,
            account_name="Purchase Expense"
        )
    )
    accounts_payable = (
        get_system_account(
            db=db,
            organization_id=organization_id,
            account_name="Accounts Payable"
        )
    )

    if not purchase_expense:
        raise HTTPException(
            status_code=404,
            detail="Purchase Expense account not found"
        )

    if not accounts_payable:
        raise HTTPException(
            status_code=404,
            detail="Accounts Payable account not found"
        )

    journal_entry = JournalEntry(
        organization_id=organization_id,
        reference_type="BILL",
        reference_id=str(bill.id),
        description=f"Bill {bill.bill_code}"
    )

    db.add(journal_entry)

    db.flush()

    expense_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=purchase_expense.id,
        debit=bill.total_amount,
        credit=0,
        description="Purchase Expense"
    )

    payable_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=accounts_payable.id,
        debit=0,
        credit=bill.total_amount,
        description="Accounts Payable"
    )

    db.add(expense_line)
    db.add(payable_line)