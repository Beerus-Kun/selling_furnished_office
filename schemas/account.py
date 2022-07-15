from typing import Optional
from pydantic import BaseModel


class Hello(BaseModel):
    title: str
    content: str
    note: Optional[str]

class registerAccount(BaseModel):
    username: str
    password: str
    repassword: str