from sqlalchemy.orm import Session

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.chart_of_accounts.schema import (
    CreateChartOfAccountSchema,
    UpdateChartOfAccountSchema
)


class ChartOfAccountRepository:

    @staticmethod
    def create_account(
        db: Session,
        organization_id: int,
        payload: CreateChartOfAccountSchema,
        generated_code: str
    ):

        account = ChartOfAccount(

            organization_id=organization_id,

            account_code=generated_code,

            account_name=payload.account_name,

            account_type=payload.account_type,

            parent_account_id=payload.parent_account_id
        )

        db.add(account)

        db.commit()

        db.refresh(account)

        return account

    @staticmethod
    def get_all_accounts(
        db: Session,
        organization_id: int
    ):

        return db.query(
            ChartOfAccount
        ).filter(
            ChartOfAccount.organization_id == organization_id,
            ChartOfAccount.is_active == True
        ).all()

    @staticmethod
    def get_account_by_id(
        db: Session,
        organization_id: int,
        account_id: int
    ):

        return db.query(
            ChartOfAccount
        ).filter(
            ChartOfAccount.organization_id == organization_id,
            ChartOfAccount.id == account_id,
            ChartOfAccount.is_active == True
        ).first()

    @staticmethod
    def update_account(
        db: Session,
        account: ChartOfAccount,
        payload: UpdateChartOfAccountSchema
    ):

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():

            setattr(account, key, value)

        db.commit()

        db.refresh(account)

        return account

    @staticmethod
    def delete_account(
        db: Session,
        account: ChartOfAccount
    ):

        db.delete(account)

        db.commit()

        return {
            "message": "Account deleted successfully"
    }