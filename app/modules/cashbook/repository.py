from sqlalchemy.orm import Session

from app.modules.cashbook.model import (
    CashbookEntry
)

from app.modules.cashbook.schema import (
    CashbookEntryCreate,
    CashbookEntryUpdate,
)


def create_cashbook_entry_repo(
    db: Session,
    entry: CashbookEntryCreate,
    user_id: int
):
    last_entry = (
        db.query(CashbookEntry)
        .order_by(CashbookEntry.created_at.desc())
        .first()
    )

    if last_entry:

        last_number = int(
            last_entry.entry_code.replace("CB-", "")
        )

        new_entry_code = f"CB-{last_number + 1:04d}"

    else:
        new_entry_code = "CB-0001"

    new_entry = CashbookEntry(
        entry_code=new_entry_code,

        user_id=user_id,

        entry_type=entry.entry_type,

        amount=entry.amount,

        title=entry.title,

        notes=entry.notes,

        payment_method=entry.payment_method,

        transaction_date=entry.transaction_date,

        attachment_url=entry.attachment_url
    )

    db.add(new_entry)

    db.commit()

    db.refresh(new_entry)

    return new_entry


def get_all_cashbook_entries_repo(
    db: Session,
    skip: int,
    limit: int,
    user_id: int,
    start_date=None,
    end_date=None,
    transaction_date=None,
):
    query = db.query(CashbookEntry).filter(
    CashbookEntry.user_id == user_id
    )

    if transaction_date:
        query = query.filter(
            CashbookEntry.transaction_date == transaction_date
        )
    else:

        if start_date:
            query = query.filter(
                CashbookEntry.transaction_date >= start_date
            )

        if end_date:
            query = query.filter(
                CashbookEntry.transaction_date <= end_date
            )

    return (
        query
        .order_by(
            CashbookEntry.transaction_date.desc(),
            CashbookEntry.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_cashbook_entries_count_repo(
    db: Session,
    user_id: int,
    start_date=None,
    transaction_date=None,
    end_date=None
):
    query = db.query(CashbookEntry).filter(
    CashbookEntry.user_id == user_id
    )

    if transaction_date:
        query = query.filter(
            CashbookEntry.transaction_date == transaction_date
        )
    else:

        if start_date:
            query = query.filter(
                CashbookEntry.transaction_date >= start_date
            )

        if end_date:
            query = query.filter(
                CashbookEntry.transaction_date <= end_date
            )

    return query.count()


def get_cashbook_entry_by_code_repo(
    db: Session,
    entry_code: str,
    user_id: int
):
    return (
        db.query(CashbookEntry)
        .filter(
            CashbookEntry.entry_code == entry_code,
            CashbookEntry.user_id == user_id
        )
        .first()
    )


def delete_cashbook_entry_repo(
    db: Session,
    entry
):
    db.delete(entry)

    db.commit()

    return True


def update_cashbook_entry_repo(
    db: Session,
    entry,
    entry_update: CashbookEntryUpdate
):
    if entry_update.entry_type is not None:
        entry.entry_type = entry_update.entry_type

    if entry_update.amount is not None:
        entry.amount = entry_update.amount

    if entry_update.title is not None:
        entry.title = entry_update.title

    if entry_update.notes is not None:
        entry.notes = entry_update.notes

    if entry_update.payment_method is not None:
        entry.payment_method = entry_update.payment_method

    if entry_update.transaction_date is not None:
        entry.transaction_date = entry_update.transaction_date

    if entry_update.attachment_url is not None:
        entry.attachment_url = entry_update.attachment_url

    db.commit()

    db.refresh(entry)

    return entry