from datetime import datetime

import jwt
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from dotenv import load_dotenv
from model import account as AccountDB
from schemas import account as AccountSC
load_dotenv()

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validateToken(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        username = payload.get('username')
        idRole = int(payload.get('idRole') or 0)
        if username is None:
            raise HTTPException(status_code=403, detail="Token expired")
        if idRole == 3:
            res = AccountDB.getAccount(username)
            if res.get('err') is None or res.get('err') == -1:
                raise HTTPException(status_code=403, detail="Something went wrong!")
            else:
                return AccountSC.account(username=username, idRole=idRole, phone= res.get('phone'), email=res.get('email'), name=res.get('name'), address=res.get('addres'))
        return AccountSC.account(username = username, idRole = int(idRole))
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def validateAdmin(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        username = payload.get('username')
        idRole = int(payload.get('idRole') or 0)
        if username is None or idRole != 1:
            raise HTTPException(status_code=403, detail="Token expired")
        
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def validateStaff(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        username = payload.get('username')
        idRole = int(payload.get('idRole') or 0)
        if username is None or idRole != 2:
            raise HTTPException(status_code=403, detail="Token expired")
        else:
            return AccountSC.account(username = username, idRole = int(idRole))
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )


def validateCustomer(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        username = payload.get('username')
        idRole = int(payload.get('idRole') or 0)
        if username is None:
            raise HTTPException(status_code=403, detail="Token expired")
        if idRole == 3:
            res = AccountDB.getAccount(username)
            if res.get('err') is None or res.get('err') == -1:
                raise HTTPException(status_code=403, detail="Something went wrong!")
            else:
                return AccountSC.account(username=username, idRole=idRole, phone= res.get('phone'), email=res.get('email'), name=res.get('name'), address=res.get('addres'))
        else:
            raise HTTPException(status_code=403, detail="Role must be customer")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def validateBuy(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        # print(1)
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        username = payload.get('username')
        idRole = int(payload.get('idRole') or 0)
        if idRole == 3:
            # print(2)
            res = AccountDB.getAccount(username)
            if res.get('err') is None or res.get('err') == -1:
                raise HTTPException(status_code=403, detail="Something went wrong!")
            else:
                return AccountSC.account(username=username, idRole=idRole, phone= res.get('phone'), email=res.get('email'), name=res.get('name'))
        elif idRole == 4:
            # print(3)
            phone = payload.get('phone')
            email = payload.get('email')
            return AccountSC.account(username='', idRole=idRole, phone= phone, email=email, name='')
        else:
            raise HTTPException(status_code=403, detail="Role must be customer")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def validateVerification(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        if http_authorization_credentials.credentials == "new":
            return AccountSC.verification(
                smsValid=False, 
                emailValid=False, 
                usernameValid=False,
                emailExpiration=0,
                emailCode='',
                smsCode='',
                smsExpiration=0,
                )
        else:
            payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
            smsCode = payload.get('smsCode')
            emailCode = payload.get('emailCode')
            smsValid = bool(payload.get('smsValid'))
            emailValid = bool(payload.get('emailValid'))
            usernameValid = bool(payload.get('usernameValid'))
            # print(payload.get('smsExpiration'))
            smsExpiration = float(payload.get('smsExpiration'))
            emailExpiration = float(payload.get('emailExpiration'))
            return AccountSC.verification(
                smsCode=smsCode, 
                emailCode=emailCode, 
                smsValid=smsValid, 
                emailValid=emailValid,
                usernameValid=usernameValid, 
                smsExpiration=smsExpiration, 
                emailExpiration=emailExpiration
            )
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )


def validateResgiter(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        smsValid = bool(payload.get('smsValid'))
        emailValid = bool(payload.get('emailValid'))
        usernameValid = bool(payload.get('usernameValid'))
        if smsValid == False or emailValid == False or usernameValid == False:
            raise HTTPException(status_code=403, detail="Information must be valid")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

def validatePhone(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[os.getenv('SECURITY_ALGORITHM')])
        smsValid = bool(payload.get('smsValid'))
        emailValid = bool(payload.get('emailValid'))
        # usernameValid = bool(payload.get('usernameValid'))
        if smsValid == False:
            raise HTTPException(status_code=403, detail="Information must be valid")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )