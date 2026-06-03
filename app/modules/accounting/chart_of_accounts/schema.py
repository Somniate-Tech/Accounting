from typing import Optional

from pydantic import BaseModel


class ChartOfAccountBase(BaseModel):

    account_name: str

    account_type: str

    parent_account_id: Optional[int] = None


class CreateChartOfAccountSchema(
    ChartOfAccountBase
):
    pass


class UpdateChartOfAccountSchema(BaseModel):

    account_name: Optional[str] = None

    account_type: Optional[str] = None

    parent_account_id: Optional[int] = None

    is_active: Optional[bool] = None


class ChartOfAccountResponseSchema(
    ChartOfAccountBase
):

    id: int

    organization_id: int

    account_code: str

    is_active: bool

    class Config:

        from_attributes = True