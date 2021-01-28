import config
from twilio.rest import Client

account_sid = config.ACCOUNT_SID
auth_token = config.AUTH_TOKEN
client = Client(account_sid, auth_token)


def send_text(info, recipient):
    message = client.messages.create(
                              body=f'{info}',
                              from_='+13042440704',
                              to=f'+1{recipient}'
                          )
    print(message.sid, message.status, message.body)

