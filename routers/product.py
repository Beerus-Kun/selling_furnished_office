# from nis import cat
from fastapi import APIRouter, Depends, HTTPException, File
from schemas import product as ProductSC
# from schemas import account as AccountSC 
from model import product as ProductDB
from .extend import security, code
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
        # print(os.getenv('DROPBOX_TOKEN'))
        dbx = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))
        print(dbx.check_user)
        current = datetime.now()
        dbx.files_upload(file, f'/image/{current}.jpg', mode=dropbox.files.WriteMode("overwrite"))
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(f"/image/{current}.jpg")
        return {'code':204, 'url': shared_link_metadata.url.replace("dl=0", "raw=1")}
    except Exception as e:
        print(e)
        return {'code': 404}

@router.post('/category', dependencies=[Depends(security.validateStaff)])
async def addProduct(type:str, name:str):
    try:
        if type == 'Bàn':
            ProductDB.createCategory(2, code.standardized(name))
        if type == 'Ghế':
            ProductDB.createCategory(1, code.standardized(name))
        return {'code': 200}
    except Exception as e:
        print(e)
        return {'code': 404}

@router.post('/', dependencies=[Depends(security.validateStaff)])
async def addProduct(product: ProductSC.product):
    try:
        res = ProductDB.createProduct(product.id_category, code.standardized(product.name), product.description, product.quantity, product.listed_price, product.image)
        return {'code': 201}
    except Exception as e:
        print(e)
        return {'code': 404}
        

### put
@router.put('/rate')
async def filterProduct(idProduct:int,score:int,idBill:int):
    res = ProductDB.rateProduct(idProduct, score, idBill)
    # res = ProductDB.filterProduct(min-1, max+1, id_category)
    return {'code': 200, 'data':res}

@router.put('/delete/{id}', dependencies=[Depends(security.validateStaff)])
async def deleteProduct(id:int):
    res = ProductDB.deleteProduct(id)
    if res == -1:
        return {'code': 400}
    elif res == 1:
        return {'code': 200}
    # res = ProductDB.filterProduct(min-1, max+1, id_category)
    # return {'code': 200, 'data':res}


@router.put('/category/{id}', dependencies=[Depends(security.validateStaff)])
async def changeCategory(id:int, name:str, type: str):
    try:
        name = code.standardized(name)
        if type == 'Bàn':
            ProductDB.updateCategory(id, name, 2)
            # ProductDB.createCategory(2, name)
        if type == 'Ghế':
            ProductDB.updateCategory(id, name,1)
        # ProductDB.updateCategory(id, name)
        return {'code': 200}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put('/delete_category/{id}', dependencies=[Depends(security.validateStaff)])
async def changeCategory(id:int):
    try:
        # ProductDB.updateCategory(id, name)
        res = ProductDB.existCategory(id)
        if res == True:
            return {'code':400}
        else:
            ProductDB.deleteCategory(id)
            return {'code': 200}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.put('/{id}', dependencies=[Depends(security.validateStaff)])
async def changeProduct(id:int, product: ProductSC.product):
    try:
        ProductDB.updateProduct(id, product.id_category, code.standardized(product.name), product.description, product.quantity, product.listed_price, product.image)
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

@router.get('/staff/{idProduct}', dependencies=[Depends(security.validateStaff)])
async def getStaffProduct (idProduct: int):
    res = ProductDB.getStaffProduct(idProduct)
    return {'code': 200, 'data' : res[0]}

@router.get('/search')
async def searchProduct(id_category:int = None, name: str = None):
    name = code.standardized(name)
    arr_name = name.split(' ')
    something = ''
    for i in arr_name:
        # if i.lower() == 'bàn' or i.lower() == 'ghế':
        #     name = i + '%'
        # else:
        something += '%' + i + '%'

    # print(something)
    res = ProductDB.searchProduct(something, id_category)
    return {'code': 203, 'data':res}

@router.get('/filter')
async def filterProduct(min:int = 0,max:int = 1000000000,id_category:int = None):
    res = ProductDB.filterProduct(min-1, max+1, id_category)
    return {'code': 203, 'data':res}
### delete