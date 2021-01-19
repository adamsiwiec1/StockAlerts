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
import sys

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
    int_price = 0.0
    floor = 0.0
    ceiling = 0.0

    def __init__(self, raw_info, stock_name, stock_ack, stock_price, stock_int_price, stock_floor, stock_ceiling):
        self.raw = raw_info
        self.name = stock_name
        self.acronym = stock_ack
        self.price = stock_price
        self.int_price = stock_int_price
        self.floor = stock_floor
        self.ceiling = stock_ceiling


class StockLibrary:

    StockNames = ["Charlie's Holdings Inc", "Oragenics Inc", "AstraZeneca plc"]
    StockAcronyms = ["CHUC", "OGEN", "AZN"]
    StockFloor = [0.12, 0.85, 51.00]
    StockCeiling = [0.20, 1.00, 52.00]


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


def pull_stock_info(stock_acryonym):

    stock_name = stock_acryonym

    print("Pulling info for" + stock_acryonym)

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
    info_array = raw_info.rsplit(' ', 4)
    # price = info_array[0].rsplit('+', 1)

    plus = '+'
    minus = '-'
    period = "."

    if plus in info_array[0]:
        price = info_array[0].split('+')[0]
    if minus in info_array[0]:
       price = info_array[0].split('-')[0]
    else:
        if period in info_array[0]:
            price = info_array[0].split('.', 2)[0] + info_array[0].split('.')[1]

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


def search_for_alerts(stock1, stock2, stock3):

    # while loop, press enter to start script esc to stop
    print("Press Enter to start searching for alerts or Esc to exit: ")
    while True:
        try:
            if(keyboard.is_pressed('ENTER')):
                stockalert1 = compare_price(stock1.price, stock1.floor, stock1.ceiling)
                if stockalert1 == True:
                    send_alert(stock1.raw, stock1.price, stock1.name)
                stockalert2 = compare_price(stock2.price, stock2.floor, stock2.ceiling)
                if stockalert2 == True:
                    send_alert(stock2.raw, stock2.price, stock2.name)
                stockalert3 = compare_price(stock3.price, stock3.floor, stock3.ceiling)
                if stockalert3 == True:
                    send_alert(stock3.raw, stock3.price, stock3.name)
                else:
                    search_for_alerts(stock1, stock2, stock3)
                    continue
            if keyboard.is_pressed('Esc'):
                print("You pressed 'esc', now exiting the script.")
                sys.exit(0)
        except:
             break


def main():

    # Stock library
    stockLibrary = StockLibrary()
    obj_Chuck = Stock("", stockLibrary.StockNames[0], stockLibrary.StockAcronyms[0], "", 0.0, stockLibrary.StockFloor[0], stockLibrary.StockCeiling[0])
    obj_Ogen = Stock("", stockLibrary.StockNames[1], stockLibrary.StockAcronyms[1], "", 0.0, stockLibrary.StockFloor[1], stockLibrary.StockCeiling[1])
    obj_Azn = Stock("", stockLibrary.StockNames[2], stockLibrary.StockAcronyms[2], "", 0.0, stockLibrary.StockFloor[2], stockLibrary.StockCeiling[2])

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

    # Set/convert to integer price
    price_stock1 = int(obj_Chuck.price[0])
    obj_Chuck.int_price = int(price_stock1)
    price_stock2 = int(obj_Ogen.price[0])
    obj_Ogen.int_price = int(price_stock2)
    price_stock3 = int(obj_Azn.price[0])
    obj_Azn.int_price = int(price_stock3)

    return obj_Chuck, obj_Ogen, obj_Azn

if __name__ == '__main__':

    while True:
        [stock1, stock2, stock3] = main()
        search_for_alerts(stock1, stock2, stock3)





