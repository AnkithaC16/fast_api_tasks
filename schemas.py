from pydantic import BaseModel
from typing import Optional

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
