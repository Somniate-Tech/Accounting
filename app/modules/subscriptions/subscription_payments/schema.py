from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SubscriptionPaymentCreate(BaseModel):
    plan_id: int
    billing_cycle: str


class SubscriptionPaymentResponse(BaseModel):
    id: int
    organization_id: int
    plan_id: int

    amount: float

    billing_cycle: str

    gateway: str

    order_id: Optional[str] = None
    payment_id: Optional[str] = None

    status: str

    paid_at: Optional[datetime] = None

    created_at: datetime

    class Config:
        from_attributes = True