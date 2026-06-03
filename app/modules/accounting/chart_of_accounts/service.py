from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.chart_of_accounts.schema import (
    CreateChartOfAccountSchema,
    UpdateChartOfAccountSchema
)

from app.modules.accounting.chart_of_accounts.repository import (
    ChartOfAccountRepository
)
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

class ChartOfAccountService:

    @staticmethod
    def generate_account_code(
        db: Session,
        account_type: str,
        organization_id: int
    ):

        type_prefix = {

            "ASSET": 1000,

            "LIABILITY": 2000,

            "EQUITY": 3000,

            "REVENUE": 4000,

            "EXPENSE": 5000
        }

        prefix = type_prefix.get(account_type)

        latest_account = (
            db.query(ChartOfAccount)
            .filter(
                ChartOfAccount.account_type == account_type,
                ChartOfAccount.organization_id == organization_id
            )
            .order_by(
                ChartOfAccount.account_code.desc()
            )
            .first()
        )

        if latest_account:

            return str(
                int(latest_account.account_code) + 10
            )

        return str(prefix)

    @staticmethod
    def create_account(
        db: Session,
        organization_id: int,
        payload: CreateChartOfAccountSchema
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.ACCOUNTING
        )

        generated_code = (
            ChartOfAccountService.generate_account_code(
                db=db,
                account_type=payload.account_type,
                organization_id=organization_id
            )
        )

        return (
            ChartOfAccountRepository.create_account(
                db=db,
                organization_id=organization_id,
                payload=payload,
                generated_code=generated_code
            )
        )

    @staticmethod
    def get_all_accounts(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.ACCOUNTING
        )

        return (
            ChartOfAccountRepository.get_all_accounts(
                db=db,
                organization_id=organization_id
            )
        )

    @staticmethod
    def get_account_by_id(
        db: Session,
        organization_id: int,
        account_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.ACCOUNTING
        )

        account = (
            ChartOfAccountRepository.get_account_by_id(
                db=db,
                organization_id=organization_id,
                account_id=account_id
            )
        )

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return account

    @staticmethod
    def update_account(
        db: Session,
        organization_id: int,
        account_id: int,
        payload: UpdateChartOfAccountSchema
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.ACCOUNTING
        )

        account = (
            ChartOfAccountRepository.get_account_by_id(
                db=db,
                organization_id=organization_id,
                account_id=account_id
            )
        )

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return (
            ChartOfAccountRepository.update_account(
                db=db,
                account=account,
                payload=payload
            )
        )

    @staticmethod
    def delete_account(
        db: Session,
        organization_id: int,
        account_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.ACCOUNTING
        )

        account = (
            ChartOfAccountRepository.get_account_by_id(
                db=db,
                organization_id=organization_id,
                account_id=account_id
            )
        )

        if not account:

            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return (
            ChartOfAccountRepository.delete_account(
                db=db,
                account=account
            )
        )