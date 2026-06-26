from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from decimal import Decimal

from app.modules.bills.model import (
    Bill,
    BillItem,
    BillPaymentStatus
)

from app.modules.bills.schema import (
    BillCreate,
    BillUpdate,
)

from app.modules.vendors.model import Vendor

from app.modules.purchase_orders.model import (
    PurchaseOrder
)


def get_all_bills_repo(
    db: Session,
    skip: int,
    limit: int,
    organization_id: int
):
    return (
        db.query(Bill)
        .options(
            joinedload(Bill.items),
            joinedload(Bill.vendor),
            joinedload(Bill.purchase_order)
        )
        .filter(
            Bill.organization_id == organization_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_bills_count_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(Bill)
        .filter(
            Bill.organization_id == organization_id
        )
        .count()
    )


def get_bill_by_code_repo(
    db: Session,
    bill_code: str,
    organization_id: int
):
    return (
        db.query(Bill)
        .options(
            joinedload(Bill.items),
            joinedload(Bill.vendor),
            joinedload(Bill.purchase_order)
        )
        .filter(
            Bill.bill_code == bill_code,
            Bill.organization_id == organization_id
        )
        .first()
    )


def create_bill_repo(
    db: Session,
    bill: BillCreate,
    organization_id: int
):
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == bill.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    purchase_order = None

    if bill.po_code:

        purchase_order = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.po_code == bill.po_code,
                PurchaseOrder.organization_id == organization_id
            )
            .first()
        )

    last_bill = (
        db.query(Bill)
        .order_by(Bill.created_at.desc())
        .first()
    )

    if last_bill:

        last_number = int(
            last_bill.bill_code.replace("BILL-", "")
        )

        new_bill_code = f"BILL-{last_number + 1:04d}"

    else:
        new_bill_code = "BILL-0001"

    subtotal = Decimal("0")
    total_tax = Decimal("0")

    for item in bill.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        subtotal += item_total
        total_tax += item_tax

    grand_total = subtotal + total_tax

    new_bill = Bill(
        bill_code=new_bill_code,

        vendor_id=vendor.id,

        purchase_order_id=(
            purchase_order.id
            if purchase_order
            else None
        ),

        organization_id=organization_id,

        invoice_number=bill.invoice_number,

        invoice_date=bill.invoice_date,
        due_date=bill.due_date,

        subtotal=subtotal,
        tax_amount=total_tax,
        total_amount=grand_total,

        paid_amount=Decimal("0"),
        due_amount=grand_total,
        payment_status=BillPaymentStatus.UNPAID,
        
        notes=bill.notes
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    for item in bill.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        final_total = item_total + item_tax

        new_item = BillItem(
            bill_id=new_bill.id,

            item_name=item.item_name,

            quantity=item.quantity,

            unit_price=item.unit_price,

            tax_percent=item.tax_percent,

            total=final_total
        )

        db.add(new_item)

    db.commit()
    db.refresh(new_bill)

    return new_bill


def delete_bill_repo(
    db: Session,
    bill
):
    db.delete(bill)
    db.commit()

    return True


def update_bill_repo(
    db: Session,
    bill,
    bill_update: BillUpdate,
    organization_id: int
):
    vendor = None

    if bill_update.vendor_code:

        vendor = (
            db.query(Vendor)
            .filter(
                Vendor.vendor_code == bill_update.vendor_code,
                Vendor.organization_id == organization_id
            )
            .first()
        )

    purchase_order = None

    if bill_update.po_code:

        purchase_order = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.po_code == bill_update.po_code,
                PurchaseOrder.organization_id == organization_id
            )
            .first()
        )

    subtotal = Decimal("0")
    total_tax = Decimal("0")
    grand_total = Decimal("0")

    if bill_update.items:

        for item in bill_update.items:

            item_total = (
                item.quantity * item.unit_price
            )

            item_tax = (
                item_total * item.tax_percent
            ) / Decimal("100")

            subtotal += item_total
            total_tax += item_tax

        grand_total = subtotal + total_tax

    if bill_update.vendor_code:
        bill.vendor_id = vendor.id

    if bill_update.po_code:
        bill.purchase_order_id = purchase_order.id

    if bill_update.invoice_number:
        bill.invoice_number = bill_update.invoice_number

    if bill_update.invoice_date:
        bill.invoice_date = bill_update.invoice_date

    if bill_update.due_date:
        bill.due_date = bill_update.due_date

    if bill_update.notes:
        bill.notes = bill_update.notes

    if bill_update.payment_status:
        bill.payment_status = bill_update.payment_status

    if bill_update.items:

        bill.subtotal = subtotal
        bill.tax_amount = total_tax
        bill.total_amount = grand_total

        db.query(BillItem).filter(
            BillItem.bill_id == bill.id
        ).delete()

        for item in bill_update.items:

            item_total = (
                item.quantity * item.unit_price
            )

            item_tax = (
                item_total * item.tax_percent
            ) / Decimal("100")

            final_total = item_total + item_tax

            new_item = BillItem(
                bill_id=bill.id,

                item_name=item.item_name,

                quantity=item.quantity,

                unit_price=item.unit_price,

                tax_percent=item.tax_percent,

                total=final_total
            )

            db.add(new_item)

    db.commit()
    db.refresh(bill)

    return bill