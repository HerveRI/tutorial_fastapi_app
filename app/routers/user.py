from fastapi import status, Depends, HTTPException, APIRouter, Response
from .. import utils, schema, db_models
from ..database import get_db
from sqlalchemy.orm import Session 


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
async def create_user(info: schema.UserCreate, db: Session = Depends(get_db)):

    #hash password
    hashed_password = utils.hash(info.password)
    info.password = hashed_password
    new_user = db_models.Users(**info.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#path parameter id
@router.get("/users/{id}", response_model=schema.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.Users).filter(db_models.Users.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, [str(id)])
    # post = cursor.fetchone()

    #post = find_post(id)
    if not user:
        #response.status_code = 404
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")
    return  user