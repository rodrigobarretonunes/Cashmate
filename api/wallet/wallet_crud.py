from sqlalchemy.orm import Session
from sqlalchemy import select
from .wallet_models import TransactionDetail
from fastapi import HTTPException
from datetime import datetime, timezone,timedelta
import traceback


async def query_all_transactions(db: Session):
    try:
        stmt = select(TransactionDetail)
        user_transactions = db.execute(stmt).scalars().all()
        return user_transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def query_transaction_by_id(db: Session, transaction_id: int):
    try:
        stmt = select(TransactionDetail).where(TransactionDetail.id == transaction_id)
        selected_transaction = db.execute(stmt).scalars().first()
        return selected_transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def create_transaction_detail(db,new_transaction,user_id):
    try:
              
        db_transaction_detail= TransactionDetail(
        total_amount = new_transaction.total_amount,
        type = new_transaction.type,
        description = new_transaction.description,
        category = new_transaction.category,
        created_at = new_transaction.created_at,
        
        is_recurring = new_transaction.is_recurring,
        end_date = new_transaction.end_date,

        is_shared = new_transaction.is_shared,
        owner_id = user_id,
        owner_amount = new_transaction.owner_amount,

        counterparty_username = new_transaction.counterparty_username,
        counterparty_amount = new_transaction.counterparty_amount,
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=int(3)))
        db.add(db_transaction_detail)
        db.commit()
        db.refresh(db_transaction_detail)
        return db_transaction_detail
    except Exception as e:
        error_detail = f"Error creating transaction: {str(e)} | {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail) 

    

async def update_transaction(db:Session, db_transaction:TransactionDetail, updated_transaction:TransactionDetail):
    try:
        for var,value in vars(updated_transaction).items():
            setattr(db_transaction, var, value) if value else None
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)+"Something went wrong when editing transaction")

async def delete_transaction(db:Session, transaction_id:int):
    try:
        selected_transaction = query_transaction_by_id(db,transaction_id)
        if not selected_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        db.delete(selected_transaction)
        db.commit()
        return {"detail":"Transaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)+"Something went wrong when deleting transaction")


async def transaction_validation(new_transaction):
    try: 
        if not new_transaction.is_shared:
            new_transaction.owner_amount = new_transaction.total_amount
            return new_transaction
        if new_transaction.owner_amount + new_transaction.counterparty_amount != new_transaction.total_amount:
            raise HTTPException(status_code=422,detail="The sum of the parts does not match the total provided.")
        return new_transaction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)+"Something went wrong with amount validation") 


