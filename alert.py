import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from termcolor import colored
import time
import keyboard as keyboard
import requests
from bs4 import BeautifulSoup
from pip._vendor.distlib.compat import raw_input
import sys
from dictionary import StockDictionary

# email variables
email_address = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
phone_number = 5712911193


# CLI Commands (Argparse)
# args = parser.parse_args()


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
    # def add_stock(self, Stock):


class User(object):

    def __int__(self, email):
        self.email = email


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


def pull_stock_info(stock):
    print("Pulling info for " + stock.acronym)

    # Send HTTP request
    try:
        yahoo = f"https://finance.yahoo.com/quote/{stock.acronym}?p={stock.acronym}&.tsrc=fin-srch"
        page = requests.get(yahoo)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:  # Scrape html from the webpage
            count = 0
            data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
            if data is None:
                while count < 4:
                    count += 1
                    print(colored(f"!!!!Failed to {stock.acronym} - Trying again!!!!\n"), "red")
                    data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
                    if data is not None:
                        count = 4
            return data
        except AttributeError:
            print(f"|----!!!!FAILED TO PULL DATA FOR {stock.acronym} !!!!----|\n")
            del Stock
            print(f"|----CORRUPT DATA HAS BEEN DELETED----|\n")
    except requests.ConnectionError as e:
        print("Connection Error:" + str(e))
    except requests.Timeout as e:
        print("Timeout Error" + str(e))
    except requests.RequestException as e:
        print("General Error:" + str(e))
    except KeyboardInterrupt:
        print("Exiting the program.")


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
    try:
        formatted_email = f"\n{stock_name}: \n\n Price: " + stock_price + "Raw:\n\n: " + raw_information + "\n\n"
        subject_alert = f"{stock_name} HAS CHANGED"
        send_email(subject_alert, formatted_email, email_address, User.email)
    except Exception as e:
        print("We were unable to send an email to the address you provided. Error: (" + str(e))


def search_for_alerts(stocks):
    count = len(stocks)
    alerts = []
    for num in range(count):
        alerts.append(compare_price(stocks[num].float_price, stocks[num].floor, stocks[num].ceiling))

    for num in range(count):
        if alerts[num]:
            print(f"*****{stocks[num].acronym} has triggered an alert*****")
            send_alert(stocks[num].raw, stocks[num].price, stocks[num].name)
        else:
            print(f"No alerts were found for {stocks[num].acronym}")


def scrape(stocks):
    count = len(stocks)
    raw_stock = []
    price_stock = []
    for num in range(count):
        raw_stock.append(pull_stock_info(stocks[num]))

    for num in range(count):
        price_stock.append(get_price(raw_stock[num]))

    for num in range(count):
        stocks[num].raw = raw_stock[num]
        stocks[num].price = price_stock[num]
        try:
            if "," in price_stock[num]:
                price_stock[num] = price_stock[num].replace(',', '')
            elif price_stock[num]:
                stocks[num].float_price = float(price_stock[num])
            else:
                raise ValueError("|----$$Price Conversion Failure$$----|")
        except ValueError as e:
            print(f"Failed to pull {stocks[num].name} ----| Value Error: {e}")
    return stocks


def user_input():
    # Welcome message + application instructions
    print("\nHello, Welcome to StockScraper. Instructions below: \n"
          "1. Enter your email address where you would like to receive alerts.\n"
          "**Important: The alerts will go to your spam folder, allow the email\n"
          "address stockalertsystem7@gmail.com to send you emails.**. \n"
          "2. Enter a stock acronym. \n"
          "3. Enter a price floor and ceiling for the stock.\n"
          "4. Press 'n' to add another stock or enter to start searching.\n\n")

    # Define local variables used to retrieve user input
    acronyms = []
    floors = []
    ceilings = []

    # Retrieve User Attributes
    emailAddr = raw_input('Enter your email address: ')
    User.email = emailAddr

    # Retrieve Stock Input from User
    escape = False
    while not escape:
        stockIndex = len(acronyms)
        print(f"\nAdd Stock #{stockIndex + 1}:")
        acronymInput = False
        floorInput = False
        ceilingInput = False
        escapeInput = False
        while not acronymInput:
            try:
                acronyms.append(raw_input(f'Enter Stock Acronym #{stockIndex + 1}: '))
                if not acronyms[stockIndex]:
                    del acronyms[stockIndex]
                    raise ValueError("Please enter a stock acronym.", "red")
                # if acronyms[stockIndex] not in StockDictionary.NASDAQ:
                #     print("Please enter a NASDAQ stock.")
                elif len(acronyms[stockIndex]) > 5:
                    raise ValueError("Enter a valid stock acronym with less than 5 characters.", "red")
                else:
                    acronymInput = True
            except ValueError as e:  # If there is an Input/Value error, we print
                print("Error reading Stock Acronym. Try again. (Error: " + str(e) + ")", "red")
                del acronyms[stockIndex]  # Delete corrupted index if there is an error.
        while not floorInput:
            try:
                floor = float(raw_input(f'Enter Price Floor for {stockIndex + 1}: '))
                floors.append(floor)
                if not floors[stockIndex]:
                    del floors[stockIndex]
                    raise ValueError("Please enter a Price Floor.", "red")
                elif floors[stockIndex] > 0.00001:
                    floorInput = True
            except ValueError as e:
                print("Error reading Price Floor. Enter a number greater than 0.00001. (Error: " + str(e) + ")", "red")
        while not ceilingInput:
            try:
                ceilings.append(float(raw_input(f'Enter Price Ceiling for {stockIndex + 1}: ')))
                if not ceilings[stockIndex]:
                    del ceilings[stockIndex]
                    raise ValueError("Please enter a Price Ceiling.", "red")
                elif floors[stockIndex] < 10000000000000000000000000000000.00:
                    ceilingInput = True
            except ValueError as e:
                print(colored(
                    "Error reading Price Ceiling. Please enter numbers only and do not use a dollar sign. (Error: " + str(
                        e) + ")"), "red")
        while not escapeInput:
            try:
                print("\nType N and press enter to start the script!")
                anothaOne = input("\n\nWould you like to add another stock? Y/N:").lower()
                if anothaOne == 'y':
                    escape = False
                    escapeInput = True
                elif anothaOne == 'n':
                    escape = True
                    escapeInput = True
                else:
                    raise ValueError("InputError: (Y/N)", "red")
            except ValueError as e:
                print(e)

    acronymRange = len(acronyms)

    stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0) for i in range(acronymRange)]
    for acronym in range(acronymRange):
        stockObjects[acronym] = Stock("", "", f"{acronyms[acronym]}", "", 0.00, floors[acronym],
                                      ceilings[acronym])

    while True:
        if keyboard.is_pressed("ENTER"):
            sys.exit(0)
        else:
            t0 = time.perf_counter()
            try:
                stockArray = scrape(stockObjects)
            except Exception as e:
                print(colored("Error. Follow the directions and try again.", "red"))
                user_input()
            try:
                search_for_alerts(stockArray)
            except Exception as e:
                print("Error searching for alerts. (Error: " + str(e))
        t1 = time.perf_counter()
        print("Completion time: ", t1 - t0)


if __name__ == '__main__':
    user_input()
