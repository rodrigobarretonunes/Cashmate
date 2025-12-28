from fastapi import APIRouter, Request
from .auth_schemas import UserCreate, UserLogin, UserRead
from .auth_crud import create_user, login_user, verify_if_user_exists
from .auth_utils import get_current_user
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from core.database import get_db 
from core.security import get_password_hash
from api.share import get_pending_shared_transactions


router = APIRouter(prefix="/auth", tags=["auth"])


#Endpoint to register a new user

@router.post("/register",response_model=UserRead)
async def register_user(user:UserCreate, db: Session=Depends(get_db)):
    # verify if user already exists
    existing_user = verify_if_user_exists(db, user.username)
    if existing_user:
        raise HTTPException (status_code=400, detail='User already exists')
    # hash the password 
    hashed_password = get_password_hash(user.password)
    #register the user 
    new_user = await create_user(db, user, hashed_password)
    return new_user


@router.post("/login")
async def login_user_endpoint(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    token = await login_user(db, user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }