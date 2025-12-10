from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
import os 
import dotenv
from fastapi import HTTPException,Request,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import JWTError, jwt




dotenv.load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")




# Function to hash a password
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def get_password_hash(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


# Function to verify a password
def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)



# Function to create access token
def create_access_token(user_id: int, username: str, email: str):
    try:
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode = {
        "sub": str(user_id),
        "id": user_id,
        "username": username,
        "email": email,
        "exp": expire
        }    
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt  
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error creating access token: " + str(e))
    

def token_validation(request):
    token = request.headers.get("Authorization")
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
        )
