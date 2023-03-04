from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    user : str
    title : str
    content : str 
    create_date : datetime | None = None