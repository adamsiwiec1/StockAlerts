import email
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

# file path - contained detailed info on stock
file_path = r"Z:\coding\scripts\StockAlerts\stock_info"
file = r"\info.txt"

# email credentials
email_address = "keyloggerproject4@gmail.com"
password = "Keylogger12345!"
recipient = "keyloggerproject4@gmail.com"

# stocks
chuck = "chuc"
azn = "azn"
# noinspection SpellCheckingInspection
ogen = "ogen"


# def send_email(file_path, stock_information, attachment, to_address):
#
#
#
#     sender = email_address
#
#     msg = MIMEMultipart()
#
#     msg['From'] = sender
#
#     msg['Subject'] = "log"
#
#     body = alert.stock_information
#
#     msg.attach(MIMEText(body, 'plain'))
#
#     file = file_path
#     attachment = open(attachment, 'rb')
#
#     p = MIMEBase('application')
#
#     p.set_payload(attachment.read())
#
#     encoders.encode_base64(p)
#
#     p.add_header('Content-Disposition', "attatchment; filename %s" % file)
#
#     msg.attach(p)


def pull_stock_info(stock):

    stock_name = stock

    # Google URL
    url = f"https://www.google.com/search?&q={stock_name}"

    yahoo = f"https://finance.yahoo.com/quote/{stock_name}?p={stock_name}&.tsrc=fin-srch"

    # Used to open a tab
    webbrowser.open(yahoo)

    # Send HTTP Request
    page = requests.get(yahoo)

    # Pull HTTP from the request
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text

    print(data)


pull_stock_info(azn)
pull_stock_info(ogen)
pull_stock_info(chuck)
