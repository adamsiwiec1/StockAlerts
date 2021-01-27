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
sender = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
phone_number = 5712911193


class Stock(object):

    def __init__(self, raw, name, acronym, price, float_price, floor, ceiling):
        self.raw = raw,
        self.name = name.upper()
        self.acronym = acronym
        self.price = price
        self.float_price = float_price
        self.floor = floor
        self.ceiling = ceiling
        self.count = 0

    def alert_count(self):
        self.count += 1


class User(object):

    def __int__(self, email):
        self.email = email


def send_email(subject, stock_info, recipient):

    msg = MIMEMultipart()

    msg['From'] = sender

    msg['Subject'] = f"{subject}"

    body = stock_info

    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    try:
        s.login(sender, password)
    except smtplib.SMTPServerDisconnected or smtplib.SMTPException:
        s.quit()
        print(colored("The StockScraper faced an error sending your message.", "red"))
        exit(421)

    text = msg.as_string()
    try:
        s.sendmail(sender, recipient, text)
    except smtplib.SMTPSenderRefused or smtplib.SMTPNotSupportedError or smtplib.SMTPException as e:
        s.quit()
        print(colored("The StockScraper message was refused by your phone/email.", "red"))
        exit(421)
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
                    print(colored(f"!!!!Failed to pull {stock.acronym} - Trying again!!!!\n"), "red")
                    data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
                    if data is not None:
                        count = 4
            return data
        except AttributeError or UnboundLocalError:
            print(colored(f"\n|----!!!!FAILED TO PULL DATA FOR {stock.acronym} !!!!----|\n", "red"))
            print(colored("Restarting the program...Please enter correct stock acronyms.", "red"))
            user_input()
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
    # elif 'open' or 'close' not in stock_info:
    #     print(colored("Error: Not open or closed?", "red"))
    #     return "0.00"

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

    if current_price < 0:
        print(colored("Error comparing stock price.", "red"))
        return False
    elif current_price <= low:
        return True
    elif current_price >= high:
        return True
    else:
        return False


def send_alert(stock):
    formatted_email = f"\n{stock.name}: \n\n Price: " + stock.price + "Raw:\n\n: " + stock.raw + "\n\n"
    subject_alert = f"{stock.name} HAS CHANGED"
    send_email(subject_alert, formatted_email, User().email)


def search_for_alerts(stocks):  # Needs work. Maybe some exceptions?
    count = len(stocks)
    alerts = []
    for num in range(count):
        alerts.append(compare_price(stocks[num].float_price, stocks[num].floor, stocks[num].ceiling))

    for num in range(count):
        if alerts[num]:
            print(f"*****{stocks[num].acronym} has triggered an alert*****")
            send_alert(stocks[num])
        else:
            print(f"No alerts were found for {stocks[num].acronym}")


def scrape(stocks):  # Needs Cleaned - move outside exceptions into method?
    count = len(stocks)
    raw_stock = []
    price_stock = []
    for num in range(count):
        raw_stock.append(pull_stock_info(stocks[num]))

    for num in range(count):
        price = get_price(raw_stock[num])
        if float(price) <= 0:
            print(colored("There was an error retrieving a stock price.", "red"))
            price_stock.append(price)
        else:
            price_stock.append(price)

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
    while not escape:  # Need to make my loops more concise
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
                elif acronyms[stockIndex] in StockDictionary().NASDAQ:
                    raise ValueError("Please enter a NASDAQ or COLE stock.")
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
            # try:
            stockArray = scrape(stockObjects)
            for stock in stockArray:
                if stock.price is None:
                    print(f"There was an error pulling the price for {stock.acronym}")
                    del stock
            search_for_alerts(stockArray)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)


if __name__ == '__main__':
    user_input()

    # get_price(stock_info="70.35-0.22(-0.31%)At 4:00 pm EST")
