

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.modules.vendors.model import Vendor
from app.modules.vendors.routes import router as vendor_router
from app.modules.auth.routes import router as auth_router

# Routers links
from app.modules.auth.routes import(
    router as auth_router
)
from app.modules.bills.routes import (
    router as bill_router
)
from app.modules.purchase_orders.routes import (
    router as purchase_order_router
)
from app.modules.cashbook.routes import (
    router as cashbook_router
)
from app.modules.customers.routes import(
    router as customers_router
)
from app.modules.quotations.routes import(
    router as quotations_router
)
from app.modules.sales_orders.routes import(
    router as sales_router
)
from app.modules.sales_invoices.routes import(
    router as sales_invoice_router
)
from app.modules.inventory.categories.routes import(
    router as categories_router
)
from app.modules.inventory.units.routes import (
    router as unit_router
)
from app.modules.inventory.products.routes import (
    router as products_router
)
from app.modules.inventory.stock_transactions.routes import (
    router as stock_transaction_router
)
from app.modules.inventory.warehouses.routes import(
    router as warehouse_router
)
from app.modules.accounting.chart_of_accounts.routes import (
    router as chart_of_accounts_router
)
from app.modules.accounting.journal_entries.routes import (
    router as journal_entries_router
)
from app.modules.accounting.general_ledger.routes import (
    router as general_ledger_router
)
from app.modules.reports.routes import(
    router as reports_router
)
from app.modules.customer_payments.routes import (
    router as customer_payment_router
)
from app.modules.vendor_payments.routes import (
    router as vendor_payment_router
)
from app.modules.subscriptions.plans.routes import (
    router as subscription_plan_router
)
from app.modules.subscriptions.organization_subscriptions.routes import(
    router as organization_subscription_router
)
from app.modules.subscriptions.features.routes import (
    router as feature_router
)
from app.modules.subscriptions.plan_features.routes import (
    router as plan_feature_router
)
from app.modules.admin.routes import (
    router as admin_router
)
from app.modules.subscriptions.subscription_payments.routes import (
    router as subscription_payment_router
)
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Accounting SaaS API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://192.168.1.14:5500",
        "http://192.168.1.14:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(auth_router)
app.include_router(vendor_router)
app.include_router(purchase_order_router)
app.include_router(bill_router)
app.include_router(cashbook_router)
app.include_router(customers_router)
app.include_router(quotations_router)
app.include_router(sales_router)
app.include_router(sales_invoice_router)
app.include_router(categories_router)
app.include_router(unit_router)
app.include_router(products_router)
app.include_router(stock_transaction_router)
app.include_router(warehouse_router)
app.include_router(chart_of_accounts_router)
app.include_router(journal_entries_router)
app.include_router(general_ledger_router)
app.include_router(reports_router)
app.include_router(customer_payment_router)
app.include_router(vendor_payment_router)
app.include_router(subscription_plan_router)
app.include_router(organization_subscription_router)
app.include_router(feature_router)
app.include_router(plan_feature_router)
app.include_router(admin_router)
app.include_router(subscription_payment_router)

@app.get("/")
def home():
    return {
        "message": "Accounting Backend Running Successfully"
    }