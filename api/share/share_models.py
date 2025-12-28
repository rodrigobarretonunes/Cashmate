from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime,Boolean
from sqlalchemy.orm import relationship
from core.database import Base


class InviteSharedTransaction(Base):
    __tablename__ = "Invites_Shared_Transactions"

    shared_transaction_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transaction_details.id"), nullable=False)
    shared_with_user_id = Column(Integer, nullable=False)
    shared_by_user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="pending")


