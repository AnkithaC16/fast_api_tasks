from pydantic import BaseModel, EmailStr
from typing import Optional, List



# Auth / token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True  # pydantic v2

class TodoBase(BaseModel):
    task: str
    done: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    task: Optional[str] = None
    done: Optional[bool] = None

class TodoOut(TodoBase):
    id: int
    class Config:
        orm_mode = True


