from pydantic import BaseModel
from datetime import datetime

class AdminDashboardResponse(BaseModel):

    total_users: int

    total_organizations: int

    active_subscriptions: int

    trial_subscriptions: int

    expired_subscriptions: int


class OrganizationResponse(BaseModel):

    id: int

    organization_name: str

    organization_type: str

    gst_number: str | None = None

    phone: str | None = None

    class Config:

        from_attributes = True

class UserResponse(BaseModel):

    id: int

    email: str

    role: str

    is_active: bool

    is_verified: bool

    class Config:

        from_attributes = True


class SubscriptionResponse(BaseModel):

    id: int

    organization_id: int

    plan_id: int

    status: str

    is_trial: bool

    start_date: datetime

    end_date: datetime

    class Config:

        from_attributes = True


class RevenueDashboardResponse(BaseModel):

    active_subscriptions: int

    trial_subscriptions: int

    expired_subscriptions: int

    monthly_revenue: float

    yearly_revenue: float

