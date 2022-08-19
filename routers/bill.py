from warnings import catch_warnings
from fastapi import APIRouter, Depends
import stripe, os
from schemas import bill as BillSC
from schemas import account as AccountSC
from model import bill as BillDB
from model import account as AccountDB
from .extend import security
from .extend import code as Code

ORDERED = 1
PAID = 2

router = APIRouter()

# post
@router.post('/coupon')
async def checkCoupon(code: BillSC.coupon):
    err, value = BillDB.checkCoupon(code.code)
    if err == -1:
        return {"code":400}
    elif err == 1:
        return {"code":200, "value":value}
    return

@router.post('/new_coupon', dependencies=[Depends(security.validateStaff)])
async def createCoupon(info: BillSC.new):
    code = Code.getCode()
    code = code.strip()
    print(code)
    BillDB.insertCoupon(code, info.month, info.value, info.amount)
    return {"code": 200, "coupon": code}

@router.post('/pay-by-card')
async def credit(bill: BillSC.checkout):
    stripe.api_key = os.getenv('SECRET_STRIPE')
    coupon = ''

    product = bill.product.split(',')
    int_product = [int(i) for i in product]
    amount = bill.amount.split(',')
    int_amout = [int(i) for i in amount]
    if bill.coupon != None:
        coupon = bill.coupon
    res = BillDB.check(int_product, int_amout, coupon)
    res = Code.str2list(res)

    if res[0] == '-1':
        return{'code':400, 'name':res[1], 'amount':res[2]}
    else:
        try:
            payment = stripe.PaymentIntent.create(
            amount=int(res[0]),
            currency="vnd",
            payment_method_types=["card"],
            )
        except (Exception) as e:
            print(e)
            return {'code':404}
        # print(payment)
        return {'code':200, 'secret':payment.get('client_secret'), 'id':payment.get('id')}

@router.post('/buy')
async def buy(bill: BillSC.checkout, account: AccountSC.account = Depends(security.validateBuy)):
    name = ''
    coupon = ''
    # price = 0
    if bill.coupon != None:
        coupon = bill.coupon

    product = bill.product.split(',')
    int_product = [int(i) for i in product]
    amount = bill.amount.split(',')
    int_amout = [int(i) for i in amount]

    if account.idRole == 3:
        name = account.name
    elif account.idRole == 4:
        insertTempCustomer = AccountDB.createTempCustomer(account.phone)
        name = bill.name

    if bill.isCredit:
        res = BillDB.buy(account.phone, name, account.email, bill.address, PAID, int_product, int_amout, coupon)
        
        res = Code.str2list(res)
        if res[0] == '-1':
            return{'code':400, 'name':res[1], 'amount':res[2]}
        else:
            return {'code': 200}
    else:
        res = BillDB.buy(account.phone, name, account.email, bill.address, ORDERED, int_product, int_amout, coupon)
        
        res = Code.str2list(res)
        if res[0] == '-1':
            return{'code':400, 'name':res[1], 'amount':res[2]}
        else:
            return {'code': 200}

@router.post('/check')
async def buy(bill: BillSC.checkout):
    coupon = ''

    product = bill.product.split(',')
    int_product = [int(i) for i in product]
    amount = bill.amount.split(',')
    int_amout = [int(i) for i in amount]
    if bill.coupon != None:
        coupon = bill.coupon
    res = BillDB.check(int_product, int_amout, coupon)
    res = Code.str2list(res)

    if res[0] == '-1':
        return{'code':400, 'name':res[1], 'amount':res[2]}
    else:
        return {'code': 200, 'amount': res[0]}

@router.get('/historyB')
async def historicBill(account: AccountSC.account = Depends(security.validateToken)):
    res = BillDB.histBill(account.phone)
    return {'code':200, 'data':res}

@router.get('/historyP', dependencies=[Depends(security.validateCustomer)])
async def historicProduct(id:str):
    # idBill = 31
    res = BillDB.histProductBill(id)
    return {'code':200, 'data':res}

@router.get('/bill-staus', dependencies=[Depends(security.validateStaff)])
async def listBill(status:int):
    res = BillDB.billStatus(status)

    return {'code':200, 'data':res}

@router.put('/cancel')
async def historicProduct(id:int, account: AccountSC.account = Depends(security.validateCustomer)):
    res = BillDB.customerCancel(id, account.phone)
    if res == -1:
        return {'code':400}
    else:
        return {'code':200}



@router.put('/force-cancel', dependencies=[Depends(security.validateStaff)])
async def listBill(id:int):
    res = BillDB.forceCancel(id)

    return {'code':200}

@router.put('/next-step', dependencies=[Depends(security.validateStaff)])
async def listBill(id:int):
    res = BillDB.nextStep(id)

    return {'code':200, 'data':res}