from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Todo(BaseModel):
    title: str
    is_complete: bool

    class Config:
        orm_mode = True


class TodoResponse(Todo):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
