from decimal import Decimal
from datetime import date
from fastapi import (
    APIRouter,
    Depends,
    Query,
    UploadFile,
    File,
    Form
)
from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_user
)
from app.core.file_upload import save_file
from app.modules.cashbook.schema import (
    CashbookEntryCreate,
    CashbookEntryUpdate
)

from app.modules.cashbook.service import (
    create_cashbook_entry_service,
    get_all_cashbook_entries_service,
    get_cashbook_entry_by_code_service,
    delete_cashbook_entry_service,
    update_cashbook_entry_service,
    export_cashbook_pdf_service,
)

router = APIRouter(
    prefix="/cashbook",
    tags=["Cashbook"]
)

@router.post("/")
async def create_cashbook_entry(
    entry_type: str = Form(...),
    amount: Decimal = Form(...),
    title: str = Form(...),
    notes: str = Form(None),
    payment_method: str = Form(...),
    transaction_date: date = Form(...),
    attachment: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    attachment_url = None

    if attachment:
        attachment_url = await save_file(
            attachment
        )

    entry = CashbookEntryCreate(
        entry_type=entry_type,
        amount=amount,
        title=title,
        notes=notes,
        payment_method=payment_method,
        transaction_date=transaction_date,
        attachment_url=attachment_url
    )

    entry_data = create_cashbook_entry_service(
        db=db,
        entry=entry,
        user_id=current_user.id
    )

    return {
        "message": "Cashbook entry created successfully",
        "data": entry_data
    }

@router.get("/")
def get_cashbook_entries(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    transaction_date: Optional[date] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    entries = get_all_cashbook_entries_service(
        db=db,
        page=page,
        limit=limit,
        transaction_date=transaction_date,
        start_date=start_date,
        end_date=end_date,
        user_id=current_user.id
    )

    return entries

@router.get("/export/pdf")
def export_cashbook_pdf(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
        transaction_date: Optional[date] = Query(None),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
    ):
    path = export_cashbook_pdf_service(
        db=db,
        user_id=current_user.id,
        transaction_date=transaction_date,
        start_date=start_date,
        end_date=end_date
    )
    return {
        "message": "PDF Generated",
        "url": path
    }



@router.get("/{entry_code}")
def get_single_cashbook_entry(
    entry_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    entry = get_cashbook_entry_by_code_service(
        db=db,
        entry_code=entry_code,
        user_id=current_user.id
    )

    return entry    


@router.delete("/{entry_code}")
def delete_cashbook_entry(
    entry_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return delete_cashbook_entry_service(
        db=db,
        entry_code=entry_code,
        user_id=current_user.id
    )


@router.patch("/{entry_code}")
def update_cashbook_entry(
    entry_code: str,
    entry_update: CashbookEntryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_entry = update_cashbook_entry_service(
        db=db,
        entry_code=entry_code,
        entry_update=entry_update,
        user_id=current_user.id
    )

    return {
        "message": "Cashbook entry updated successfully",
        "data": updated_entry
    }

