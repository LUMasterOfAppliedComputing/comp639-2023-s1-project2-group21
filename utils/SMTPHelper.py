import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email details
from flask import session

sender_email = 'leon846666@gmail.com'
sender_password = 'iuchylrjfizaadpz'

# create message object
msg = MIMEMultipart()
msg['From'] = sender_email



def sentPasswordEmail(to):
    # establish connection with SMTP server
    msg['To'] = to
    msg['Subject'] = "Reset your password"
    msg.attach(MIMEText("<a href=http://localhost:5000/forgotPassword?key=%s> please click this to reset your password</a>"%(to), 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # enable encryption
        smtp.login(sender_email, sender_password)

        smtp.send_message(msg)
