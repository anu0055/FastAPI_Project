from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRETE_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exceptions
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=401, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exceptions=credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
        