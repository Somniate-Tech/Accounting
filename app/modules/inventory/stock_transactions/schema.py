from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class StockTransactionBase(BaseModel):

    product_id: int
    warehouse_id: int | None = None
    transaction_type: str

    quantity: Decimal

    reference_type: Optional[str] = None
    reference_id: Optional[int] = None

    remarks: Optional[str] = None


class StockTransactionCreate(
    StockTransactionBase
):
    pass


class StockTransactionResponse(
    StockTransactionBase
):

    id: int

    organization_id: int
    before_stock: Decimal
    after_stock: Decimal

    created_at: datetime

    class Config:
        from_attributes = True