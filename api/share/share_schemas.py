from pydantic import BaseModel
from datetime import datetime




class InviteSharedTransactionRead(BaseModel):
    shared_transaction_id: int
    transaction_id: int
    shared_with_user_id: int
    shared_by_user_id: int
    created_at: datetime
    status: str

    model_config = {"from_attributes": True}