from fastapi import Depends, HTTPException, APIRouter, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schema, db_models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schema.Token)
async def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session =  Depends(get_db)):
    user = db.query(db_models.Users).filter(db_models.Users.email == creds.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    # Casting id to string considering pydantic model expect a string but user.id in of type int in table
    access_token = oauth2.create_access_token(data = {"user_id": str(user.id)})
    return {"access_token": access_token, "token_type" : "bearer"}