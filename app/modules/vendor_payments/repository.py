from sqlalchemy.orm import Session

from app.modules.vendor_payments.model import (
    VendorPayment
)

from app.modules.bills.model import (
    Bill
)


class VendorPaymentRepository:

    @staticmethod
    def create_payment(
        db: Session,
        payment_data: dict
    ):

        payment = VendorPayment(
            **payment_data
        )

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    @staticmethod
    def get_bill(
        db: Session,
        bill_id: str,
        organization_id: int
    ):

        return (
            db.query(Bill)

            .filter(
                Bill.id == bill_id,

                Bill.organization_id
                == organization_id
            )

            .first()
        )

    @staticmethod
    def update_bill(
        db: Session,
        bill: Bill
    ):

        db.add(bill)

        db.commit()

        db.refresh(bill)

        return bill
    
    @staticmethod
    def get_all_payments(
        db: Session,
        organization_id: int,
        skip: int,
        limit: int
    ):

        return (
            db.query(VendorPayment)

            .filter(
                VendorPayment.organization_id
                == organization_id
            )

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
            db.query(VendorPayment)

            .filter(
                VendorPayment.id == payment_id,

                VendorPayment.organization_id
                == organization_id
            )

            .first()
        )

    @staticmethod
    def update_payment(
        db: Session,
        payment: VendorPayment
    ):

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment