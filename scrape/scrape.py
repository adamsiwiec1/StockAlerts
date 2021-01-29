import requests
from bs4 import BeautifulSoup
from termcolor import colored
from alert.alert import user_input


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