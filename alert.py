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
import timer as timer
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
    float_price = 0.0
    floor = 0.0
    drop_alert = False
    ceiling = 0.0
    rise_alert = False
    stock = [raw, name, acronym, price, float_price, floor, ceiling]

    def __init__(self, raw_info, stock_name, stock_ack, stock_price, stock_int_price, stock_floor, stock_ceiling):
        self.raw = raw_info
        self.name = stock_name
        self.acronym = stock_ack
        self.price = stock_price
        self.int_price = stock_int_price
        self.floor = stock_floor
        self.ceiling = stock_ceiling
        self.stock = self.stock


class StockLibrary:

    StockNames = ["Charlie's Holdings Inc", "Oragenics Inc", "AstraZeneca plc"]
    StockAcronyms = ["CHUC", "OGEN", "AZN"]
    StockFloor = [0.12, 0.85, 40.00]
    StockCeiling = [0.20, 1.00, 45.00]

    def __init__(self):
        self.obj_Chuck = Stock("", self.StockNames[0], self.StockAcronyms[0], "", 0.0, self.StockFloor[0], self.StockCeiling[0])
        self.obj_Ogen = Stock("", self.StockNames[1], self.StockAcronyms[1], "", 0.0, self.StockFloor[1], self.StockCeiling[1])
        self.obj_Azn = Stock("", self.StockNames[2], self.StockAcronyms[2], "", 0.0, self.StockFloor[2], self.StockCeiling[2])


def send_email(subject, stock_info, email):

    from_address = email_address

    sender = email

    msg = MIMEMultipart()

    msg['From'] = sender

    msg['Subject'] = f"{subject}"

    body = stock_info

    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(from_address, password)

    text = msg.as_string()

    s.sendmail(from_address, recipient, text)

    s.quit()


def pull_stock_info(stock_acryonym):

    period = "."
    if period in stock_acryonym:
        return "null"
    else:
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
    else: # needed to format for no change, had to count periods
        count = 0
        for period in info_array[0]:
            if period == '.':
                count = count + 1
                if count >= 2:
                    price = info_array[0].split('.', 2)[0] + info_array[0].split('.')[1]
            else:
                print("Error")
                return info_array[0]

    return price


def compare_price(stock_price, low, high):

    current_price = float(stock_price)

    if current_price < low:
        return True
    if current_price > high:
        return True
    else:
        return False


def send_alert(raw_information, stock_price, stock_name):

    # Format Information
    formatted_email = f"\n{stock_name}: \n\n Price: " + stock_price + "Raw:\n\n: " + raw_information + "\n\n"

    subject_alert = f"{stock_name} HAS CHANGED"

    send_email(stock_name, formatted_email, recipient)


def search_for_alerts(stock1, stock2, stock3):

    library = StockLibrary()
    stockalert1 = compare_price(stock1.float_price, stock1.floor, stock1.ceiling)
    stockalert2 = compare_price(stock2.float_price, stock2.floor, stock2.ceiling)
    stockalert3 = compare_price(stock3.float_price, stock3.floor, stock3.ceiling)
    alerts = [stockalert1, stockalert2, stockalert3]

    while True:
        try:
            if alerts[0] == True:
                print("***Stock 1 has triggered an alert")
                send_alert(stock1.raw, stock1.price, stock1.name)
            if alerts[1] == True:
                print("***Stock 2 has triggered an alert")
                send_alert(stock2.raw, stock2.price, stock2.name)
            if alerts[2] == True:
                print("***Stock 3 has triggered an alert")
                send_alert(stock3.raw, stock3.price, stock3.name)
            else:
                print("No alerts were found")
                continue
        except:
             break


def main(stock1, stock2, stock3):

    # Pull raw Information by acronym & add to stock object
    raw_stock1 = pull_stock_info(stock1.acronym)
    stock1.raw = raw_stock1
    raw_stock2 = pull_stock_info(stock2.acronym)
    stock2.raw = raw_stock2
    raw_stock3 = pull_stock_info(stock3.acronym)
    stock3.raw = raw_stock3

    # Parse price from raw info and add to stock object
    stock1.price = get_price(stock1.raw)
    stock2.price = get_price(stock2.raw)
    stock3.price = get_price(stock3.raw)

    # Set/convert to integer price
    price_stock1 = float(stock1.price[0])
    stock1.int_price = float(price_stock1)
    price_stock2 = float(stock2.price[0])
    stock2.int_price = float(price_stock2)
    price_stock3 = float(stock3.price[0])
    stock3.int_price = float(price_stock3)

    return stock1, stock2, stock3


if __name__ == '__main__':

    # Stock library
    library = StockLibrary()

    while True:
        if keyboard.is_pressed("ENTER"):
            sys.exit(0)
        else:
            t0 = time.perf_counter()
            [stock1, stock2, stock3] = main(library.obj_Chuck, library.obj_Ogen, library.obj_Azn)
            search_for_alerts(stock1, stock2, stock3)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)






