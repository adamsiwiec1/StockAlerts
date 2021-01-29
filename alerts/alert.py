import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request
from twilio.base.exceptions import TwilioRestException
from twilio.twiml.messaging_response import Body
from twilio import twiml
from twilio.rest import Client
from alerts.env import Config as c
from termcolor import colored
import main


# email variables
sender = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
phone_number = 5712911193
# sms variables
account_sid = c.ACCOUNT_SID
auth_token = c.AUTH_TOKEN
client = Client(account_sid, auth_token)


class User(object):

    def __int__(self, email, phone=None):
        self.email = email
        self.phone = phone


# Currently not used, only doing text alerts
# def send_email(subject, stock_info, recipient):
#
#     msg = MIMEMultipart()
#
#     msg['From'] = sender
#
#     msg['Subject'] = f"{subject}"
#
#     body = stock_info
#
#     msg.attach(MIMEText(body, 'plain'))
#
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#
#     s.starttls()
#     try:
#         s.login(sender, password)
#     except smtplib.SMTPServerDisconnected or smtplib.SMTPException:
#         s.quit()
#         print(colored("The StockScraper faced an error sending your message.", "red"))
#         exit(421)
#
#     text = msg.as_string()
#     try:
#         s.sendmail(sender, recipient, text)
#     except smtplib.SMTPSenderRefused or smtplib.SMTPNotSupportedError or smtplib.SMTPException as e:
#         s.quit()
#         print(colored("The StockScraper message was refused by your phone/email.", "red"))
#         exit(421)
#     s.quit()


def send_text(info, recipient):
    try:
        message = client.messages.create(
                              body=f'{info}',
                              from_='+13042440704',
                              to=f'+1{recipient}'
                          )
        print(message.sid, message.status, message.body)
    except TwilioRestException:
        print(colored("The user has stopped the script or blocked the number. Please try again.", "red"))
        main.user_input()


def compare_price(stock_price, low, high):
    current_price = float(stock_price)

    if current_price < 0:
        print(colored("Error comparing stocks price.", "red"))
        return False
    elif current_price <= low:
        return True
    elif current_price >= high:
        return True
    else:
        return False


def send_alert(stock):
    formatted_email = f"\n{stock.acronym}: Price: " + stock.price + "!!!!Raw:\n\n: " + stock.raw + "\n\n"
    formatted_text = f"{stock.acronym} PRICE {stock.price}"
    subject_alert = f"{stock.name} HAS CHANGED"
    # send_email(subject_alert, formatted_email, )
    if User().phone is not None:
        stock.count += 1
        if stock.count <= 1:
            # stocks.start_timer()
            send_text(formatted_text, User().phone)
        elif stock.count > 20:
            stock.reset_count()
            # stocks.reset_timer()
        # elif stocks.timer >= 30.00 and not None:
        #     text.send_text(formatted_text, User().phone)


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

