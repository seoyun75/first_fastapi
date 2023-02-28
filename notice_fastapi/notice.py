from pydantic import BaseModel
from datetime import datetime

class Notice(BaseModel):
    user : str
    title : str
    content : str 
    # create_date : datetime