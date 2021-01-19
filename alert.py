import email
import smtplib
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

import keyboard as keyboard
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


class Stock:

    raw = ""
    name = ""
    acronym = ""
    price = ""
    int_price = int(price)
    floor = 0.0
    ceiling = 0.0

    def __init__(self,raw_info, stock_name, stock_ack, stock_price, stock_floor, stock_ceiling):
        self.raw = raw_info
        self.name = stock_name
        self.acronym = stock_ack
        self.price = stock_price
        self.floor =  stock_floor
        self.ceiling = stock_ceiling


class StockLibrary:

    StockNames = ["Charlie's Holdings Inc", "Oragenics Inc", "AstraZeneca plc"]
    StockAcronyms = ["CHUC","OGEN","AZN"]
    StockFloor = [0.12,0.85,51.00]
    StockCeiling = [0.20,1.00,52.00]

    StockArray = [StockNames,StockAcronyms,StockFloor,StockCeiling]


    def __int__(self):
        self.StockNames
        self.StockAcronyms
        self.StockFloor
        self.

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


def get_price(raw_info):

    # Parse out price from raw info
    info_array = raw_info.rsplit(' ', 5)
    price = info_array[0].rsplit('+', 1)

    return price


def compare_price(stock, low, high):

    data = pull_stock_info(stock)
    current_price = get_price(data)

    if current_price < low:
        send_alert(data, current_price)
        return True
    if current_price > high:
        send_alert(data, current_price)
        return True


def send_alert(raw_information, stock_price, stock_name):

    # Format Information
    formatted_email = f"\n{stock_name}: \n\n Price: " + stock_price + "Raw:\n\n: " + raw_information + "\n\n"

    send_email(formatted_email, recipient)


if __name__ == '__main__':

    # Stock library
    stockLibrary = StockLibrary()
    obj_Chuck = Stock(stockLibrary.StockNames[0],stockLibrary.StockAcronyms[0],stockLibrary.StockFloor[0],stockLibrary.StockCeiling[0])
    obj_Ogen = Stock(stockLibrary.StockNames[1],stockLibrary.StockAcronyms[1],stockLibrary.StockFloor[1],stockLibrary.StockCeiling[1])
    obj_Azn = Stock(stockLibrary.StockNames[2],stockLibrary.StockAcronyms[2],stockLibrary.StockFloor[2],stockLibrary.StockCeiling[2])

    # Pull raw Information by acronym & add to stock object
    rawInfo_Chuck = pull_stock_info(obj_Chuck.acronym)
    obj_Chuck.raw = rawInfo_Chuck
    rawInfo_Ogen = pull_stock_info(obj_Ogen.acronym)
    obj_Ogen.raw = rawInfo_Ogen
    rawInfo_Azn = pull_stock_info(obj_Azn.acronym)
    obj_Azn.raw = rawInfo_Azn

    # Parse price from raw info and add to stock object
    obj_Chuck.price = get_price(obj_Chuck.raw)
    obj_Ogen.price = get_price(obj_Ogen.raw)
    obj_Azn.price = get_price(obj_Azn.raw)

    # Escape sequence
    esc = keyboard.is_pressed('Esc')

    # while loop, press enter to start script esc to stop
    if keyboard.is_pressed('ENTER'):
        while not esc:
            stockAlert1 = compare_price(obj_Chuck.price, obj_Chuck.floor, obj_Chuck.ceiling)
            if stockAlert1 == True:
                send_alert(obj_Chuck.raw, obj_Chuck.price, obj_Chuck.name)
            else:
                continue
            stockAlert2 = compare_price(obj_Ogen.price, obj_Ogen.floor, obj_Ogen.ceiling)
            if stockAlert2 == True:
                send_alert(obj_Chuck.raw, obj_Chuck.price, obj_Chuck.name)
            else:
                continue
            stockAlert3 = compare_price(obj_Chuck.price, obj_Chuck.floor, obj_Chuck.ceiling)
            if stockAlert3 == True:
                send_alert(obj_Azn.raw, obj_Azn.price, obj_Azn.name)
            else:
                continue




