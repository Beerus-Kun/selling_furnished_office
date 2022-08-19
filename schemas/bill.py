from typing import Optional
from pydantic import BaseModel

class coupon(BaseModel) :
    code: str


class new(BaseModel):
    # p_id_coupon text,
    month: int
    value: int
    amount: int

class checkout(BaseModel):
    name: Optional[str]
    address: str
    isCredit: bool
    product: str
    amount: str
    coupon: Optional[str]
    secret: Optional[str]