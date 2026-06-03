from datetime import datetime

from pydantic import BaseModel


class CustomerPaymentCreate(BaseModel):
    customer_id: int

    invoice_id: int

    amount: float

    payment_method: str

    reference_number: str | None = None

    notes: str | None = None

    payment_date: datetime


class CustomerPaymentResponse(BaseModel):
    id: int

    customer_id: int

    invoice_id: int

    amount: float

    payment_method: str

    reference_number: str | None

    notes: str | None

    payment_date: datetime

    created_at: datetime

    class Config:
        from_attributes = True

class CustomerPaymentUpdate(BaseModel):

    payment_method: str | None = None

    reference_number: str | None = None

    notes: str | None = None