from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Session
from sqlalchemy import select
from .share_models import InviteSharedTransaction
from fastapi import HTTPException
from core.utils_core import get_user_by_username,get_current_user
from fastapi import Request
from api.wallet import TransactionDetail
# Função responsavel por criar um convite de compartilhamento
def transaction_invite_create(db,new_transaction_detail):
    try:
        if not new_transaction_detail.counterparty_username:
            raise HTTPException(status_code=400, detail="Missing counterparty")
        counterparty = get_user_by_username(db,new_transaction_detail.counterparty_username)
        if not counterparty:
            raise HTTPException(status_code=404, detail="Counterparty not found")
        invite = InviteSharedTransaction(
            transaction_id =new_transaction_detail.id,
            shared_with_user_id = counterparty.id,
            shared_by_user_id = new_transaction_detail.owner_id,
            created_at = new_transaction_detail.created_at,
            status = "pending"
        )
        db.add(invite)
        db.commit()
        db.refresh(invite)
        return invite
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 # Função chamada em todo o login e na rota de dashboard para pegar as transações pendentes   
def get_pending_shared_transactions(db:Session, user_id:int):
    try: 
        stmt = select(InviteSharedTransaction).where(InviteSharedTransaction.shared_with_user_id == user_id, InviteSharedTransaction.status == 'pending')
        results = db.execute(stmt).scalars().all()
        return results 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Função que altera o status do convite 
def accept_shared_transaction(db:Session,shared_transaction_id: int):
    try:
        stmt = select(InviteSharedTransaction).where(InviteSharedTransaction.shared_transaction_id == shared_transaction_id)
        invite = db.execute(stmt).scalars().first()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        invite.status = 'accepted'
        db.commit()
        db.refresh(invite)
        stmt_transaction = select(TransactionDetail).where(TransactionDetail.id == invite.transaction_id, TransactionDetail.owner_id == invite.shared_by_user_id)
        shared_transaction = db.execute(stmt_transaction).scalars().first()
        if not shared_transaction:
            raise HTTPException(status_code=404, detail="Original transaction not found")
        return shared_transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

        


