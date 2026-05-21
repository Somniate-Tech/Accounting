from decimal import Decimal

from typing import Optional
from typing import List

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import model_validator


class JournalEntryLineSchema(BaseModel):

    account_id: int

    debit: Decimal = Decimal("0.00")

    credit: Decimal = Decimal("0.00")

    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_debit_credit(self):

        if self.debit < 0:

            raise ValueError(
                "Debit cannot be negative"
            )

        if self.credit < 0:

            raise ValueError(
                "Credit cannot be negative"
            )

        if self.debit > 0 and self.credit > 0:

            raise ValueError(
                "Both debit and credit cannot have values together"
            )

        if self.debit == 0 and self.credit == 0:

            raise ValueError(
                "Either debit or credit must be greater than zero"
            )

        return self


class CreateJournalEntrySchema(BaseModel):

    reference_type: Optional[str] = None

    reference_id: Optional[int] = None

    description: Optional[str] = None

    lines: List[JournalEntryLineSchema]

    @field_validator("lines")
    @classmethod
    def validate_lines(cls, value):

        if len(value) < 2:

            raise ValueError(
                "Journal entry must contain at least two lines"
            )

        return value

    @model_validator(mode="after")
    def validate_balanced_entry(self):

        total_debit = sum(
            line.debit for line in self.lines
        )

        total_credit = sum(
            line.credit for line in self.lines
        )

        if total_debit != total_credit:

            raise ValueError(
                "Total debit must equal total credit"
            )

        return self