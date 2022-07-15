from fastapi import APIRouter, Depends
import jwt
from typing import Optional
import os
from ..schemas import account as SAccount 
from dotenv import load_dotenv
from .extend import security
load_dotenv()

router = APIRouter()

def generate_token(username: str, idRole: str) -> str:
    to_encode = {
        "idRole": idRole, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECURITY_ALGORITHM'))
    return encoded_jwt

@router.get('/sigin_up', dependencies=[Depends(security.validate_token)])
def signUp():
    return 'hello'