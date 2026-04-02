from jose import JWTError, jwt
from datetime import UTC, datetime, timedelta
from . import schema, database, db_models, config
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 


SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = config.settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    now_utc = datetime.now(UTC)
    expire = now_utc + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM )
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)

    except JWTError as e:
        print(f"The error: {e.args[0]}")
        raise credentials_exception
    
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
        )
    result_token = verify_access_token(token, credentials_exception)
    user = db.query(db_models.Users).filter(db_models.Users.id == int(result_token.id)).first()
    return user