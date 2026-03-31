from fastapi import status, Depends, HTTPException, APIRouter, Response
from typing import List, Optional
from .. import utils, schema, db_models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schema.PostResponse])
async def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
                     limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(db_models.Post).filter(db_models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # 
    # Need investigation consideering that current_user is set to int but returns object type
    # And to investigate how the str and int are getting mismatched?
    #  
    print(type(current_user))
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
async def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    new_post = db_models.Post(owner_id = current_user.id, **post.model_dump())
    #new_post = db_models.Post(title=post.title, content=post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Same as the RETURNING of sql - a way to return what we just posted
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # db_conn.commit()
    #return new_post
    print(type(current_user))
    return new_post

#path parameter id
@router.get("/{id}", response_model=schema.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(db_models.Post).filter(db_models.Post.id == id).first()
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, [str(id)])
    # post = cursor.fetchone()

    #post = find_post(id)
    if not post:
        #response.status_code = 404
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    post = post_query.first()
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, [str(id)])
    # deleted_post = cursor.fetchone()
    # db_conn.commit()
    #index = find_index_post(id)

    #if delete_post == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.PostResponse)
async def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    post_query = db.query(db_models.Post).filter(db_models.Post.id == id)
    existing_post = post_query.first()
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # db_conn.commit()
    #index = find_index_post(id)

    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # the **post.model_dump() not used -- LEARNING
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #post_dict = post.model_dump()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return post_query.first()