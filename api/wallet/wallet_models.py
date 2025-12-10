from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone 
from core.database import Base



class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    id = Column(Integer, primary_key=True, index=True)
   

    total_amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)

    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    is_recurring = Column(Boolean, default=False, nullable=True)
    end_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_shared = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, nullable=False)
    owner_amount =Column(Float, nullable=True)
    counterparty_username = Column(String, nullable=True)
    counterparty_amount = Column(Float, nullable=True)
    expiration_time =  Column(DateTime,nullable=True)

