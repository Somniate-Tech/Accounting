from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class PurchaseRegisterItem(BaseModel):
    bill_id: str

    bill_code: str
    invoice_number: str

    vendor_name: str

    invoice_date: date

    total_amount: Decimal

    due_amount: Decimal

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


class SalesRegisterItem(BaseModel):
    invoice_id: int

    invoice_number: str

    customer_name: str

    total_amount: float

    paid_amount: float

    due_amount: float

    status: str


class SalesRegisterResponse(BaseModel):
    items: list[SalesRegisterItem]

    total_sales_amount: float

    total_paid_amount: float

    total_due_amount: float

class CustomerLedgerItem(BaseModel):
    date: datetime

    invoice_number: str

    debit: float

    credit: float

    balance: float


class CustomerLedgerResponse(BaseModel):
    customer_name: str

    items: list[CustomerLedgerItem]

    total_debit: float

    total_credit: float

    closing_balance: float


class OutstandingReceivableItem(BaseModel):
    customer_name: str

    total_invoices: int

    outstanding_amount: float


class OutstandingReceivablesResponse(BaseModel):
    items: list[OutstandingReceivableItem]

    total_outstanding: float


class CustomerAgingItem(BaseModel):
    customer_name: str

    current: float

    days_31_60: float

    days_61_90: float

    above_90_days: float


class CustomerAgingResponse(BaseModel):
    items: list[CustomerAgingItem]


class ProfitByCustomerItem(BaseModel):
    customer_name: str

    total_sales: float

    estimated_profit: float


class ProfitByCustomerResponse(BaseModel):
    items: list[ProfitByCustomerItem]

    total_sales_amount: float

    total_estimated_profit: float


class VendorAgingItem(BaseModel):
    vendor_name: str

    current: float

    days_31_60: float

    days_61_90: float

    above_90_days: float


class VendorAgingResponse(BaseModel):
    items: list[VendorAgingItem]


class StockSummaryItem(BaseModel):

    product_id: str

    product_name: str

    current_stock: float


class StockSummaryResponse(BaseModel):

    items: list[StockSummaryItem]



class LowStockItem(BaseModel):

    product_id: str

    product_name: str

    current_stock: float

    minimum_stock: float


class LowStockResponse(BaseModel):

    items: list[LowStockItem]


class InventoryValuationItem(BaseModel):

    product_id: str

    product_name: str

    current_stock: float

    purchase_price: float

    total_value: float


class InventoryValuationResponse(BaseModel):

    items: list[InventoryValuationItem]

    total_inventory_value: float

class FastMovingItem(BaseModel):

    product_id: str

    product_name: str

    total_quantity_sold: float


class FastMovingItemsResponse(BaseModel):

    items: list[FastMovingItem]


class DeadStockItem(BaseModel):

    product_id: str

    product_name: str

    current_stock: float

    last_sold_date: datetime | None = None


class DeadStockResponse(BaseModel):

    items: list[DeadStockItem]

class WarehouseReportItem(BaseModel):

    warehouse_id: str

    warehouse_name: str

    total_products: int

    total_stock: float


class WarehouseReportResponse(BaseModel):

    warehouse_id: int

    warehouse_name: str

    total_products: int

    total_stock: float

    inventory_value: float

class WarehouseReportResponse(BaseModel):

    items: list[WarehouseReportItem]