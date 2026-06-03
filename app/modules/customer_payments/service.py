from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.customer_payments.repository import (
    CustomerPaymentRepository
)

from app.modules.customer_payments.schema import (
    CustomerPaymentCreate,
    CustomerPaymentUpdate

)

from app.modules.sales_invoices.model import (
    InvoiceStatus
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


class CustomerPaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: CustomerPaymentCreate,
        organization_id: int,
        user_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.CUSTOMERS
        )

        invoice = (
            CustomerPaymentRepository.get_invoice(
                db=db,
                invoice_id=payment_data.invoice_id,
                organization_id=organization_id
            )
        )

        if not invoice:

            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        if payment_data.amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Payment amount must be greater than zero"
            )

        if payment_data.amount > invoice.due_amount:

            raise HTTPException(
                status_code=400,
                detail="Payment exceeds due amount"
            )

        payment_dict = payment_data.model_dump()

        payment_dict["organization_id"] = (
            organization_id
        )

        payment_dict["created_by"] = user_id

        payment = (
            CustomerPaymentRepository.create_payment(
                db=db,
                payment_data=payment_dict
            )
        )

        invoice.paid_amount += payment.amount

        invoice.due_amount -= payment.amount

        if invoice.due_amount == 0:

            invoice.status = InvoiceStatus.PAID

        else:

            invoice.status = (
                InvoiceStatus.PARTIALLY_PAID
            )

        CustomerPaymentRepository.update_invoice(
            db=db,
            invoice=invoice
        )

        create_customer_payment_journal(
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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.CUSTOMERS
        )


        skip = (page - 1) * limit

        payments = (
            CustomerPaymentRepository.get_all_payments(
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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.CUSTOMERS
        )


        payment = (
            CustomerPaymentRepository.get_payment_by_id(
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
        payment_data: CustomerPaymentUpdate,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.CUSTOMERS
        )


        payment = (
            CustomerPaymentRepository.get_payment_by_id(
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
            CustomerPaymentRepository.update_payment(
                db=db,
                payment=payment
            )
        )

        return updated_payment
    



def create_customer_payment_journal(
    db: Session,
    payment,
    organization_id: int
):

    cash_account = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == 3,
            ChartOfAccount.organization_id == organization_id
        )
        .first()
    )

    accounts_receivable = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.id == 13,
            ChartOfAccount.organization_id == organization_id
        )
        .first()
    )

    if not cash_account:
        raise HTTPException(
            status_code=404,
            detail="Cash Account not found"
        )

    if not accounts_receivable:
        raise HTTPException(
            status_code=404,
            detail="Accounts Receivable account not found"
        )

    journal_entry = JournalEntry(
        organization_id=organization_id,
        reference_type="CUSTOMER_PAYMENT",
        reference_id=str(payment.id),
        description=f"Customer Payment {payment.id}"
    )

    db.add(journal_entry)

    db.flush()

    cash_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=cash_account.id,
        debit=payment.amount,
        credit=0,
        description="Cash Received"
    )

    receivable_line = JournalEntryLine(
        journal_entry_id=journal_entry.id,
        account_id=accounts_receivable.id,
        debit=0,
        credit=payment.amount,
        description="Accounts Receivable"
    )

    db.add(cash_line)
    db.add(receivable_line)