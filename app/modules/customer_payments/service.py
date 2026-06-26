from fastapi import HTTPException
from sqlalchemy import func
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

        db.refresh(payment)


        return {

            "id": payment.id,
            "customer_id": payment.customer_id,
            "customer_name": (
                payment.customer.customer_name
                if payment.customer
                else None
            ),
            "invoice_id": payment.invoice_id,
            "invoice_number": (
                payment.invoice.invoice_number
                if payment.invoice
                else None
            ),
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "reference_number": payment.reference_number,
            "notes": payment.notes,
            "payment_date": payment.payment_date,
            "created_at": payment.created_at
        }

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

        response = []

        for payment in payments:

            response.append(

                {

                    "id": payment.id,

                    "customer_id": payment.customer_id,

                    "customer_name": (
                        payment.customer.customer_name
                        if payment.customer
                        else None
                    ),

                    "invoice_id": payment.invoice_id,

                    "invoice_number": (
                        payment.invoice.invoice_number
                        if payment.invoice
                        else None
                    ),

                    "amount": payment.amount,

                    "payment_method": payment.payment_method,

                    "reference_number": payment.reference_number,

                    "notes": payment.notes,

                    "payment_date": payment.payment_date,

                    "created_at": payment.created_at

                }

            )

        return response

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

        return {

            "id": payment.id,
            "customer_id": payment.customer_id,
            "customer_name": (
                payment.customer.customer_name
                if payment.customer
                else None
            ),
            "invoice_id": payment.invoice_id,
            "invoice_number": (
                payment.invoice.invoice_number
                if payment.invoice
                else None
            ),
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "reference_number": payment.reference_number,
            "notes": payment.notes,
            "payment_date": payment.payment_date,
            "created_at": payment.created_at
        }

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

        return {

            "id": updated_payment.id,
            "customer_id": updated_payment.customer_id,
            "customer_name": (
                updated_payment.customer.customer_name
                if updated_payment.customer
                else None
            ),
            "invoice_id": updated_payment.invoice_id,
            "invoice_number": (
                updated_payment.invoice.invoice_number
                if updated_payment.invoice
                else None
            ),
            "amount": updated_payment.amount,
            "payment_method": updated_payment.payment_method,
            "reference_number": updated_payment.reference_number,
            "notes": updated_payment.notes,
            "payment_date": updated_payment.payment_date,
            "created_at": updated_payment.created_at
        }
    

def get_system_account(
        db: Session,
        organization_id: int,
        account_name: str
):
    account = (
        db.query(ChartOfAccount)
        .filter(
            ChartOfAccount.organization_id==organization_id,
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

def create_customer_payment_journal(
    db: Session,
    payment,
    organization_id: int
):

    cash_account = (
         get_system_account(
            db=db,
            organization_id=organization_id,
            account_name="Cash Account"
        )
    )
    accounts_receivable = (
        get_system_account(
            db=db,
            organization_id=organization_id,
            account_name="Accounts Receivable"
        )

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