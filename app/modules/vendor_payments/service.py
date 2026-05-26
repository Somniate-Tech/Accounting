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

        if payment_data.amount <= 0:

            raise HTTPException(
                status_code=400,
                detail="Payment amount must be greater than zero"
            )

        if payment_data.amount > float(bill.due_amount):

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
            VendorPaymentRepository.create_payment(
                db=db,
                payment_data=payment_dict
            )
        )

        bill.paid_amount += payment.amount

        bill.due_amount -= payment.amount

        if float(bill.due_amount) == 0:

            bill.payment_status = (
                BillPaymentStatus.PAID
            )

        else:

            bill.payment_status = (
                BillPaymentStatus.PARTIALLY_PAID
            )

        VendorPaymentRepository.update_bill(
            db=db,
            bill=bill
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