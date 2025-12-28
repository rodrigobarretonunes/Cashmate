from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from core.database import get_db
from api.auth import get_current_user
from api.share.share_crud import transaction_invite_create, get_pending_shared_transactions, accept_shared_transaction
from wallet.wallet_models import TransactionDetail
from api.share.share_schemas import TransactionInviteCreate, SharedTransactionResponse



router = APIRouter( prefix = "/share", tags=["share"])


