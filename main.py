from fastapi import FastAPI, Body, Depends, HTTPException, status
from pydantic import BaseModel 
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

#https://github.com/pydantic/pydantic/issues/3320
#class BaseModel(PydanticBaseModel):
    #class Config:
        #arbitrary_types_allowed = True

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    

class UserBase(BaseModel):
    username: str
   
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/posts/{post_id}", tags=["Posts"], status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        HTTPException(status_code=404, detail="Post was not found")
    return post

@app.post("/posts/", tags=["Posts"], status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post was not found")
    db.delete(db_post)
    db.commit()

@app.post("/users/", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


        




