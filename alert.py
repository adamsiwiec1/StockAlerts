import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

from termcolor import colored
import keyboard as keyboard
import requests
from bs4 import BeautifulSoup
from pip._vendor.distlib.compat import raw_input
import sys
from linkedList import Sentinel_DLL

# Instance Variables
stock_dll = Sentinel_DLL() # Instance of a linked list for stock acronyms

# email variables
sender = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
phone_number = 5712911193

# cell phone variables
carriers = {
    "vzn": "vtext.com",
    "att": "txt.att.net",
    "spr": "sprintpaging.com",
    "tmb": "tmomail.net",
    "vgn": "vmobl.com"
}

stockdict = {

    "AZN": "AstraZeneca",
    "OGEN": "Oragenics Inc",
    "CHUC": "Charlie's Holdings Inc",
    "CLWD": "CloudCommerce",
    "TLSS": "Transport&Logs",
    "PLYZ": "Plyzer Tech"
}

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


class StockLibrary(object): # this is a linked list consisted of STOCK ACRONYMS
    def __init__(self):
        self.stock = Stock

    # def add_stock(self, Stock):
    #     stock_dll.append(Stock.acronym)


class User(object):
    def __int__(self, email):
        self.email = email

    # def user_input(self,email):


def send_email(subject, stock_info, email_addr, recipient):

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

    s.sendmail(sender, recipient, text)

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


def pull_stock_info(Stock):

    print("Pulling info for " + Stock.name)

    yahoo = f"https://finance.yahoo.com/quote/{Stock.acronym}?p={Stock.acronym}&.tsrc=fin-srch"

    # Send HTTP Request
    page = requests.get(yahoo)

    # Pull HTTP from the request
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
        return data
    except AttributeError as a:
        print(f"|----!!!!FAILED TO PULL DATA FOR {Stock.acronym}:{Stock.name}!!!!----|\n|---- Attribute Error: {a} ----|\n")
        del Stock
        print(f"|----CORRUPT DATA HAS BEEN DELETED----|\n")


def get_price(stock_info):
    # Need to add exception handling in this method, there is already some later in in scrape()***********
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
    try:
        send_email(subject_alert, formatted_email, sender, User.email)
    except Exception as e:
        print(colored(f"There was a fatal error sending your email. Make sure you have it configured correctly. ERROR: {e}", "red"))
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
            print(f"No alerts were found for {stocks[num]}")


def scrape(stocks):
    count = len(stocks)
    raw_stock = []
    price_stock = []
    try:
        for num in range(count):
            raw_stock.append(pull_stock_info(stocks[num]))

        for num in range(count):
            price_stock.append(get_price(raw_stock[num]))

        for num in range(count):
            stocks[num].raw = raw_stock[num]
            stocks[num].price = price_stock[num]
    except ValueError or TypeError or AttributeError as e:
        print(colored(f"!!Fatal error retrieving data!! Please input stock acronyms correctly.", "red"))
    try:
        if "," in price_stock[num]:
            price_stock[num] = price_stock[num].replace(',', '')
        elif price_stock[num]:
            stocks[num].float_price = float(price_stock[num])
        else:
            raise ValueError("|----$$Price Conversion Failure$$----|")
    except ValueError or TypeError or AttributeError as e:
        print(f"Failed to pull {stocks[num].name} ----| Error: {e}")
    return stocks

def main():
    print("\nHello, welcome to Adam's stock scraper. Instructions below: \n"
          "1. Enter your email address where you would like to receive alerts."
          "**Important: You must allow less secure apps in your email security "
          "settings. If this makes you uncomfortable, make a new email address for the alerts. \n"
          # "2. Enter a phone number (optional) for text alerts or press enter to continue without. \n"
          "2. Enter a stock acronym followed by a nickname. \n"
          "3. Enter a price floor and ceiling for the stock.\n"
          "4. Press 'n' to add another stock or enter to start searching.\n\n")
    emailAddr = raw_input('Enter your email address: ')
    User.email = emailAddr
    # phone = raw_input('Enter phone number or enter to continue without text alerts: ')
    acronyms = []
    nicknames = []
    floors = []
    ceilings = []

    escape = False
    value = True
    while not escape:
        stockIndex = len(acronyms)
        print(f"\nStock #{stockIndex + 1}:")
        acronymInput = False
        nicknameInput = False
        floorInput = False
        ceilingInput = False
        escapeInput = False
        while not acronymInput:
            try:
                acronyms.append(raw_input(f'Enter Stock Acronym #{stockIndex + 1}: '))
                if not acronyms[stockIndex] or len(acronyms[stockIndex]) > 4:
                    raise ValueError("Please enter a valid stock acronym.")
                else:
                    acronymInput = True
            except ValueError as e:
                print(e)
                del acronyms[stockIndex]
        while not nicknameInput:
            try:
                nicknames.append(raw_input(f'Enter Nickname #{stockIndex + 1}: '))
                if not nicknames[stockIndex]:
                    raise ValueError("Please enter a Nickname.")
                else:
                    nicknameInput = True
            except ValueError as e:
                print(e)
                del nicknames[stockIndex]
        while not floorInput:
            try:
                floor = float(raw_input(f'Enter Price Floor for {stockIndex + 1}: '))
                floors.append(floor)
                if not floors[stockIndex]:
                    del floors[stockIndex]
                    raise ValueError("Please enter a Price Floor.")
                elif floors[stockIndex] > 0.00001:
                    floorInput = True
            except ValueError as e:
                print(e)
        while not ceilingInput:
            try:
                ceilings.append(float(raw_input(f'Enter Price Ceiling for {stockIndex + 1}: ')))
                if not ceilings[stockIndex]:
                    del ceilings[stockIndex]
                    raise ValueError("Please enter a valid Price Ceiling.")
                elif floors[stockIndex] < 10000000000000000000000000000000.00:
                    ceilingInput = True
            except ValueError as e:
                print(e)
        while not escapeInput:
            try:
                print("\nType N and press enter to start the script!")
                anothaOne = input("\n\nWould you like to add another stock? Y/N:").lower()
                if anothaOne == 'y':
                    escape = False
                    escapeInput = True
                if anothaOne == 'n':
                    escape = True
                    escapeInput = True
                else:
                    raise ValueError("InputError: (Y/N)")
            except ValueError as e:
                print(e)

    acronymRange = len(acronyms)
    nicknameRange = len(nicknames)
    floorRange = len(floors)
    ceilingRange = len(ceilings)



    # Testing Linked List - pull stocks from dictionary and add to DLL
    dictionaryLength = len(stockdict)
    stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0)]  # for i in (range(acronymRange + dictionaryLength))
    for key, value in stockdict.items():
        stockObjects.append(Stock("", f"{value}", f"{str(key)}", "", 0.00, 0.00, 0.00))



    for x in range(acronymRange):
        stockObjects[x] = Stock("", f"{nicknames[x]}", f"{acronyms[x]}", "", 0.00, floors[x],
                              ceilings[x])
        # Testing Linked List - Adds Stock Acronyms to List
        add_to_dll(stockObjects[x])

    while True:
        if keyboard.is_pressed("ENTER"):
            sys.exit(0)
        else:
            t0 = time.perf_counter()
            stockArray = scrape(stockObjects)
            search_for_alerts(stockArray)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)

# Linked List branch

def add_to_dictionary(stockArray):
    try:
        for stock in stockArray:
            stockdict[stockArray[stock].acronym] = ('Name: ' + str(stockArray[stock].name) + "Price: " + str(stockArray[stock].price))
    except ValueError or AttributeError as e:
        print("Error in add to dictionary" + str(e))


def add_to_dll(Stock):
    try:
        stock_dll.append(str(Stock.acronym))
    except ValueError or AttributeError as e:
        print("An error occurred in add_to_dll  |" + str(e))


if __name__ == '__main__':
    main()








