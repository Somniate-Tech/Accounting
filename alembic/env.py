from logging.config import fileConfig
 
from sqlalchemy import engine_from_config
from sqlalchemy import pool
 
from alembic import context

from app.core.database import Base

from app.core.config import settings
# =========================
# IMPORT ALL MODELS HERE
# =========================

from app.modules.users.model import User

from app.modules.organizations.model import Organization

from app.modules.organization_members.model import (
    OrganizationMember
)

from app.modules.vendors.model import Vendor

from app.modules.customers.model import Customer

from app.modules.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderItem
)

from app.modules.bills.model import (
    Bill,
    BillItem
)

from app.modules.cashbook.model import (
    CashbookEntry
)

from app.modules.quotations.model import (
    Quotation,
    QuotationItem
)

from app.modules.sales_orders.model import (
    SalesOrder,
    SalesOrderItem
)

from app.modules.sales_invoices.model import (
    SalesInvoice,
    SalesInvoiceItem
)

from app.modules.inventory.categories.model import (
    Category
)

from app.modules.inventory.units.model import (
    Unit
)

from app.modules.inventory.products.model import (
    Product
)

from app.modules.inventory.stock_transactions.model import (
    StockTransaction
)

from app.modules.inventory.warehouses.model import (
    Warehouse
)

from app.modules.accounting.chart_of_accounts.model import (
    ChartOfAccount
)

from app.modules.accounting.journal_entries.model import (
    JournalEntry,
    JournalEntryLine
)
from app.modules.subscriptions.plans.model import (
    SubscriptionPlan
)
from app.modules.customer_payments.model import(
    CustomerPayment
)
from app.modules.vendor_payments.model import(
    VendorPayment
)
from app.modules.subscriptions.organization_subscriptions.model import (
    OrganizationSubscription
)
from app.modules.subscriptions.features.model import (
    Feature
)
from app.modules.subscriptions.plan_features.model import (
    PlanFeature
)
from app.modules.subscriptions.subscription_payments.model import (
    SubscriptionPayment
)
# ALEMBIC CONFIG
# =========================

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# =========================
# TARGET METADATA
# =========================

target_metadata = Base.metadata

# DEBUG PRINT
# print(Base.metadata.tables.keys())


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )
 
    with context.begin_transaction():
        context.run_migrations()
 
 
def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """
    config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL
    )

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
 
    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
 
        with context.begin_transaction():
            context.run_migrations()
 
 
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
