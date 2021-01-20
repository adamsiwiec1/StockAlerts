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

# email credentials
email_address = "keyloggerproject4@gmail.com"
password = "Keylogger12345!"
recipient = "keyloggerproject4@gmail.com"


class Stock(object):

    def __init__(self, raw, name, acronym, price, float_price, floor, ceiling):
        self.raw = raw,
        self.name = name
        self.acronym = acronym
        self.price = price
        self.float_price = float_price
        self.floor = floor
        self.ceiling = ceiling
        self.stock = [self.raw, self.name, self.acronym, self.price, self.float_price, self.floor, self.ceiling]


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

    print("Pulling info for " + stock_acryonym)

    yahoo = f"https://finance.yahoo.com/quote/{stock_acryonym}?p={stock_acryonym}&.tsrc=fin-srch"

    # Send HTTP Request
    page = requests.get(yahoo)

    # Pull HTTP from the request
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text

    return data


def get_price(stock_info):

    plus = '+'
    minus = '-'
    period = "."

    # Account for different format when market is closed or open
    if 'close' in stock_info:
        info_array = stock_info.rsplit(' ', 5)
    if 'open' in stock_info:
        info_array = stock_info.rsplit(' ', 8)

    # Account for different format when stock is up/down
    if plus in info_array[0]:
        price = info_array[0].split('+')[0]
    elif minus in info_array[0]:
        price = info_array[0].split('-')[0]
    else:
        count = 0
        for period in info_array[0]:
            if period == '.':
                count = count + 1
                if count >= 2:
                    price = info_array[0].split('.', 2)[0] + info_array[0].split('.')[1]
            else:
                print("Error")
                return "0.00"
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

    formatted_email = f"\n{stock_name}: \n\n Price: " + stock_price + "Raw:\n\n: " + raw_information + "\n\n"

    subject_alert = f"{stock_name} HAS CHANGED"

    send_email(subject_alert, formatted_email, recipient)


def search_for_alerts(stocks):

    count = len(stocks)
    alerts = []
    for num in range(count):
        alerts.append(compare_price(stocks[num].float_price, stocks[num].floor, stocks[num].ceiling))

    for num in range(count):
        if alerts[num]:
            print(f"*****{stocks[num].name} has triggered an alert*****")
            send_alert(stocks[num].raw, stocks[num].price, stocks[num].name)
        else:
            print("No alerts were found")


def main(stocks):
    count = len(stocks)
    raw_stock = []
    price_stock = []

    for num in range(count):
        raw_stock.append(pull_stock_info(stocks[num].acronym))

    for num in range(count):
        price_stock.append(get_price(raw_stock[num]))

    for num in range(count):
        stocks[num].raw = raw_stock[num]
        stocks[num].price = price_stock[num]
        stocks[num].float_price = float(price_stock[num])

    return stocks


if __name__ == '__main__':

    stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0) for i in range(6)]
    stockObjects[0] = Stock("", "Charlie's Holdings Inc", "CHUC", "", 0.00, 0.01, 0.02)
    stockObjects[1] = Stock("", "Oragenics Inc", "OGEN", "", 0.00, 1.10, 1.15)
    stockObjects[2] = Stock("", "AstraZeneca plc", "AZN", "", 0.00, 52.00, 60.00)
    stockObjects[3] = Stock("", "CloudCommerce", "CLWD" , "", 0.00, 0.081, 0.15)
    stockObjects[4] = Stock("", "Transport&Logs", "TLSS" , "", 0.00, 0.07, 0.12)
    stockObjects[5] = Stock("", "Plyzer Tech", "PLYZ" , "", 0.00, 0.0016, 0.0070)



    while True:
        if keyboard.is_pressed("ENTER"):
            sys.exit(0)
        else:
            t0 = time.perf_counter()
            stockArray = main(stockObjects)
            search_for_alerts(stockArray)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)






