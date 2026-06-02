from decimal import Decimal

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.vendor_payments.repository import (
    VendorPaymentRepository
)

from app.modules.vendor_payments.schema import (
    VendorPaymentCreate,
    VendorPaymentUpdate,
)

from app.modules.bills.model import (
    BillPaymentStatus
)
from app.modules.accounting.journal_entries.model import (
    JournalEntry,
    JournalEntryLine
)

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

class VendorPaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: VendorPaymentCreate,
        organization_id: int,
        user_id: int
    ):

        bill = (
            VendorPaymentRepository.get_bill(
                db=db,
                bill_id=payment_data.bill_id,
                organization_id=organization_id
            )
        )

        if not bill:

            raise HTTPException(
                status_code=404,
                detail="Bill not found"
            )

        payment_amount = Decimal(str(payment_data.amount))

        if payment_amount <= Decimal("0"):

            raise HTTPException(
                status_code=400,
                detail="Payment amount must be greater than zero"
            )

        bill_due_amount = bill.due_amount or Decimal("0")

        if payment_amount > bill_due_amount:

            raise HTTPException(
                status_code=400,
                detail="Payment exceeds due amount"
            )

        payment_dict = payment_data.model_dump()

        payment_dict["amount"] = float(payment_amount)

        payment_dict["organization_id"] = organization_id

        payment_dict["created_by"] = user_id

        payment = (
            VendorPaymentRepository.create_payment(
                db=db,
                payment_data=payment_dict
            )
        )

        bill.paid_amount = (
            bill.paid_amount or Decimal("0")
        ) + payment_amount

        bill.due_amount = (
            bill.due_amount or Decimal("0")
        ) - payment_amount

        if bill.due_amount == Decimal("0"):

            bill.payment_status = BillPaymentStatus.PAID

        else:

            bill.payment_status = BillPaymentStatus.PARTIALLY_PAID

        VendorPaymentRepository.update_bill(
            db=db,
            bill=bill
        )
        create_vendor_payment_journal(
            db=db,
            payment=payment,
            organization_id=organization_id
        )

        db.commit()

        return payment

    @staticmethod
    def get_all_payments(
        db: Session,
        organization_id: int,
        page: int,
        limit: int
    ):

        skip = (page - 1) * limit

        payments = (
            VendorPaymentRepository.get_all_payments(
                db=db,
                organization_id=organization_id,
                skip=skip,
                limit=limit
            )
        )

        return payments

    @staticmethod
    def get_single_payment(
        db: Session,
        payment_id: int,
        organization_id: int
    ):

        payment = (
            VendorPaymentRepository.get_payment_by_id(
                db=db,
                payment_id=payment_id,
                organization_id=organization_id
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return payment

    @staticmethod
    def update_payment(
        db: Session,
        payment_id: int,
        payment_data: VendorPaymentUpdate,
        organization_id: int
    ):

        payment = (
            VendorPaymentRepository.get_payment_by_id(
                db=db,
                payment_id=payment_id,
                organization_id=organization_id
            )
        )

        if not payment:

            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        update_data = (
            payment_data.model_dump(
                exclude_unset=True
            )
        )

        for key, value in update_data.items():

            setattr(payment, key, value)

        updated_payment = (
            VendorPaymentRepository.update_payment(
                db=db,
                payment=payment
            )
        )

        return updated_payment
    


def create_vendor_payment_journal(
    db: Session,
    payment,
    organization_id: int
):

    accounts_payable = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == 16,
            ChartOfAccount.organization_id == organization_id
        )
        .first()
    )

    cash_account = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == 3,
            ChartOfAccount.organization_id == organization_id
        )
        .first()
    )

    if not accounts_payable:
        raise HTTPException(
            status_code=404,
            detail="Accounts Payable account not found"
        )

    if not cash_account:
        raise HTTPException(
            status_code=404,
            detail="Cash Account not found"
        )

    journal_entry = JournalEntry(
        organization_id=organization_id,
        reference_type="VENDOR_PAYMENT",
        reference_id=str(payment.id),
        description=f"Vendor Payment #{payment.id}"
    )

    db.add(journal_entry)

    db.flush()

    payable_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=accounts_payable.id,
        debit=payment.amount,
        credit=0,
        description="Accounts Payable"
    )

    cash_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=cash_account.id,
        debit=0,
        credit=payment.amount,
        description="Cash Paid"
    )

    db.add(payable_line)
    db.add(cash_line)