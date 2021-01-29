import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from termcolor import colored
import text
from flask import Flask, request
from twilio.twiml.messaging_response import Body
from twilio import twiml

# Imported classes

app = Flask(__name__)

# email variables
sender = "stockalertsystem7@gmail.com"
adam_number = "5712911193@txt.att.net"
password = "Alert12345!"
phone_number = 5712911193


class User(object):

    def __int__(self, email, phone=None):
        self.email = email
        self.phone = phone


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
    formatted_email = f"\n{stock.acronym}: Price: " + stock.price + "!!!!Raw:\n\n: " + stock.raw + "\n\n"
    formatted_text = f"{stock.acronym} PRICE {stock.price}"
    subject_alert = f"{stock.name} HAS CHANGED"
    # send_email(subject_alert, formatted_email, )
    if User().phone is not None:
        stock.count += 1
        if stock.count <= 1:
            # stock.start_timer()
            text.send_text(formatted_text, User().phone)
        elif stock.count > 20:
            stock.reset_count()
            # stock.reset_timer()
        # elif stock.timer >= 30.00 and not None:
        #     text.send_text(formatted_text, User().phone)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    print(number)
    print(message_body)

    resp = twiml.messaging_response.MessagingResponse()
    resp.message('Text /price followed by a stock acronym to see details.'.format(number, message_body))
    return str(resp)


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

