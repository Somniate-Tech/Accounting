from pydantic import BaseModel

from typing import Optional

from decimal import Decimal


class ProductBase(BaseModel):

    name: str

    category_id: int

    unit_id: int

    barcode: Optional[str] = None

    purchase_price: Decimal = 0

    selling_price: Decimal = 0

    gst_percent: Decimal = 0

    opening_stock: Decimal = 0

    minimum_stock: Decimal = 0

    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):

    name: Optional[str] = None

    category_id: Optional[int] = None

    unit_id: Optional[int] = None

    barcode: Optional[str] = None

    purchase_price: Optional[Decimal] = None

    selling_price: Optional[Decimal] = None

    gst_percent: Optional[Decimal] = None

    opening_stock: Optional[Decimal] = None

    current_stock: Optional[Decimal] = None

    minimum_stock: Optional[Decimal] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


class ProductResponse(ProductBase):

    id: int

    organization_id: int

    sku: str

    current_stock: Decimal

    is_active: bool

    class Config:

        from_attributes = True