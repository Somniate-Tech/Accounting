from sqlalchemy.orm import Session

from app.modules.customer_payments.model import (
    CustomerPayment
)

from app.modules.sales_invoices.model import (
    SalesInvoice
)


class CustomerPaymentRepository:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: dict
    ):

        payment = CustomerPayment(
            **payment_data
        )

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def get_invoice(
        db: Session,
        invoice_id: int,
        organization_id: int
    ):

        return (
            db.query(SalesInvoice)

            .filter(
                SalesInvoice.id == invoice_id,

                SalesInvoice.organization_id
                == organization_id
            )

            .first()
        )

    @staticmethod
    def update_invoice(
        db: Session,
        invoice: SalesInvoice
    ):

        db.add(invoice)

        db.commit()

        db.refresh(invoice)

        return invoice
    

    @staticmethod
    def get_all_payments(
        db: Session,
        organization_id: int,
        skip: int,
        limit: int
    ):

        return (
            db.query(CustomerPayment)

            .filter(
                CustomerPayment.organization_id== organization_id)
            .offset(skip)

            .limit(limit)

            .all()
        )

    @staticmethod
    def get_payment_by_id(
        db: Session,
        payment_id: int,
        organization_id: int
    ):

        return (
            db.query(CustomerPayment)

            .filter(
                CustomerPayment.id == payment_id,
                CustomerPayment.organization_id== organization_id
            )

            .first()
        )

    @staticmethod
    def update_payment(
        db: Session,
        payment: CustomerPayment
    ):

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment