from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session 
from core.database import get_db
from .wallet_schemas import TransactionDetailsCreate,TransactionDetailsRead
from .wallet_crud import create_transaction_detail, transaction_validation, query_all_transactions, query_transaction_by_id, update_transaction, delete_transaction
from core import token_validation,get_user_by_username,get_current_user
from api.auth import get_current_user


router = APIRouter(prefix='/transactions', tags=['transactions'])
@router.post("/all_transactions", response_model=list[TransactionDetailsRead])
async def get_transactions_endpoint(request, db: Session=Depends(get_db)):
    if not token_validation(request):
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        transactions = query_all_transactions(db=db)   
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transaction/create", response_model=TransactionDetailsRead)
async def create_transaction_endpoint(request: Request, transaction:TransactionDetailsCreate, db: Session=Depends(get_db)):
    if not token_validation(request):
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        new_transaction = await transaction_validation(transaction)
        user = get_current_user(request,db)
        if new_transaction.is_shared:
            counterparty = get_user_by_username(db,new_transaction.counterparty_username)
            if not counterparty:
                raise HTTPException(status_code=404, detail="Counterparty not found")
            new_transaction_detail = await create_transaction_detail(new_transaction=new_transaction,db=db,user_id=user.id)
            return new_transaction_detail
        new_transaction_detail = await create_transaction_detail(db=db,new_transaction=new_transaction,user_id=user.id)
        return new_transaction_detail
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.delete("/transaction/delete/{transaction_id}", response_model=dict)
async def delete_transaction_endpoint(request:Request, transaction_id:int, db:Session=Depends(get_db)):
    if not token_validation(request):
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        delete_transaction(db=db,transaction_id=transaction_id)  
        return {"detail":"Transaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.put("/transaction/update/{transaction_id}",response_model=TransactionDetailsRead)
async def update_transaction_endpoint(request,transaction_id:int,updated_transaction:TransactionDetailsCreate,db:Session=Depends(get_db)):
    if not token_validation(request):
        raise HTTPException(status_code=401, detail="Invalid token")
    try:
        db_transaction = query_transaction_by_id(db=db,transaction_id=transaction_id) 
        if not db_transaction:
            raise HTTPException(status_code=404,detail="Transaction not found")
        updated_transaction = update_transaction(db=db,db_transaction=db_transaction,updated_transaction=updated_transaction)  
        return updated_transaction
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
