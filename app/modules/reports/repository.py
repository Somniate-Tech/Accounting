from sqlalchemy.orm import Session

from app.modules.bills.model import Bill
from app.modules.vendors.model import Vendor


class ReportRepository:

    @staticmethod
    def get_purchase_register(
        db: Session,
        organization_id: int
    ):

        purchase_register = (
            db.query(
                Bill.id,
                Bill.bill_code,
                Bill.invoice_number,
                Bill.invoice_date,
                Bill.total_amount,
                Bill.payment_status,

                Vendor.vendor_name.label("vendor_name")
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .order_by(
                Bill.invoice_date.desc()
            )

            .all()
        )

        return purchase_register
    

    @staticmethod
    def get_vendor_ledger(
        db: Session,
        organization_id: int,
        vendor_id
    ):

        ledger_entries = (
            db.query(
                Bill.invoice_date.label("date"),

                Bill.bill_code.label("reference"),

                Bill.invoice_number.label("description"),

                Bill.total_amount.label("credit")
            )

            .filter(
                Bill.organization_id == organization_id,
                Bill.vendor_id == vendor_id
            )

            .order_by(
                Bill.invoice_date.asc()
            )

            .all()
        )

        return ledger_entries
    
    @staticmethod
    def get_outstanding_payables(
        db: Session,
        organization_id: int
    ):

        outstanding_payables = (
            db.query(
                Vendor.vendor_name.label("vendor_name"),

                Bill.vendor_id,

                Bill.total_amount
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .all()
        )

        return outstanding_payables
    

    @staticmethod
    def get_expense_report(
        db: Session,
        organization_id: int
    ):

        expense_rows = (
            db.query(
                Vendor.vendor_name.label("vendor_name"),

                Bill.total_amount
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .all()
        )

        return expense_rows