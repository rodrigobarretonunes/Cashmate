from sqlalchemy.orm import Session 
from fastapi import HTTPException, Request
from sqlalchemy import select
from jose import JWTError, jwt
import os
from .security import SECRET_KEY, ALGORITHM




def get_current_user(request:Request, db:Session):
    from api.auth.auth_crud import get_user_by_id
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    try:
        token_type,token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = get_user_by_id(db, user_id=user_id)
        if user is None:
            print("User not found for ID:", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        print("Current user:", user.username, user.id)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token decode error")
    
    
def get_user_by_username(db:Session,counterparty_username):
    from api.auth.auth_models import User
    stmt = select(User).where(User.username == counterparty_username)
    counterparty = db.execute(stmt).scalars().first()
    return counterparty


