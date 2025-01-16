from typing import Optional
from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime  
from typing_extensions import Annotated
  
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True 

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner: UserOut
    class Config:               # Since Post is a type of sqlalchemy model we use the pydantic orm to convert it to a pydantic model
        from_attributes = True  # orm_mode name is changed to from_attributes.

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:               
        from_attributes = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
    