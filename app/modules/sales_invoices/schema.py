from pydantic import BaseModel

from typing import List
from typing import Optional

from datetime import datetime

from enum import Enum


class InvoiceStatus(str, Enum):

    DRAFT = "DRAFT"

    SENT = "SENT"

    PARTIALLY_PAID = "PARTIALLY_PAID"

    PAID = "PAID"

    OVERDUE = "OVERDUE"

    CANCELLED = "CANCELLED"


class SalesInvoiceItemBase(BaseModel):

    product_id: int

    item_name: str

    quantity: int

    price: float

    tax_percent: Optional[float] = 0


class SalesInvoiceItemCreate(
    SalesInvoiceItemBase
):
    pass


class SalesInvoiceItemResponse(
    SalesInvoiceItemBase
):

    id: int

    total: float

    class Config:

        from_attributes = True


class SalesInvoiceCreate(BaseModel):

    customer_id: int

    sales_order_id: Optional[int] = None

    due_date: Optional[datetime] = None

    notes: Optional[str] = None

    items: List[
        SalesInvoiceItemCreate
    ]


class SalesInvoiceUpdate(BaseModel):

    status: Optional[
        InvoiceStatus
    ] = None

    paid_amount: Optional[
        float
    ] = None

    due_date: Optional[
        datetime
    ] = None

    notes: Optional[
        str
    ] = None


class SalesInvoiceResponse(BaseModel):

    id: int

    invoice_number: str

    status: InvoiceStatus

    subtotal: float

    tax_amount: float

    total_amount: float

    paid_amount: float

    due_amount: float

    notes: Optional[str]

    due_date: Optional[datetime]

    created_at: datetime

    items: List[
        SalesInvoiceItemResponse
    ]

    class Config:

        from_attributes = True