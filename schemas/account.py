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
    address: str

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
    address: Optional[str]

class staff(BaseModel):
    username:str
    email:str
    name:str
    gender:int
    

class login(BaseModel):
    username: str
    password: Optional[str]

class account(BaseModel):
    username: str
    idRole: int
    phone: Optional[str]
    email: Optional[str]
    name: Optional[str]
    address: Optional[str]

class verification(BaseModel):
    smsCode: Optional[str]
    emailCode: Optional[str]
    smsValid: bool
    emailValid: bool
    usernameValid: bool
    smsExpiration: Optional[float]
    emailExpiration: Optional[float]

class password(BaseModel):
    oldPassword: str
    newPassword: str
