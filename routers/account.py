import jwt, os, bcrypt, re, random, datetime
from fastapi import APIRouter, Depends
from schemas import account as AccountSC 
from model import account as AccountDB
from .extend import security, sms, gmail

router = APIRouter()

def generateToken(username: str, idRole: str) -> str:
    to_encode = {
        "idRole": idRole, "username": username
    }
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECURITY_ALGORITHM'))
    return encoded_jwt

def generateTempToken(phone: str, idRole: str, email: str) -> str:
    to_encode = {
        "idRole": idRole, "phone": phone, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECURITY_ALGORITHM'))
    return encoded_jwt

def genRegToken(smsCode: str, emailCode: str, smsValid: str, emailValid: bool, smsExpiration: float, emailExpiration: float, usernameValid: bool)-> str:
    # time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
    # time = datetime.datetime.timestamp(time)
    to_encode = {
        "emailCode": smsCode, 
        "smsCode": smsCode, 
        "emailCode": emailCode, 
        "smsValid": smsValid, 
        "emailValid": emailValid, 
        "smsExpiration": smsExpiration, 
        "emailExpiration": emailExpiration,
        "usernameValid": usernameValid
    }
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('SECURITY_ALGORITHM'))
    return encoded_jwt

### post
@router.post('/create_staff', dependencies=[Depends(security.validateAdmin)])
def createStaffAccount(staff: AccountSC.staff):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    isValid = re.fullmatch(regex, staff.email)
    if not isValid:
        return {'code':404}
    defaulPass = str(random.randint(0,999999))
    defaulPass = (6-len(defaulPass))*"0" + defaulPass
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(defaulPass.encode(), salt)
    err = AccountDB.createStaffAccount(staff.username, hashed, staff.name, staff.gender, staff.email)
    if err == -2 or err is None:
        return {'code':400}
    elif err == -1:
        return {'code':401}
    elif err == 0:
        return {'code':402}
    else:
        content = f'Nhân viên {staff.name} đã được cung cấp tài khoản. \nVới thông tin username: {staff.username} và password: {defaulPass}\nVui lòng đổi mật khẩu sau khi nhận tin nhắn này'
        gmail.sendEmail(staff.email, 'Tài khoản mới', content)
        return {'code':201}

@router.post('/forgot')
def forgotPassword(valid: AccountSC.valid, verification: AccountSC.verification = Depends(security.validateVerification), pw:str = ""):
    smsCodeV = verification.smsCode
    emailCodeV= verification.emailCode
    smsValidV= verification.smsValid
    emailValidV= verification.emailValid
    usernameValidV= verification.usernameValid
    smsExpirationV= verification.smsExpiration
    emailExpirationV= verification.emailExpiration

    if smsCodeV == "":
        res = AccountDB.getAccount(valid.username)
        if res.get('err') == -1:
            return {'code':400}
        elif res.get('id_role') == 2:
            req = AccountDB.getStaff(valid.username)
            smsCodeV = str(random.randint(0,999999))
            smsCodeV = (6-len(smsCodeV))*"0" + smsCodeV
            # send code
            # print(req.get('email'))
            gmail.sendEmail(req.get('email'), 'Mã xác nhận', 'Mã xác nhận '+ smsCodeV)
            time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
            smsExpirationV = datetime.datetime.timestamp(time)
            token = genRegToken(smsCodeV, emailCodeV, smsValidV, emailValidV, smsExpirationV, emailExpirationV, usernameValidV)
            return {'code':202, 'token': token}
        else:
            smsCodeV = str(random.randint(0,999999))
            smsCodeV = (6-len(smsCodeV))*"0" + smsCodeV
            # send code
            sms.send_sms('+84' + res.get['phone'], 'Mã xác nhận '+ smsCodeV)
            time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
            smsExpirationV = datetime.datetime.timestamp(time)
            token = genRegToken(smsCodeV, emailCodeV, smsValidV, emailValidV, smsExpirationV, emailExpirationV, usernameValidV)
            return {'code':202, 'token': token}
    else:
        time = datetime.datetime.now()
        time = datetime.datetime.timestamp(time)
        if valid.smsCode == verification.smsCode and time < verification.smsExpiration:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pw.encode(), salt)
            err = AccountDB.changePassword(valid.username, hashed)
            print(err)
            return {'code':200}
        else:
            return {'code': 406}
    
    
    # salt = bcrypt.gensalt()
    # hashed = bcrypt.hashpw(staff.password.encode(), salt)
    # err = AccountDB.createStaffAccount(staff.username, hashed)
    # if err == -2 or err is None:
    #     return {'code':400}
    # elif err == -1:
    #     return {'code':401}
    # elif err == 0:
    #     return {'code':402}
    # else:
    #     # token = generateToken(idRole=3, username=account.username)
    #     return {'code':201}

@router.post('/check-phone-email')
def verifyPhoneEmail(valid: AccountSC.valid, verification: AccountSC.verification = Depends(security.validateVerification)):
    smsCodeV = verification.smsCode
    emailCodeV= verification.emailCode
    smsValidV= verification.smsValid
    emailValidV= verification.emailValid
    usernameValidV= verification.usernameValid
    smsExpirationV= verification.smsExpiration
    emailExpirationV= verification.emailExpiration
    if valid.smsState == 1:
        isValid = re.search("^0+(32|33|34|35|36|37|38|39|52|56|58|59|70|76|77|78|79|81|82|83|84|85|86|87|88|89|90|91|92|93|94|96|97|98|99)+([0-9]{7})", valid.phone)
        if isValid:
            smsCodeV = str(random.randint(0,999999))
            smsCodeV = (6-len(smsCodeV))*"0" + smsCodeV
                # send code
            sms.send_sms('+84' + valid.phone[1:], 'Mã xác nhận '+ smsCodeV)
            time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
            smsExpirationV = datetime.datetime.timestamp(time)
        else:
            return {'code': 405}

    elif valid.smsState == 2:
        time = datetime.datetime.now()
        time = datetime.datetime.timestamp(time)
        if valid.smsCode == verification.smsCode and time < verification.smsExpiration:
            smsValidV = True
        else:
            return {'code': 406}

    if valid.emailState == 1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        isValid = re.fullmatch(regex, valid.email)
        if isValid:
            emailCodeV = str(random.randint(0,999999))
            emailCodeV = (6-len(emailCodeV))*"0" + emailCodeV
            # send code
            gmail.sendEmail(valid.email, 'Xác thực tài khoản', 'Mã xác nhận '+ emailCodeV)
            time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
            emailExpirationV = datetime.datetime.timestamp(time)
                
        else:
            return {'code': 405}
            
    elif valid.emailState == 2:
        time = datetime.datetime.now()
        time = datetime.datetime.timestamp(time)
        if valid.emailCode == verification.emailCode and verification.emailExpiration > time:
            emailValidV = True
        else:
            return {'code': 406}

    if smsValidV and emailValidV:
        create = AccountDB.createTempCustomer(valid.phone)
        token = generateTempToken(valid.phone, 4, valid.email)
        return {'code':202, 'token': token}

    token = genRegToken(smsCodeV, emailCodeV, smsValidV, emailValidV, smsExpirationV, emailExpirationV, usernameValidV)
    return {'code':202, 'token': token}

    

@router.post('/register')
def receiveInformation(valid: AccountSC.valid, verification: AccountSC.verification = Depends(security.validateVerification)):
    # time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
    # time = datetime.datetime.timestamp(time)
    smsCodeV = verification.smsCode
    emailCodeV= verification.emailCode
    smsValidV= verification.smsValid
    emailValidV= verification.emailValid
    usernameValidV= verification.usernameValid
    smsExpirationV= verification.smsExpiration
    emailExpirationV= verification.emailExpiration

    if valid.smsState == 0:
        isValid = re.search("0+(32|33|34|35|36|37|38|39|52|56|58|59|70|76|77|78|79|81|82|83|84|85|86|87|88|89|90|91|92|93|94|96|97|98|99)+([0-9]{7})", valid.phone)
        if isValid:
            hasPhone = AccountDB.checkPhone(valid.phone)
            if hasPhone == -1:
                return {'code': 402}
        else:
            return {'code': 405}
        return {'code':200}
                
    
    if valid.emailState == 0:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        isValid = re.fullmatch(regex, valid.email)
        if isValid:
            hasEmail = AccountDB.checkEmail(valid.email)
            if hasEmail == -1:
                return {'code': 402}
        else:
            return {'code': 405}
        return {'code':200}


    if valid.smsState == 1:
        isValid = re.search("0+(32|33|34|35|36|37|38|39|52|56|58|59|70|76|77|78|79|81|82|83|84|85|86|87|88|89|90|91|92|93|94|96|97|98|99)+([0-9]{7})", valid.phone)
        if isValid:
            hasPhone = AccountDB.checkPhone(valid.phone)
            if hasPhone == -1:
                return {'code': 402}
            elif hasPhone == 1:
                smsCodeV = str(random.randint(0,999999))
                smsCodeV = (6-len(smsCodeV))*"0" + smsCodeV
                # send code
                sms.send_sms('+84' + valid.phone[1:], 'Mã xác nhận '+ smsCodeV)
                time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
                smsExpirationV = datetime.datetime.timestamp(time)
        else:
            return {'code': 405}
            
    elif valid.smsState == 2:
        time = datetime.datetime.now()
        time = datetime.datetime.timestamp(time)
        # print(valid.smsCode)
        # print(verification.smsCode)
        # print(verification.smsExpiration > time)
        if valid.smsCode == verification.smsCode and time < verification.smsExpiration:
            smsValidV = True
        else:
            return {'code': 406}
    
    if verification.usernameValid == False and valid.username !=None:
        hasUsername = AccountDB.checkUsername(valid.username)
        if hasUsername == -1:
            return {'code': 401}
        elif hasUsername == 1:
            usernameValidV = True
    
    if valid.emailState == 1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        isValid = re.fullmatch(regex, valid.email)
        if isValid:
            hasEmail = AccountDB.checkEmail(valid.email)
            if hasEmail == -1:
                return {'code': 402}
            elif hasEmail == 1:
                emailCodeV = str(random.randint(0,999999))
                emailCodeV = (6-len(emailCodeV))*"0" + emailCodeV
                # send code
                gmail.sendEmail(valid.email, 'Xác thực tài khoản', 'Mã xác nhận '+ emailCodeV)
                time = datetime.datetime.now() + datetime.timedelta(minutes = 20)
                emailExpirationV = datetime.datetime.timestamp(time)
        else:
            return {'code': 405}
            
    elif valid.emailState == 2:
        time = datetime.datetime.now()
        time = datetime.datetime.timestamp(time)
        if valid.emailCode == verification.emailCode and verification.emailExpiration > time:
            emailValidV = True
        else:
            return {'code': 406}

    token = genRegToken(smsCodeV, emailCodeV, smsValidV, emailValidV, smsExpirationV, emailExpirationV, usernameValidV)
    return {'code':202, 'token': token}

@router.post('/sign_up', dependencies=[Depends(security.validateResgiter)])
def createCustomerAccount(account: AccountSC.customerAccount):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(account.password.encode(), salt)
    err = AccountDB.createCustomerAccount(account.username, hashed, account.name, account.gender, account.email, account.phone, account.address)
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
        if res.get('password') == None:
            return {'code':403}
        if bcrypt.checkpw(account.password.encode(), res.get('password').encode()):
            acc = AccountDB.getAccount(account.username)
            token = generateToken(idRole=acc.get('id_role'), username=account.username)
            return {'code':202, 'token':token}
        else:
            return {'code':403}

### put
@router.put('/info', dependencies=[Depends(security.validateCustomer)])
def changeInformation(account: AccountSC.updateCustomer):
    res = AccountDB.changeInfo(account.phone, account.name, account.gender, account.email)
    if res == -1:
        return {'code':404}
    elif res == 0:
        return {'code':402}
    else:
        return {'code':202}

### patch
@router.put('/password')
def changePassword(password: AccountSC.password, account: AccountSC.account = Depends(security.validateToken)):
    res = AccountDB.getPassword(account.username)
    if res.get('err') == -1:
        return {'code':404}
    else:
        if bcrypt.checkpw(password.oldPassword.encode(), res.get('password').encode()):
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.newPassword.encode(), salt)
            res = AccountDB.changePassword(account.username, hashed)
            if res == -1:
                return {'code':404}
            else:
                return {'code':200}
        else:
            return {'code':404}
    
@router.put('/staff', dependencies=[Depends(security.validateAdmin)])
def createStaffAccount(staff: AccountSC.staff):
    AccountDB.updateStaff(staff.name, staff.gender, staff.email)
    return {'code':200}

@router.put('/delete_staff', dependencies=[Depends(security.validateAdmin)])
def createStaffAccount(staff: AccountSC.staff):
    AccountDB.deleteStaff(staff.username)
    return {'code':200}

@router.put('/restore_staff', dependencies=[Depends(security.validateAdmin)])
def createStaffAccount(staff: AccountSC.staff):
    # defaulPass = '123456'
    defaulPass = str(random.randint(0,999999))
    defaulPass = (6-len(defaulPass))*"0" + defaulPass
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(defaulPass.encode(), salt)
    # print(staff.username)
    AccountDB.restoreStaffAccount(staff.username, hashed)
    content = f'Nhân viên {staff.name} đã được khôi phục tài khoản. \nVới username: {staff.username} và password: {defaulPass}\nVui lòng đổi mật khẩu sau khi nhận tin nhắn này'
    # send code
    # send account
    gmail.sendEmail(staff.email, 'Tài khoản mới', content)
    print(content)
    return {'code':200}

### get
@router.get('/info')
def getInformation(account: AccountSC.account = Depends(security.validateToken)):
    return account.dict()

@router.get('/staff')
def getInformation(account: AccountSC.account = Depends(security.validateAdmin)):
    res = AccountDB.selectStaff()
    return {'code':200, 'data':res}

@router.get('/status', dependencies=[Depends(security.validateAdmin)])
def getInformation(username: str):
    res = AccountDB.statusStaff(username)
    return {'code':200, 'data':res}
