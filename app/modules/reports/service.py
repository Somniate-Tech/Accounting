from sqlalchemy.orm import Session
from sqlalchemy import func

from app.modules.accounting.journal_entries.model import JournalEntryLine
from app.modules.accounting.chart_of_accounts.model import ChartOfAccount
from app.modules.reports.repository import ReportRepository
from app.modules.reports.schema import (
    PurchaseRegisterItem,
    PurchaseRegisterResponse
)
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession


from app.modules.reports.schema import (
    VendorLedgerItem,
    VendorLedgerResponse,
    OutstandingPayableItem,
    OutstandingPayablesResponse,
    ExpenseReportItem,
    ExpenseReportResponse
)
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
    
    @staticmethod
    def get_purchase_register(
        db: Session,
        organization_id: int
    ):

        purchase_rows = ReportRepository.get_purchase_register(
            db=db,
            organization_id=organization_id
        )

        items = []

        total_purchase_amount = Decimal("0")

        for row in purchase_rows:

            item = PurchaseRegisterItem(
                bill_id=str(row.id),

                bill_code=row.bill_code,
                invoice_number=row.invoice_number,

                vendor_name=row.vendor_name,

                invoice_date=row.invoice_date,

                total_amount=row.total_amount,

                payment_status=row.payment_status.value
            )

            items.append(item)

            total_purchase_amount += (
                row.total_amount or Decimal("0")
            )

        return PurchaseRegisterResponse(
            items=items,
            total_purchase_amount=total_purchase_amount
        )
    

    @staticmethod
    def get_vendor_ledger(
        db: Session,
        organization_id: int,
        vendor_id
    ):

        ledger_rows = ReportRepository.get_vendor_ledger(
            db=db,
            organization_id=organization_id,
            vendor_id=vendor_id
        )

        items = []

        running_balance = Decimal("0")

        total_debit = Decimal("0")
        total_credit = Decimal("0")

        vendor_name = ""

        for row in ledger_rows:

            credit = row.credit or Decimal("0")
            debit = Decimal("0")

            running_balance += credit

            total_credit += credit

            item = VendorLedgerItem(
                date=row.date,

                reference=row.reference,

                description=row.description,

                debit=debit,
                credit=credit,

                balance=running_balance
            )

            items.append(item)

        if items:
            vendor_name = items[0].description

        return VendorLedgerResponse(
            vendor_name=vendor_name,

            items=items,

            total_debit=total_debit,
            total_credit=total_credit,

            closing_balance=running_balance
        )
    

    @staticmethod
    def get_outstanding_payables(
        db: Session,
        organization_id: int
    ):

        payable_rows = ReportRepository.get_outstanding_payables(
            db=db,
            organization_id=organization_id
        )

        vendor_map = {}

        total_outstanding = Decimal("0")

        for row in payable_rows:

            vendor_name = row.vendor_name

            if vendor_name not in vendor_map:

                vendor_map[vendor_name] = {
                    "total_bills": 0,
                    "outstanding_amount": Decimal("0")
                }

            vendor_map[vendor_name]["total_bills"] += 1

            vendor_map[vendor_name]["outstanding_amount"] += (
                row.total_amount or Decimal("0")
            )

            total_outstanding += (
                row.total_amount or Decimal("0")
            )

        items = []

        for vendor_name, data in vendor_map.items():

            item = OutstandingPayableItem(
                vendor_name=vendor_name,

                total_bills=data["total_bills"],

                outstanding_amount=data["outstanding_amount"]
            )

            items.append(item)

        return OutstandingPayablesResponse(
            items=items,

            total_outstanding=total_outstanding
        )
    

    @staticmethod
    def get_expense_report(
        db: Session,
        organization_id: int
    ):

        expense_rows = ReportRepository.get_expense_report(
            db=db,
            organization_id=organization_id
        )

        vendor_map = {}

        total_expense_amount = Decimal("0")

        for row in expense_rows:

            vendor_name = row.vendor_name

            if vendor_name not in vendor_map:

                vendor_map[vendor_name] = Decimal("0")

            vendor_map[vendor_name] += (
                row.total_amount or Decimal("0")
            )

            total_expense_amount += (
                row.total_amount or Decimal("0")
            )

        items = []

        for vendor_name, total_expense in vendor_map.items():

            item = ExpenseReportItem(
                vendor_name=vendor_name,

                total_expense=total_expense
            )

            items.append(item)

        return ExpenseReportResponse(
            items=items,

            total_expense_amount=total_expense_amount
        )