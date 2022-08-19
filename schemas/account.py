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

class valid(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    smsCode: Optional[str]
    emailCode: Optional[str]
    smsState: Optional[int]
    emailState: Optional[int]
    username: Optional[str]

class updateCustomer(BaseModel):
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

class verification(BaseModel):
    smsCode: Optional[str]
    emailCode: Optional[str]
    smsValid: bool
    emailValid: bool
    usernameValid: bool
    smsExpiration: Optional[float]
    emailExpiration: Optional[float]

class password(BaseModel):
    password: str
