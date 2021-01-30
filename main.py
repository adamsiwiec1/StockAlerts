import time
from pip._vendor.distlib.compat import raw_input
from program import alert, scrape
from termcolor import colored
from program.dictionary import StockDictionary
from program.stock import Stock
from program import alert

def user_input():
    # Welcome message + application instructions
    print("\nHello, Welcome to StockScraper. Instructions below: \n"
          "1. Enter the email address where you would like to receive alerts.\n"
          "**Important: The alerts will go to your spam folder, allow the email\n"
          "address stockalertsystem7@gmail.com to send you emails.**. \n"
          "2. Enter a stocks acronym. \n"
          "3. Enter a price floor and ceiling for the stocks.\n"
          "4. Press 'n' to add another stocks or enter to start searching.\n"
          "**Reply 'STOP' at any time to end the script**\n\n")

    # Define local variables used to retrieve user input
    acronyms = []
    floors = []
    ceilings = []

    # Retrieve User Attributes
    emailAddr = raw_input('Enter your email address: ')
    # No parenthesis to set?
    alert.User.email = emailAddr

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
                    raise ValueError("Please enter a stocks acronym.", "red")
                elif acronyms[stockIndex] in StockDictionary().NASDAQ:
                    raise ValueError("Please enter a NASDAQ or COLE stocks.")
                elif len(acronyms[stockIndex]) > 5:
                    raise ValueError("Enter a valid stocks acronym with less than 5 characters.", "red")
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
                print(colored("Error reading Price Floor. Enter a number greater than 0.00001.", "red"))
        while not ceilingInput:
            try:
                ceilings.append(float(raw_input(f'Enter Price Ceiling for {stockIndex + 1}: ')))
                if not ceilings[stockIndex]:
                    del ceilings[stockIndex]
                    raise ValueError("Please enter a Price Ceiling.", "red")
                elif floors[stockIndex] < 10000000000000000000000000000000.00:
                    ceilingInput = True
            except ValueError as e:
                print(colored("Error reading Price Ceiling. Please enter numbers only and do not use a dollar sign.)", "red"))
        while not escapeInput:
            try:
                print("\nType N and press enter to start the script!")
                anothaOne = input("\n\nWould you like to add another stocks? Y/N:").lower()
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
            t0 = time.perf_counter()
            # try:
            stockArray = scrape.scrape(stockObjects)
            for stock in stockArray:
                if stock.price is None:
                    print(f"There was an error pulling the price for {stock.acronym}")
                    del stock
            alert.search_for_alerts(stockArray)
            t1 = time.perf_counter()
            print("Completion time: ", t1 - t0)


if __name__ == '__main__':
    user_input()

