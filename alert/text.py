from alert import config
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml

account_sid = config.ACCOUNT_SID
auth_token = config.AUTH_TOKEN
client = Client(account_sid, auth_token)

app = Flask(__name__)


def send_text(info, recipient):
    message = client.messages.create(
                              body=f'{info}',
                              from_='+13042440704',
                              to=f'+1{recipient}'
                          )
    print(message.sid, message.status, message.body)


@app.route('/sms', methods=['POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    print(number)
    print(message_body)

    resp = twiml.messaging_response.MessagingResponse()
    resp.message('Text /price followed by a stock acronym to see details.'.format(number, message_body))
    return str(resp)


if __name__ == "__main__":
    app.run()
