import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def sendEmail(receiver_address, Subject, mail_content):
    sender_address = os.getenv('GOOGLE_EMAIL')
    sender_pass = os.getenv('GOOGLE_PASS')

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = Subject  #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')