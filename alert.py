import email
import smtplib
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import mime
import requests
from bs4 import BeautifulSoup
from requests import get

# file path - contained detailed info on stock - took out for now
file = r"\info.txt"
file_path = r"Z:\coding\scripts\StockAlerts\stock_info" + file

# email credentials
email_address = "stockalertsystem7@gmail.com"
password = "Alert12345!"
recipient = "stockalertsystem7@gmail.com"

# stocks
chuck = "chuc"
azn = "azn"
ogen = "ogen"


def send_email(stock_info, email):

    from_address = email_address

    sender = email

    msg = MIMEMultipart()

    msg['From'] = sender

    msg['Subject'] = "log"

    body = stock_info

    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(from_address, password)

    text = msg.as_string()

    s.sendmail(from_address, recipient, text)

    s.quit()


def pull_stock_info(stock):

    stock_name = stock

    yahoo = f"https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch"

    # Used to open a tab
    # webbrowser.open(yahoo)

    # Send HTTP Request
    page = requests.get(yahoo)

    # Pull HTTP from the request
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text

    return data


azn_info = pull_stock_info(azn)
azn_info_formatted = "\nAstraZenica: " + azn_info + "\n\n"
ogen_info = pull_stock_info(ogen)
ogen_info_formatted = "\nOragenics: " + ogen_info + "\n\n"
chuck_info = pull_stock_info(chuck)
chuck_info_formatted = "\nChuck: " + chuck_info + "\n\n"

send_email(azn_info_formatted, recipient)
send_email(ogen_info_formatted, recipient)
send_email(chuck_info_formatted, recipient)