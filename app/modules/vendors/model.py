from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

import uuid
import enum
from datetime import datetime

class VendorStatus(str, enum.Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    OVERDUE = "OVERDUE"


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    vendor_code = Column(String,unique=True,nullable=False)
    vendor_name = Column(String,nullable=False) 
    organization_id = Column(Integer,ForeignKey("organizations.id"))
    email = Column(String,unique=True)
    phone = Column(String,nullable=False)
    gst_number = Column(String,unique=True)
    city = Column(String)
    address = Column(Text)
    state = Column(String)
    pincode = Column(String)
    status = Column(Enum(VendorStatus), default=VendorStatus.UNPAID, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )