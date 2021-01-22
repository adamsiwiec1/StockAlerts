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
from pip._vendor.distlib.compat import raw_input
from requests import get
import sys

# email variables
email_address = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
recipient = email_address
phone_number = 5712911193

# email_address = "stockalertsystem7@gmail.com
# password = "Stock12345!"
# recipient = email_address

# # cell phone variables
# carriers = {
#     "vzn": "vtext.com",
#     "att": "txt.att.net",
#     "spr:": "sprintpaging.com",
#     "tmb": "tmomail.net",
#     "vgn": "vmobl.com"
# }


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


def send_email(subject, stock_info, email_addr, recipients):

    sender = email_addr

    msg = MIMEMultipart()

    msg['From'] = sender

    msg['Subject'] = f"{subject}"

    body = stock_info

    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(sender, password)

    text = msg.as_string()

    s.sendmail(sender, recipients, text)

    s.quit()

# def send_text(message, carrier , phone_number):
#
#     msg = MIMEMultipart()
#
#     msg['From'] = ""
#
#     body = "This is a Text Message."
#
#     msg.attach(MIMEText(body, 'plain'))
#
#     ts = smtplib.SMTP('smtp.gmail.com', 587)
#
#     ts.starttls()
#
#     ts.login(email_address, password)
#
#     text = msg.as_string()
#
#     ts.sendmail(email_address, phone_number, text)
#
#     ts.quit()


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

    if current_price <= low:
        return True
    if current_price >= high:
        return True
    else:
        return False


def send_alert(raw_information, stock_price, stock_name):

    formatted_email = f"\n{stock_name}: \n\n Price: " + stock_price + "Raw:\n\n: " + raw_information + "\n\n"

    subject_alert = f"{stock_name} HAS CHANGED"

    send_email(subject_alert, formatted_email, email_address, adam_number)
    # send_text(stock_name + " has changed to " + stock_price, adam_address)


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

    print("\nHello, welcome to Adam's stock scraper. Instructions below: \n"
          "1. Enter your email address where you would like to receive alerts.\n"
          # "2. Enter a phone number (optional) for text alerts or press enter to continue without. \n"
          "2. Enter a stock acronym followed by a nickname. \n"
          "3. Enter a price floor and ceiling for the stock.\n"
          "4. Press 'n' to add another stock or enter to start searching.\n\n")
    email = raw_input('Enter your email address: ')
    # phone = raw_input('Enter phone number or enter to continue without text alerts: ')
    acronyms = []
    nicknames = []
    floors = []
    ceilings = []
    allowedCharacters = 'abcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'
    acronyms.append(raw_input('Enter Stock Acronym #1: '))
    nicknames.append(raw_input('Enter Nickname #1: '))
    floors.append(float(raw_input(f'Enter Price Floor for Stock #1: ')))
    ceilings.append(float(raw_input(f'Enter Price Ceiling for Stock #1: ')))

    escape = False
    value = True
    while not escape:
        stockIndex = len(acronyms)
        print("New stock:\n")
        acronymInput = False
        nicknameInput = False
        floorInput = False
        ceilingInput = False
        while not acronymInput:
            try:
                acronyms.append(raw_input(f'Enter Stock Acronym #{stockIndex+1}: '))
                if not acronyms[stockIndex]:
                    raise ValueError("Please enter a valid stock acronym.")
                else:
                    acronymInput = True
            except ValueError as e:
                print(e)
                del acronyms[stockIndex]
        while not nicknameInput:
            try:
                nicknames.append(raw_input(f'Enter Nickname #{stockIndex+1}: '))
                if not nicknames[stockIndex]:
                    raise ValueError("Please enter a Nickname.")
                else:
                    nicknameInput = True
            except ValueError as e:
                print(e)
                del nicknames[stockIndex]
        while not floorInput:
            try:
                floors.append(raw_input(f'Enter Price Floor for {stockIndex+1}: '))
                if not floors[stockIndex]:
                    raise ValueError("Please enter a Price Floor.")
                else:
                    floorInput = True
            except ValueError as e:
                print(e)
                del floors[stockIndex]
        while not ceilingInput:
            try:
                ceilings.append(raw_input(f'Enter Price Ceiling for {stockIndex+1}: '))
                if not ceilings[stockIndex]:
                    raise ValueError("Please enter a Price Ceiling.")
                else:
                    ceilingInput = True
            except ValueError as e:
                print(e)
                del ceilings[stockIndex]

        anothaOne = input("\n\nPress 'Enter' to add another stock or type '-1' then press 'Enter' to start the script:")

        if anothaOne == keyboard.is_pressed('Enter'):
            continue
        elif anothaOne == '-1':
            escape = True
            break

    acronymRange = len(acronyms)
    nicknameRange = len(nicknames)
    floorRange = len(floors)
    ceilingRange = len(ceilings)

    stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0) for i in range(acronymRange)]
    for acronym in range(acronymRange):
        stockObjects[acronym] = Stock("", f"{nicknames[acronym]}", f"{acronyms[acronym]}", "", 0.00, 0.01, 0.00)

    # stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0) for i in range(6)]
    # stockObjects[0] = Stock("", "Charlie's Holdings Inc", "CHUC", "", 0.00, 0.01, 0.00)
    # stockObjects[1] = Stock("", "Oragenics Inc", "OGEN", "", 0.00, 1.10, 0.15)
    # stockObjects[2] = Stock("", "AstraZeneca plc", "AZN", "", 0.00, 52.00, 2.23)
    # stockObjects[3] = Stock("", "CloudCommerce", "CLWD" , "", 0.00, 0.081, 0.05)
    # stockObjects[4] = Stock("", "Transport&Logs", "TLSS" , "", 0.00, 0.07, 0.02)
    # stockObjects[5] = Stock("", "Plyzer Tech", "PLYZ" , "", 0.00, 0.0016, 0.0000)
    # Testing notes:
    # email_address = "stockalertsystem7@gmail.com"
    # adam_number = "5712911193@txt.att.net"
    # password = "Alert12345!"

    while True:
        if keyboard.is_pressed("ENTER"):
            sys.exit(0)
        else:
            t0 = time.perf_counter()
            stockArray = main(stockObjects)
            search_for_alerts(stockArray)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)






