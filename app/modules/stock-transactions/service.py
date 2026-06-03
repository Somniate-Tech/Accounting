from sqlalchemy.orm import Session

from fastapi import HTTPException

from decimal import Decimal

from app.modules.customers.model import (
    Customer
)

from app.modules.sales_orders.model import (
    SalesOrder
)

from app.modules.inventory.products.model import (
    Product
)

from app.modules.inventory.stock_transactions.model import (
    StockTransaction
)

from app.modules.sales_invoices.schema import (
    SalesInvoiceCreate,
    SalesInvoiceUpdate
)

from app.modules.sales_invoices.repository import (
    create_sales_invoice_repo,
    get_all_sales_invoices_repo,
    get_total_sales_invoices_count_repo,
    get_sales_invoice_by_id_repo,
    update_sales_invoice_repo,
    delete_sales_invoice_repo
)


def create_sales_invoice_service(
    db: Session,
    invoice: SalesInvoiceCreate,
    organization_id: int,
    user_id: int
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == invoice.customer_id,
            Customer.organization_id == organization_id
        )
        .first()
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if invoice.sales_order_id:

        sales_order = (
            db.query(SalesOrder)
            .filter(
                SalesOrder.id == invoice.sales_order_id,
                SalesOrder.organization_id == organization_id
            )
            .first()
        )

        if not sales_order:

            raise HTTPException(
                status_code=404,
                detail="Sales Order not found"
            )

    # PRODUCT VALIDATION BEFORE CREATING INVOICE

    for item in invoice.items:

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.organization_id == organization_id
            )
            .first()
        )

        if not product:

            raise HTTPException(
                status_code=404,
                detail=f"Product not found for item {item.item_name}"
            )

        if product.current_stock < item.quantity:

            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

    # CREATE INVOICE

    created_invoice = create_sales_invoice_repo(
        db=db,
        invoice=invoice,
        organization_id=organization_id,
        user_id=user_id
    )

    # AUTOMATIC STOCK DEDUCTION

    for item in created_invoice.items:

        product = (
            db.query(Product)
            .filter(
                Product.id == item.product_id,
                Product.organization_id == organization_id
            )
            .first()
        )

        before_stock = Decimal(
            product.current_stock
        )

        quantity = Decimal(
            item.quantity
        )

        after_stock = (
            before_stock - quantity
        )

        product.current_stock = after_stock

        stock_transaction = StockTransaction(
            organization_id=organization_id,

            product_id=product.id,

            transaction_type="SALE",

            quantity=quantity,

            before_stock=before_stock,

            after_stock=after_stock,

            reference_type="SALES_INVOICE",

            reference_id=created_invoice.id,

            remarks=(
                f"Stock deducted from invoice "
                f"{created_invoice.invoice_number}"
            )
        )

        db.add(stock_transaction)

    db.commit()

    return created_invoice


def get_all_sales_invoices_service(
    db: Session,
    page: int,
    limit: int,
    organization_id: int
):

    skip = (page - 1) * limit

    invoices = get_all_sales_invoices_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_sales_invoices_count_repo(
        db=db,
        organization_id=organization_id
    )

    total_pages = (
        total + limit - 1
    ) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": invoices
    }


def get_single_sales_invoice_service(
    db: Session,
    invoice_id: int,
    organization_id: int
):

    invoice = get_sales_invoice_by_id_repo(
        db=db,
        invoice_id=invoice_id,
        organization_id=organization_id
    )

    if not invoice:

        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


def update_sales_invoice_service(
    db: Session,
    invoice_id: int,
    invoice_update: SalesInvoiceUpdate,
    organization_id: int
):

    invoice = get_sales_invoice_by_id_repo(
        db=db,
        invoice_id=invoice_id,
        organization_id=organization_id
    )

    if not invoice:

        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return update_sales_invoice_repo(
        db=db,
        invoice=invoice,
        invoice_update=invoice_update
    )


def delete_sales_invoice_service(
    db: Session,
    invoice_id: int,
    organization_id: int
):

    invoice = get_sales_invoice_by_id_repo(
        db=db,
        invoice_id=invoice_id,
        organization_id=organization_id
    )

    if not invoice:

        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    delete_sales_invoice_repo(
        db=db,
        invoice=invoice
    )

    return {
        "message": "Invoice deleted successfully"
    }