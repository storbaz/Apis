from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    stripe_customer_id = Column(String(255), unique=True)
    stripe_subscription_id = Column(String(255), unique=True)
    stripe_price_id = Column(String(255))
    plan = Column(String(20), default="free", nullable=False)
    status = Column(String(20), default="active", nullable=False)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", backref="subscription")
