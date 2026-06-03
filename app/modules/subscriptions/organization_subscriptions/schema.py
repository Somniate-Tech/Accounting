from datetime import datetime

from pydantic import BaseModel

class ChoosePlanSchema(BaseModel):
    plan_id: int
    
class OrganizationSubscriptionCreate(BaseModel):

    organization_id: int
    plan_id: int

    status: str = "ACTIVE"

    start_date: datetime
    end_date: datetime

    is_trial: bool = False


class OrganizationSubscriptionResponse(BaseModel):

    id: int

    organization_id: int
    plan_id: int

    status: str

    start_date: datetime
    end_date: datetime

    is_trial: bool

    class Config:
        from_attributes = True


class UpgradePlanSchema(BaseModel):
    plan_id: int