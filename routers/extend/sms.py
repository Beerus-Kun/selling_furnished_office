from twilio.rest import Client
import os

def send_sms(phonenumber:str, body: str):
    # Your Account SID from twilio.com/console  
    account_sid = os.getenv("SMS_ACCOUNT")
    # Your Auth Token from twilio.com/console
    auth_token  = os.getenv("SMS_PSW")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=phonenumber, 
        from_=os.getenv("SENDING_NUMBER"),
        body=body)

    print(message)