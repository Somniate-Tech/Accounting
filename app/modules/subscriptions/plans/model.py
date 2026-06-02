from sqlalchemy import Column, Integer, String, Boolean, Numeric
from app.core.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)

    description = Column(String)

    monthly_price = Column(Numeric(12, 2), default=0)
    yearly_price = Column(Numeric(12, 2), default=0)

    max_users = Column(Integer, default=1)
    max_customers = Column(Integer, default=0)
    max_vendors = Column(Integer, default=0)
    max_products = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)