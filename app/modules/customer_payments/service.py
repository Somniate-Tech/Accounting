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


class CustomerPaymentService:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: CustomerPaymentCreate,
        organization_id: int,
        user_id: int
    ):

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