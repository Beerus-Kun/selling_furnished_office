# from datetime import datetime
from fastapi import APIRouter, Depends
from schemas import account as AccountSC 
from model import static as StaticDB
from .extend import security, code
import calendar

router = APIRouter()

def num2date(num:int):
    return (2-len(str(num)))*'0'+ str(num)

@router.get('/month-turnover', dependencies=[Depends(security.validateAdmin)])
def getMonthTurnover(date):
    
    # getMonthTurnover
    days = calendar.monthrange(int(date[:4]), int(date[5:7]))[1]
    # print(days)
    current = 1
    final = []
    def addData(start, end):
        for i in range(start, end):
            ob ={}
            ob['date'] = num2date(i) + '/' + date[5:7] + '/' + date[:4]
            ob['sum'] = 0
            final.append(ob)

    
    res = StaticDB.monthTurnover(date)
    # print(res)
    for i in res:
        if int(i.get('date')[:2]) == current:
            current +=1
            final.append(i)
        else:
            addData(current, int(i.get('date')[:2]))
            final.append(i)
            current = int(i.get('date')[:2]) + 1

    if current < days:
        addData(current, days+1)

    lab = []
    data = []
    count = 0
    for i in final:
        if count % 5 == 0:
            lab.append(i.get('date'))
        else:
            lab.append('')
        count+=1
        data.append(i.get('sum')/1000000)
    return {'code':200, 'label':lab, 'data':data}

@router.get('/year-turnover', dependencies=[Depends(security.validateAdmin)])
def getYearTurnover(date):
    current = 1
    finaleMonth = 12
    final = []
    # getMonthTurnover

    def addData(start, end):
        for i in range(start, end):
            ob ={}
            ob['month'] = i
            ob['sum'] = 0
            final.append(ob)

    res = StaticDB.yearTurnover(date)
    for i in res:
        if int(i.get('month')) == current:
            current +=1
            final.append(i)
        else:
            addData(current, int(i.get('month')))
            final.append(i)
            current = int(i.get('month')) + 1

    if current < finaleMonth:
        addData(current, finaleMonth+1)

    lab = []
    data = []
    for i in final:
        lab.append(i.get('month'))
        data.append(i.get('sum')/1000000.0)
    return {'code':200, 'label':lab, 'data':data}
    # return {'code':200, 'data':final}

@router.get('/bill', dependencies=[Depends(security.validateAdmin)])
def getAdminBill(start, stop):
    res = StaticDB.getBoughtBill(start, stop)
    # print(res)
    return {'code':200, 'data':res}

@router.get('/total/bill', dependencies=[Depends(security.validateAdmin)])
def getAdminBill(start, stop):
    res = StaticDB.getTotalBill(start, stop)
    # print(res)
    return {'code':200, 'data':res}

@router.get('/month-status', dependencies=[Depends(security.validateAdmin)])
def getMonthStatus(date):
    res = StaticDB.monthStatus(date)
    return {'code':200, 'data':res}


@router.get('/admin-year', dependencies=[Depends(security.validateAdmin)])
def getAdminYear():
    res = StaticDB.adminYear()
    data = []
    for i in res:
        ob = {}
        ob['label'] = i.get('year')
        ob['value'] = str(i.get('year'))
        data.append(ob)

    return {'code':200, 'data':data}

@router.get('/admin-month', dependencies=[Depends(security.validateAdmin)])
def getAdminMonth(year:int):
    res = StaticDB.adminMonth(year)
    data = []
    for i in res:
        ob = {}
        ob['label'] = i.get('month')
        ob['value'] = num2date(i.get('month'))
        data.append(ob)
    return {'code':200, 'data':data}

@router.get('/total-month-turnover', dependencies=[Depends(security.validateAdmin)])
def getTotalMonthTurnover(date):
    res = StaticDB.totalMonthTurnover(date)
    return {'code':200, 'data':res}

@router.get('/total-year-turnover', dependencies=[Depends(security.validateAdmin)])
def getTotalYearTurnover(date):
    res = StaticDB.totalYearTurnover(date)
    return {'code':200, 'data':res}