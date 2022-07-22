from typing import Optional
from pydantic import BaseModel


class Hello(BaseModel):
    title: str
    content: str
    note: Optional[str]

class customerAccount(BaseModel):
    username: str
    password: str
    gender: int
    email: str
    phone: str
    name: str

class login(BaseModel):
    username: str
    password: str

class account(BaseModel):
    username: str
    idRole: int
    phone: Optional[str]
    email: Optional[str]
    name: Optional[str]
