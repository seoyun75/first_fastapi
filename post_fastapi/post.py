from pydantic import BaseModel
from datetime import datetime 
from typing import Optional

from sqlmodel import SQLModel, Field


class Post(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user : str
    title : str
    content : str 
    create_date : Optional[datetime] = None

class PostUpdate(BaseModel):
    user : str
    title : str
    content : str 

class PostCreate(BaseModel):
    id : Optional[int] = Field(default=None, primary_key=True)
    user : str
    title : str
    content : str 
    