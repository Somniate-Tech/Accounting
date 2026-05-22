from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.accounting.journal_entries.model import JournalEntryLine
from app.modules.accounting.chart_of_accounts.model import ChartOfAccount


class ReportService:

    @staticmethod
    def get_trial_balance(db: Session, organization_id: int):

        trial_balance = (
            db.query(
                ChartOfAccount.account_code,
                ChartOfAccount.account_name,
                ChartOfAccount.account_type,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_code,
                ChartOfAccount.account_name,
                ChartOfAccount.account_type
            )

            .all()
        )

        results = []

        total_debit = 0
        total_credit = 0

        for account in trial_balance:

            debit = float(account.total_debit or 0)
            credit = float(account.total_credit or 0)

            balance = debit - credit

            debit_balance = 0
            credit_balance = 0

            if balance > 0:
                debit_balance = balance
            else:
                credit_balance = abs(balance)

            total_debit += debit_balance
            total_credit += credit_balance

            results.append({
                "account_code": account.account_code,
                "account_name": account.account_name,
                "account_type": account.account_type,
                "debit": debit_balance,
                "credit": credit_balance
            })

        return {
            "accounts": results,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "is_balanced": total_debit == total_credit
        }
    

    @staticmethod
    def get_profit_and_loss(db: Session, organization_id: int):

        revenue_accounts = (
            db.query(
                ChartOfAccount.account_name,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.account_type == "REVENUE"
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_name
            )

            .all()
        )

        expense_accounts = (
            db.query(
                ChartOfAccount.account_name,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.account_type == "EXPENSE"
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_name
            )

            .all()
        )

        revenue_data = []
        expense_data = []

        total_revenue = 0
        total_expense = 0

        for account in revenue_accounts:

            revenue = float(account.total_credit or 0) - float(account.total_debit or 0)

            total_revenue += revenue

            revenue_data.append({
                "account_name": account.account_name,
                "amount": revenue
            })

        for account in expense_accounts:

            expense = float(account.total_debit or 0) - float(account.total_credit or 0)

            total_expense += expense

            expense_data.append({
                "account_name": account.account_name,
                "amount": expense
            })

        net_profit = total_revenue - total_expense

        return {
            "revenues": revenue_data,
            "expenses": expense_data,
            "total_revenue": total_revenue,
            "total_expense": total_expense,
            "net_profit": net_profit
        }
    
    @staticmethod
    def get_balance_sheet(db: Session, organization_id: int):

        asset_accounts = (
            db.query(
                ChartOfAccount.account_name,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.account_type == "ASSET"
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_name
            )

            .all()
        )

        liability_accounts = (
            db.query(
                ChartOfAccount.account_name,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.account_type == "LIABILITY"
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_name
            )

            .all()
        )

        equity_accounts = (
            db.query(
                ChartOfAccount.account_name,

                func.sum(JournalEntryLine.debit).label("total_debit"),
                func.sum(JournalEntryLine.credit).label("total_credit")
            )

            .join(
                JournalEntryLine,
                JournalEntryLine.account_id == ChartOfAccount.id
            )

            .filter(
                ChartOfAccount.organization_id == organization_id,
                ChartOfAccount.account_type == "EQUITY"
            )

            .group_by(
                ChartOfAccount.id,
                ChartOfAccount.account_name
            )

            .all()
        )

        assets = []
        liabilities = []
        equity = []

        total_assets = 0
        total_liabilities = 0
        total_equity = 0

        for account in asset_accounts:

            balance = float(account.total_debit or 0) - float(account.total_credit or 0)

            total_assets += balance

            assets.append({
                "account_name": account.account_name,
                "amount": balance
            })

        for account in liability_accounts:

            balance = float(account.total_credit or 0) - float(account.total_debit or 0)

            total_liabilities += balance

            liabilities.append({
                "account_name": account.account_name,
                "amount": balance
            })

        for account in equity_accounts:

            balance = float(account.total_credit or 0) - float(account.total_debit or 0)

            total_equity += balance

            equity.append({
                "account_name": account.account_name,
                "amount": balance
            })

        return {
            "assets": assets,
            "liabilities": liabilities,
            "equity": equity,

            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "total_equity": total_equity,

            "is_balanced":
                total_assets == (total_liabilities + total_equity)
        }