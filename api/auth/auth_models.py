from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone 
from core.database import Base


# ========================
#       USERS
# ========================
class User(Base):
    __tablename__ = "users_table"
    id = Column(Integer, primary_key=True, index=True)
    email =  Column(String, unique=True, nullable=False,index=True)
    username = Column(String, unique=True,nullable=False,index=True)
    hashed_password = Column(String, nullable=True)
    balance = Column(Float,default=0.0)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
