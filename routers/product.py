# from nis import cat
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, File
from schemas import product as ProductSC
# from schemas import account as AccountSC 
from model import product as ProductDB
from .extend import security
from datetime import datetime
import dropbox
import os

router = APIRouter()

# @router.patch('/password')
# def changePassword(password: AccountSC.password, account: AccountSC.account = Depends(security.validateToken)):
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.password.encode(), salt)
#     res = AccountDB.changePassword(account.username, hashed)
#     if res == -1:
#         return {'code':404}
#     else:
#         return {'code':200}

### post
# @router.post('/new', dependencies=[[Depends(security.validateStaff)]])
# def changeProduct():
#     return 

@router.post('/image', dependencies=[Depends(security.validateStaff)])
async def uploadImage(file: bytes = File()):
    try:
        dbx = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))
        current = datetime.now()
        dbx.files_upload(file, f'/image/{current}.jpg', mode=dropbox.files.WriteMode("overwrite"))
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/image/{current}.jpg")
        return {'code':204, 'url': shared_link_metadata.url}
    except Exception as e:
        print(e)
        return {'code': 404}

@router.post('/', dependencies=[Depends(security.validateStaff)])
async def addProduct(product: ProductSC.product):
    try:
        res = ProductDB.createProduct(product.id_category, product.name, product.description, product.quantity, product.listed_price, product.image)
        return {'code': 201}
    except Exception as e:
        print(e)
        return {'code': 404}

### put
@router.put('/{id}', dependencies=[Depends(security.validateStaff)])
def changeProduct(id:int, product: ProductSC.product):
    try:
        ProductDB.updateProduct(id, product.id_category, product.name, product.description, product.quantity, product.listed_price, product.image)
        return {'code': 200}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")
        

### patch

### get
@router.get('/category')
async def getCategory():
    err, res = ProductDB.getCategories()
    if err == 1:
        return {'code':203, 'data': res}
    else:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get('/all')
async def getProduct(id_category:int = None):
    res = ProductDB.getProduct(id_category)
    return {'code': 203, 'data':res}
### delete