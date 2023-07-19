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

# Get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello": "World"}

#@app.post("/users/", tags=["quotes_user"])
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()


        




