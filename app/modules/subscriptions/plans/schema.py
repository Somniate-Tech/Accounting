from pydantic import BaseModel


class SubscriptionPlanCreate(BaseModel):
    name: str
    code: str
    description: str | None = None

    monthly_price: float
    yearly_price: float

    max_users: int
    max_customers: int
    max_vendors: int
    max_products: int


class SubscriptionPlanResponse(BaseModel):
    id: int

    name: str
    code: str
    description: str | None = None

    monthly_price: float
    yearly_price: float

    max_users: int
    max_customers: int
    max_vendors: int
    max_products: int

    is_active: bool

    class Config:
        from_attributes = True


class SubscriptionPlanUpdate(BaseModel):

    name: str | None = None

    description: str | None = None

    monthly_price: float | None = None

    yearly_price: float | None = None

    max_users: int | None = None

    max_customers: int | None = None

    max_vendors: int | None = None

    max_products: int | None = None