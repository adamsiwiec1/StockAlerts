from flask import Flask, request
from twilio.twiml.messaging_response import Body
from twilio import twiml


app = Flask(__name__)


# Text reply system
@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    print(number)
    print(message_body)

    resp = twiml.messaging_response.MessagingResponse()
    if message_body.lower() == "menu":
        resp.message("StockScraper Commands:\n/start\n/stop\n/mystocks\n/details 'STOCK'\n/price 'STOCK'"
                     "\n/add 'STOCK' \n/remove 'STOCK'".format(number, message_body))
    else:
        resp.message('Text /price followed by a stocks acronym to see details.'.format(number, message_body))
    return str(resp)


app.run()

