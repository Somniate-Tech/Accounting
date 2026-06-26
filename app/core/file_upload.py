import uuid
from pathlib import Path

from fastapi import (
    UploadFile,
    HTTPException
)
from app.core.config import settings

UPLOAD_DIR = Path(
    settings.UPLOAD_DIR
) / "documents"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


async def save_file(
    file: UploadFile
):

    extension = (
        Path(file.filename)
        .suffix
        .lower()
    )

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    file_path = (
        UPLOAD_DIR / filename
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)

    return (
        f"/uploads/documents/"
        f"{filename}"
    )