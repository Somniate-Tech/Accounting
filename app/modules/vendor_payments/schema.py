from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VendorPaymentCreate(BaseModel):
    vendor_id: UUID
    bill_id: UUID
    amount: float
    payment_method: str
    reference_number: str | None = None
    notes: str | None = None
    payment_date: datetime


class VendorPaymentResponse(BaseModel):
    id: int
    vendor_id: UUID
    bill_id: UUID
    vendor_name: str | None
    bill_code: str | None
    amount: float
    payment_method: str
    reference_number: str | None
    notes: str | None
    payment_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class VendorPaymentUpdate(BaseModel):
    payment_method: str | None = None
    reference_number: str | None = None
    notes: str | None = None