
from fastapi import APIRouter, Depends
from schemas import account as AccountSC 
from model import comment as CommentDB
from .extend import security, code

router = APIRouter()

@router.post('/{idProduct}')
def newComment(idProduct:int, account: AccountSC.account = Depends(security.validateToken), content:str = ""):
    CommentDB.insertComment(account.username, idProduct, code.standardized(content))
    return {'code':200}

@router.get('/{idProduct}')
def newComment(idProduct:int):
    # CommentDB.insertComment(account.username, idProduct, content)
    res = CommentDB.getComment(idProduct)
    return {'code':200, 'data': res}