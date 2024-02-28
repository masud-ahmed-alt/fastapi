
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from .database import Base

#For Create Posts input
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


#For Create Users input
class UserCreate(BaseModel):
    email:EmailStr
    password:str

#For User response
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

#For Posts response
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner : UserOut
    class Config:
        from_attributes = True



    