from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.modules.accounting.journal_entries.model import JournalEntryLine
from app.modules.accounting.chart_of_accounts.model import ChartOfAccount
from app.modules.reports.repository import ReportRepository
from app.modules.reports.schema import (
    PurchaseRegisterItem,
    PurchaseRegisterResponse
)
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.feature_guard import (
    FeatureGuard
)

from app.core.constants import (
    FeatureCodes
)

from app.modules.reports.schema import (
    VendorLedgerItem,
    VendorLedgerResponse,
    OutstandingPayableItem,
    OutstandingPayablesResponse,
    ExpenseReportItem,
    ExpenseReportResponse,
    SalesRegisterItem,
    SalesRegisterResponse,
    CustomerLedgerItem,
    CustomerLedgerResponse,
    OutstandingReceivableItem,
    OutstandingReceivablesResponse,
    CustomerAgingItem,
    CustomerAgingResponse,
    ProfitByCustomerItem,
    ProfitByCustomerResponse,
    VendorAgingItem,
    VendorAgingResponse,
     StockSummaryItem,
    StockSummaryResponse,
    LowStockItem,
    LowStockResponse,
    InventoryValuationItem,
    InventoryValuationResponse,
    FastMovingItem,
    FastMovingItemsResponse,
    DeadStockItem,
    DeadStockResponse,
    WarehouseReportItem,
    WarehouseReportResponse,

)

class ReportService:

    @staticmethod
    def get_trial_balance(db: Session, organization_id: int):

        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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

        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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

        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

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
    

    @staticmethod
    def get_sales_register(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        sales_rows = ReportRepository.get_sales_register(
            db=db,
            organization_id=organization_id
        )

        items = []

        total_sales_amount = 0
        total_paid_amount = 0
        total_due_amount = 0

        for row in sales_rows:

            item = SalesRegisterItem(
                invoice_id=row.id,

                invoice_number=row.invoice_number,

                customer_name=row.customer_name,

                total_amount=row.total_amount,

                paid_amount=row.paid_amount,

                due_amount=row.due_amount,

                status=row.status.value
            )

            items.append(item)

            total_sales_amount += (
                row.total_amount or 0
            )

            total_paid_amount += (
                row.paid_amount or 0
            )

            total_due_amount += (
                row.due_amount or 0
            )

        return SalesRegisterResponse(
            items=items,

            total_sales_amount=total_sales_amount,

            total_paid_amount=total_paid_amount,

            total_due_amount=total_due_amount
        )
    

    @staticmethod
    def get_customer_ledger(
        db: Session,
        organization_id: int,
        customer_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        ledger_rows, customer = (
            ReportRepository.get_customer_ledger(
                db=db,
                organization_id=organization_id,
                customer_id=customer_id
            )
        )

        items = []

        running_balance = 0

        total_debit = 0

        total_credit = 0

        for row in ledger_rows:

            debit = row.debit or 0

            credit = 0

            running_balance += debit

            total_debit += debit

            item = CustomerLedgerItem(
                date=row.date,

                invoice_number=row.invoice_number,

                debit=debit,

                credit=credit,

                balance=running_balance
            )

            items.append(item)

        return CustomerLedgerResponse(
            customer_name=customer.customer_name,

            items=items,

            total_debit=total_debit,

            total_credit=total_credit,

            closing_balance=running_balance
        )
    

    @staticmethod
    def get_outstanding_receivables(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        receivable_rows = (
            ReportRepository.get_outstanding_receivables(
                db=db,
                organization_id=organization_id
            )
        )

        customer_map = {}

        total_outstanding = 0

        for row in receivable_rows:

            customer_name = row.customer_name

            if customer_name not in customer_map:

                customer_map[customer_name] = {
                    "total_invoices": 0,
                    "outstanding_amount": 0
                }

            customer_map[customer_name]["total_invoices"] += 1

            customer_map[customer_name]["outstanding_amount"] += (
                row.due_amount or 0
            )

            total_outstanding += (
                row.due_amount or 0
            )

        items = []

        for customer_name, data in customer_map.items():

            item = OutstandingReceivableItem(
                customer_name=customer_name,

                total_invoices=data["total_invoices"],

                outstanding_amount=data["outstanding_amount"]
            )

            items.append(item)

        return OutstandingReceivablesResponse(
            items=items,

            total_outstanding=total_outstanding
        )
    


    @staticmethod
    def get_customer_aging(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        aging_rows = ReportRepository.get_customer_aging(
            db=db,
            organization_id=organization_id
        )

        customer_map = {}

        today = datetime.now().date()

        for row in aging_rows:

            customer_name = row.customer_name

            if customer_name not in customer_map:

                customer_map[customer_name] = {
                    "current": 0,
                    "days_31_60": 0,
                    "days_61_90": 0,
                    "above_90_days": 0
                }

            due_amount = row.due_amount or 0

            if row.due_date:

                overdue_days = (
                    today - row.due_date
                ).days

            else:

                overdue_days = 0

            if overdue_days <= 30:

                customer_map[customer_name]["current"] += due_amount

            elif overdue_days <= 60:

                customer_map[customer_name]["days_31_60"] += due_amount

            elif overdue_days <= 90:

                customer_map[customer_name]["days_61_90"] += due_amount

            else:

                customer_map[customer_name]["above_90_days"] += due_amount

        items = []

        for customer_name, data in customer_map.items():

            item = CustomerAgingItem(
                customer_name=customer_name,

                current=data["current"],

                days_31_60=data["days_31_60"],

                days_61_90=data["days_61_90"],

                above_90_days=data["above_90_days"]
            )

            items.append(item)

        return CustomerAgingResponse(
            items=items
        )
    


    @staticmethod
    def get_profit_by_customer(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        profit_rows = (
            ReportRepository.get_profit_by_customer(
                db=db,
                organization_id=organization_id
            )
        )

        customer_map = {}

        total_sales_amount = 0

        total_estimated_profit = 0

        for row in profit_rows:

            customer_name = row.customer_name

            if customer_name not in customer_map:

                customer_map[customer_name] = {
                    "total_sales": 0,
                    "estimated_profit": 0
                }

            total_sales = row.total_amount or 0

            estimated_profit = total_sales * 0.30

            customer_map[customer_name]["total_sales"] += total_sales

            customer_map[customer_name]["estimated_profit"] += (
                estimated_profit
            )

            total_sales_amount += total_sales

            total_estimated_profit += estimated_profit

        items = []

        for customer_name, data in customer_map.items():

            item = ProfitByCustomerItem(
                customer_name=customer_name,

                total_sales=data["total_sales"],

                estimated_profit=data["estimated_profit"]
            )

            items.append(item)

        return ProfitByCustomerResponse(
            items=items,

            total_sales_amount=total_sales_amount,

            total_estimated_profit=total_estimated_profit
        )
    

    @staticmethod
    def get_vendor_aging(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        aging_rows = ReportRepository.get_vendor_aging(
            db=db,
            organization_id=organization_id
        )

        vendor_map = {}

        today = datetime.now().date()

        for row in aging_rows:

            vendor_name = row.vendor_name

            if vendor_name not in vendor_map:

                vendor_map[vendor_name] = {
                    "current": 0,
                    "days_31_60": 0,
                    "days_61_90": 0,
                    "above_90_days": 0
                }

            total_amount = row.total_amount or 0

            if row.due_date:

                overdue_days = (
                    today - row.due_date
                ).days

            else:

                overdue_days = 0

            if overdue_days <= 30:

                vendor_map[vendor_name]["current"] += total_amount

            elif overdue_days <= 60:

                vendor_map[vendor_name]["days_31_60"] += total_amount

            elif overdue_days <= 90:

                vendor_map[vendor_name]["days_61_90"] += total_amount

            else:

                vendor_map[vendor_name]["above_90_days"] += total_amount

        items = []

        for vendor_name, data in vendor_map.items():

            item = VendorAgingItem(
                vendor_name=vendor_name,

                current=data["current"],

                days_31_60=data["days_31_60"],

                days_61_90=data["days_61_90"],

                above_90_days=data["above_90_days"]
            )

            items.append(item)

        return VendorAgingResponse(
            items=items
        )
    

    @staticmethod
    def get_stock_summary(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        stock_data = (
            ReportRepository.get_stock_summary(
                db=db,
                organization_id=organization_id
            )
        )

        items = [

            StockSummaryItem(

                product_id=str(
                    item.product_id
                ),

                product_name=item.product_name,

                current_stock=float(
                    item.current_stock
                )
            )

            for item in stock_data
        ]

        return StockSummaryResponse(
            items=items
        )
    

    @staticmethod
    def get_low_stock_report(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        low_stock_products = (

            ReportRepository.get_low_stock_products(
                db=db,
                organization_id=organization_id
            )
        )

        items = [

            LowStockItem(

                product_id=str(
                    item.product_id
                ),

                product_name=item.product_name,

                current_stock=float(
                    item.current_stock
                ),

                minimum_stock=float(
                    item.minimum_stock
                )
            )

            for item in low_stock_products
        ]

        return LowStockResponse(
            items=items
        )
    

    @staticmethod
    def get_inventory_valuation(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        products = (

            ReportRepository.get_inventory_valuation(
                db=db,
                organization_id=organization_id
            )
        )

        items = []

        total_inventory_value = 0

        for product in products:

            total_value = (
                float(product.current_stock)
                *
                float(product.purchase_price)
            )

            total_inventory_value += total_value

            items.append(

                InventoryValuationItem(

                    product_id=str(
                        product.product_id
                    ),

                    product_name=product.product_name,

                    current_stock=float(
                        product.current_stock
                    ),

                    purchase_price=float(
                        product.purchase_price
                    ),

                    total_value=total_value
                )
            )

        return InventoryValuationResponse(
            items=items,

            total_inventory_value=
            total_inventory_value
        )
    

    @staticmethod
    def get_fast_moving_items(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        products = (

            ReportRepository.get_fast_moving_items(
                db=db,
                organization_id=organization_id
            )
        )

        items = [

            FastMovingItem(

                 product_id="0",

                product_name=item.product_name,

                total_quantity_sold=float(
                    item.total_quantity_sold
                )
            )

            for item in products
        ]

        return FastMovingItemsResponse(
            items=items
        )
    
    @staticmethod
    def get_dead_stock_report(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        products = (

            ReportRepository.get_dead_stock_items(
                db=db,
                organization_id=organization_id
            )
        )

        cutoff_date = (
            datetime.utcnow()
            - timedelta(days=90)
        )

        items = []

        for product in products:

            if (

                product.last_sold_date is None

                or

                product.last_sold_date
                < cutoff_date
            ):

                items.append(

                    DeadStockItem(

                        product_id=str(
                            product.product_id
                        ),

                        product_name=product.product_name,

                        current_stock=float(
                            product.current_stock
                        ),

                        last_sold_date=
                        product.last_sold_date
                    )
                )

        return DeadStockResponse(
            items=items
        )
    

    @staticmethod
    def get_warehouse_report(
        db: Session,
        organization_id: int
    ):
        FeatureGuard.check_feature_access(
            db=db,
            organization_id=organization_id,
            feature_code=FeatureCodes.REPORTS
        )

        warehouses = (

            ReportRepository.get_warehouse_report(
                db=db,
                organization_id=organization_id
            )
        )

        items = [

            WarehouseReportItem(

                warehouse_id=str(
                    item.warehouse_id
                ),

                warehouse_name=item.warehouse_name,

                total_products=int(
                    item.total_products
                ),

                total_stock=float(
                    item.total_stock or 0
                )
            )

            for item in warehouses
        ]

        return WarehouseReportResponse(
            items=items
        )