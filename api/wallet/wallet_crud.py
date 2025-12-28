from sqlalchemy.orm import Session
from sqlalchemy import select
from .wallet_models import TransactionDetail
from fastapi import HTTPException, Request
from datetime import datetime, timezone,timedelta
import traceback
from api.auth import get_current_user



async def query_all_transactions(request:Request, db: Session ):
    try:
        current_user = get_current_user(request,db)
        stmt = select(TransactionDetail).where(TransactionDetail.owner_id == current_user.id)
        user_transactions = db.execute(stmt).scalars().all()
        return user_transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def query_transaction_by_id(db: Session, transaction_id: int,request:Request):
    try:
        current_user= get_current_user(request,db)
        stmt = select(TransactionDetail).where(TransactionDetail.owner_id == current_user.user_id).where(id==transaction_id)
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

async def delete_transaction(db:Session, transactions_ids:list[int], request:Request):
    try:
        current_user = get_current_user(request,db)
        stmt = select(TransactionDetail).where(TransactionDetail.owner_id == current_user.id, TransactionDetail.id.in_(transactions_ids))
        selected_transaction = db.execute(stmt).scalars().all()
        if not selected_transaction:
            raise HTTPException(status_code=404, detail="Transactions not found")
        for t in selected_transaction:
            db.delete(t)
        db.commit()
        return {"detail":"Transaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)+"Something went wrong when deleting transaction")

async def transaction_validation(new_transaction, request=None, db=None):
    try:
        # Se não for compartilhada, só define owner_amount e counterparty_amount
        if not new_transaction.is_shared:
            new_transaction.owner_amount = new_transaction.total_amount
            new_transaction.counterparty_amount = 0
            new_transaction.counterparty_username = None
            return new_transaction
        if request and db:
            current_user = get_current_user(request, db)
            print (current_user.username)
            if current_user.username == new_transaction.counterparty_username:
                raise HTTPException(
                    status_code=422,
                    detail="You cannot create a shared transaction with yourself."
                )
        # Somatório deve bater com total
        if new_transaction.owner_amount + new_transaction.counterparty_amount != new_transaction.total_amount:
            raise HTTPException(
                status_code=422,
                detail="The sum of owner and counterparty amounts does not match the total provided."
            )

        # **Bloqueio de transação compartilhada consigo mesmo**
        

        return new_transaction

    except HTTPException:
        raise  # Re-raise exceptions já levantadas
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e) + " Something went wrong with transaction validation."
        )