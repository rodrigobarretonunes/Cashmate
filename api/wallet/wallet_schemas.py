from pydantic import BaseModel
from typing import Optional        
from datetime import datetime 



class TransactionRead(BaseModel):
    id: int
    owner_id : int 
    total_amount : float
    type : Optional [str]
    description : Optional [str]
    category : Optional [str]
    created_at : Optional [datetime]
    is_recurring : bool
    end_date : Optional [datetime]
    is_shared : bool
    counterparty_id : Optional [int]
    model_config = {"from_attributes": True}

class TransactionDetailsCreate(BaseModel):
    total_amount: float
    type: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None
    is_recurring: bool
    end_date: Optional[datetime] = None
    is_shared: bool
    owner_amount: Optional[float] = None
    counterparty_username: Optional[str] = None
    counterparty_amount: Optional[float] = None




class TransactionDetailsRead(BaseModel):
    id : int
    total_amount : float
    type : Optional [str]
    description : Optional [str]
    category : Optional [str]
    created_at : Optional [datetime]
    is_recurring : bool
    end_date : Optional [datetime]
    is_shared : bool
    owner_id : int
    owner_amount : float
    counterparty_username : Optional [str]
    counterparty_amount : Optional[float]
    expiration_time : Optional[datetime]
    model_config = {"from_attributes": True}




