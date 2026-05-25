from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class PurchaseRegisterItem(BaseModel):
    bill_id: str

    bill_code: str
    invoice_number: str

    vendor_name: str

    invoice_date: date

    total_amount: Decimal

    payment_status: str


class PurchaseRegisterResponse(BaseModel):
    items: list[PurchaseRegisterItem]

    total_purchase_amount: Decimal

class VendorLedgerItem(BaseModel):
    date: date

    reference: str
    description: str

    debit: Decimal
    credit: Decimal

    balance: Decimal


class VendorLedgerResponse(BaseModel):
    vendor_name: str

    items: list[VendorLedgerItem]

    total_debit: Decimal
    total_credit: Decimal

    closing_balance: Decimal

class OutstandingPayableItem(BaseModel):
    vendor_name: str

    total_bills: int

    outstanding_amount: Decimal


class OutstandingPayablesResponse(BaseModel):
    items: list[OutstandingPayableItem]

    total_outstanding: Decimal


class ExpenseReportItem(BaseModel):
    vendor_name: str

    total_expense: Decimal


class ExpenseReportResponse(BaseModel):
    items: list[ExpenseReportItem]

    total_expense_amount: Decimal