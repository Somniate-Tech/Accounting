from pydantic import BaseModel


class FeatureCreate(BaseModel):
    name: str
    code: str
    description: str | None = None


class FeatureResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str | None = None
    is_active: bool

    class Config:
        from_attributes = True