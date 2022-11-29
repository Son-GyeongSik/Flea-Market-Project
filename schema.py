from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    id : Optional[int]
    name : str
    password : str
    user_type : int

    class Config:
        orm_mode = True

class ProductSchema(BaseModel):
    id : Optional[int]
    name : Optional[str]
    description : Optional[str]
    price : Optional[int]
    seller_id : Optional[int]
    buyer_id : Optional[int]

    class Config:
        orm_mode = True