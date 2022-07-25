from typing import Optional
from pydantic import BaseModel

class product(BaseModel):
    id_category: int
    name: str
    description: str
    quantity: int
    listed_price: int
    image: str