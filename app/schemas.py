from pydantic import BaseModel, EmailStr, constr, ConfigDict
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostOut(BaseModel):
    id: int
    title: str 
    content: str
    published: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attribute = True)

class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool

class UserCreate(BaseModel):
    email: str
    password: constr(min_length = 6, max_length = 72)

class UserOut(BaseModel):
    id:int
    email: str
    created_at: datetime 
   
    class Config:
        from_attributes = True
     