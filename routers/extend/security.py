from datetime import datetime

import jwt
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from dotenv import load_dotenv
load_dotenv()

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        if payload.get('username') < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )