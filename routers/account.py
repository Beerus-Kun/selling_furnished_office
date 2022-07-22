from fastapi import APIRouter, Depends
import jwt
import os
import bcrypt
from schemas import account as AccountSC 
from model import account as AccountDB
from dotenv import load_dotenv
from .extend import security
load_dotenv()

router = APIRouter()

def generateToken(username: str, idRole: str) -> str:
    to_encode = {
        "idRole": idRole, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECURITY_ALGORITHM'))
    return encoded_jwt

# @router.get('/sigin_up', dependencies=[Depends(security.validate_token)])
# def signUp():
#     return 'hello'

@router.post('/create_staff', dependencies=[Depends(security.validate_admin)])
def createStaffAccount(staff: AccountSC.login):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(staff.password.encode(), salt)
    err = AccountDB.createStaffAccount(staff.username, hashed)
    if err == -2 or err is None:
        return {'code':400}
    elif err == -1:
        return {'code':401}
    elif err == 0:
        return {'code':402}
    else:
        # token = generateToken(idRole=3, username=account.username)
        return {'code':201}

@router.post('/sign_up')
def createCustomerAccount(account: AccountSC.customerAccount):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(account.password.encode(), salt)
    err = AccountDB.createCustomerAccount(account.username, hashed, account.name, account.gender, account.email, account.phone)
    if err == -2 or err is None:
        return {'code':400}
    elif err == -1:
        return {'code':401}
    elif err == 0:
        return {'code':402}
    else:
        token = generateToken(idRole=3, username=account.username)
        return {'code':202, 'token':token}

@router.post('/sign_in')
def login(account: AccountSC.login):
    res = AccountDB.getPassword(account.username)
    if res.get('err') == -1:
        return {'code':403}
    else:
        if bcrypt.checkpw(account.password.encode(), res.get('password').encode()):
            acc = AccountDB.getAccount(account.username)
            token = generateToken(idRole=acc.get('id_role'), username=account.username)
            return {'code':202, 'token':token}
        else:
            return {'code':403}


@router.get('/info')
def getInformation(account: AccountSC.account = Depends(security.validate_token)):
    return account.dict()
