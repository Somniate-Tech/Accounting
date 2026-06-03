from sqlalchemy.orm import Session

from app.modules.bills.model import Bill
from app.modules.vendors.model import Vendor
from app.modules.sales_invoices.model import SalesInvoice
from app.modules.customers.model import Customer
from app.modules.customers.model import Customer
from app.modules.sales_invoices.model import SalesInvoice
from sqlalchemy import func
from app.modules.inventory.products.model import (Product)
from sqlalchemy import func

from app.modules.sales_invoices.model import (
    SalesInvoiceItem
)
from sqlalchemy import func

from app.modules.sales_invoices.model import (
    SalesInvoiceItem
)

from app.modules.inventory.products.model import (
    Product
)

from app.modules.sales_invoices.model import (
    SalesInvoice
)
from app.modules.inventory.warehouses.model import (
    Warehouse
)
from app.modules.inventory.stock_transactions.model import (
    StockTransaction
)
from app.modules.inventory.warehouses.model import (
    Warehouse
)

class ReportRepository:

    @staticmethod
    def get_purchase_register(
        db: Session,
        organization_id: int
    ):

        purchase_register = (
            db.query(
                Bill.id,
                Bill.bill_code,
                Bill.invoice_number,
                Bill.invoice_date,
                Bill.total_amount,
                Bill.payment_status,

                Vendor.vendor_name.label("vendor_name")
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .order_by(
                Bill.invoice_date.desc()
            )

            .all()
        )

        return purchase_register
    

    @staticmethod
    def get_vendor_ledger(
        db: Session,
        organization_id: int,
        vendor_id
    ):

        ledger_entries = (
            db.query(
                Bill.invoice_date.label("date"),

                Bill.bill_code.label("reference"),

                Bill.invoice_number.label("description"),

                Bill.total_amount.label("credit")
            )

            .filter(
                Bill.organization_id == organization_id,
                Bill.vendor_id == vendor_id
            )

            .order_by(
                Bill.invoice_date.asc()
            )

            .all()
        )

        return ledger_entries
    
    @staticmethod
    def get_outstanding_payables(
        db: Session,
        organization_id: int
    ):

        outstanding_payables = (
            db.query(
                Vendor.vendor_name.label("vendor_name"),

                Bill.vendor_id,

                Bill.total_amount
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .all()
        )

        return outstanding_payables
    

    @staticmethod
    def get_expense_report(
        db: Session,
        organization_id: int
    ):

        expense_rows = (
            db.query(
                Vendor.vendor_name.label("vendor_name"),

                Bill.total_amount
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .all()
        )

        return expense_rows
    

    @staticmethod
    def get_sales_register(
        db: Session,
        organization_id: int
    ):

        sales_rows = (
            db.query(
                SalesInvoice.id,

                SalesInvoice.invoice_number,

                SalesInvoice.total_amount,

                SalesInvoice.paid_amount,

                SalesInvoice.due_amount,

                SalesInvoice.status,

                Customer.customer_name.label("customer_name")
            )

            .join(
                Customer,
                Customer.id == SalesInvoice.customer_id
            )

            .filter(
                SalesInvoice.organization_id == organization_id
            )

            .order_by(
                SalesInvoice.created_at.desc()
            )

            .all()
        )

        return sales_rows
    

    @staticmethod
    def get_customer_ledger(
        db: Session,
        organization_id: int,
        customer_id: int
    ):

        ledger_rows = (
            db.query(
                SalesInvoice.created_at.label("date"),

                SalesInvoice.invoice_number,

                SalesInvoice.total_amount.label("debit")
            )

            .filter(
                SalesInvoice.organization_id == organization_id,
                SalesInvoice.customer_id == customer_id
            )

            .order_by(
                SalesInvoice.created_at.asc()
            )

            .all()
        )

        customer = (
            db.query(Customer)
            .filter(
                Customer.id == customer_id
            )
            .first()
        )

        return ledger_rows, customer
    

    @staticmethod
    def get_outstanding_receivables(
        db: Session,
        organization_id: int
    ):

        receivable_rows = (
            db.query(
                Customer.customer_name.label("customer_name"),

                SalesInvoice.id,

                SalesInvoice.due_amount
            )

            .join(
                Customer,
                Customer.id == SalesInvoice.customer_id
            )

            .filter(
                SalesInvoice.organization_id == organization_id,

                SalesInvoice.due_amount > 0
            )

            .all()
        )

        return receivable_rows
    

    @staticmethod
    def get_customer_aging(
        db: Session,
        organization_id: int
    ):

        aging_rows = (
            db.query(
                Customer.customer_name.label("customer_name"),

                SalesInvoice.due_amount,

                SalesInvoice.due_date
            )

            .join(
                Customer,
                Customer.id == SalesInvoice.customer_id
            )

            .filter(
                SalesInvoice.organization_id == organization_id,

                SalesInvoice.due_amount > 0
            )

            .all()
        )

        return aging_rows
    

    @staticmethod
    def get_profit_by_customer(
        db: Session,
        organization_id: int
    ):

        profit_rows = (
            db.query(
                Customer.customer_name.label("customer_name"),

                SalesInvoice.total_amount
            )

            .join(
                Customer,
                Customer.id == SalesInvoice.customer_id
            )

            .filter(
                SalesInvoice.organization_id == organization_id
            )

            .all()
        )

        return profit_rows
    
    @staticmethod
    def get_vendor_aging(
        db: Session,
        organization_id: int
    ):

        aging_rows = (
            db.query(
                Vendor.vendor_name.label("vendor_name"),

                Bill.total_amount,

                Bill.due_date
            )

            .join(
                Vendor,
                Vendor.id == Bill.vendor_id
            )

            .filter(
                Bill.organization_id == organization_id
            )

            .all()
        )

        return aging_rows
    

    @staticmethod
    def get_stock_summary(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                Product.id.label(
                    "product_id"
                ),

                Product.name.label(
                    "product_name"
                ),

                Product.current_stock.label(
                    "current_stock"
                )
            )

            .filter(
                Product.organization_id
                == organization_id
            )

            .all()
        )
    

    @staticmethod
    def get_low_stock_products(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                Product.id.label(
                    "product_id"
                ),

                Product.name.label(
                    "product_name"
                ),

                Product.current_stock.label(
                    "current_stock"
                ),

                Product.minimum_stock.label(
                    "minimum_stock"
                )
            )

            .filter(
                Product.organization_id
                == organization_id,

                Product.current_stock
                < Product.minimum_stock
            )

            .all()
        )
    


    @staticmethod
    def get_inventory_valuation(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                Product.id.label(
                    "product_id"
                ),

                Product.name.label(
                    "product_name"
                ),

                Product.current_stock.label(
                    "current_stock"
                ),

                Product.purchase_price.label(
                    "purchase_price"
                )
            )

            .filter(
                Product.organization_id
                == organization_id
            )

            .all()
        )
    @staticmethod
    def get_fast_moving_items(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                SalesInvoiceItem.item_name.label(
                    "product_name"
                ),

                func.sum(
                    SalesInvoiceItem.quantity
                ).label(
                    "total_quantity_sold"
                )
            )

            .join(
                SalesInvoice,

                SalesInvoice.id
                == SalesInvoiceItem.invoice_id
            )

            .filter(
                SalesInvoice.organization_id
                == organization_id
            )

            .group_by(
                SalesInvoiceItem.item_name
            )

            .order_by(
                func.sum(
                    SalesInvoiceItem.quantity
                ).desc()
            )

            .all()
        )
    @staticmethod
    def get_dead_stock_items(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                Product.id.label(
                    "product_id"
                ),

                Product.name.label(
                    "product_name"
                ),

                Product.current_stock.label(
                    "current_stock"
                ),

                func.max(
                    SalesInvoice.created_at
                ).label(
                    "last_sold_date"
                )
            )

            .outerjoin(
                SalesInvoiceItem,

                Product.id
                == SalesInvoiceItem.product_id
            )

            .outerjoin(
                SalesInvoice,

                SalesInvoice.id
                == SalesInvoiceItem.invoice_id
            )

            .filter(
                Product.organization_id
                == organization_id
            )

            .group_by(
                Product.id,
                Product.name,
                Product.current_stock
            )

            .all()
        )
    

    @staticmethod
    def get_warehouse_report(
        db: Session,
        organization_id: int
    ):

        return (

            db.query(

                Warehouse.id.label(
                    "warehouse_id"
                ),

                Warehouse.name.label(
                    "warehouse_name"
                ),

                func.count(
                    StockTransaction.product_id.distinct()
                ).label(
                    "total_products"
                ),

                func.sum(
                    StockTransaction.quantity
                ).label(
                    "total_stock"
                )
            )

            .join(
                StockTransaction,

                Warehouse.id
                == StockTransaction.warehouse_id
            )

            .filter(
                Warehouse.organization_id
                == organization_id
            )

            .group_by(
                Warehouse.id,
                Warehouse.name
            )

            .all()
        )
