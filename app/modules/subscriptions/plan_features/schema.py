from pydantic import BaseModel


class PlanFeatureCreate(BaseModel):
    plan_id: int
    feature_id: int


class PlanFeatureResponse(BaseModel):
    id: int
    plan_id: int
    feature_id: int

    class Config:
        from_attributes = True